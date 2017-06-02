"""
arc - dead simple chat
Copyright (C) 2017 Jewel Mahanta <jewelmahanta@gmail.com>

This file is part of arc.

arc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

arc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with arc.  If not, see <http://www.gnu.org/licenses/>.
"""
import psycopg2
import os
import bcrypt
from datetime import datetime
import hashlib
import re
# import uuid
# import random

# Seed the random number generator to prevent collisions
# while generating our id's
# random.seed(os.urandom(32))


# Custom meaningful exceptions.
class Error(Exception):
    pass


class LengthError(Error):
    def __init__(self, origin, message):
        self.origin = origin
        self.message = message


class NoUserError(Error):
    def __init__(self, message):
        self.message = message


class ValidationError(Error):
    """
    This is a general exception. Its meant to be raised when validation
    of input data fails.
    """
    def __init__(self, message):
        self.message = message


class DB:
    """
    Methods for interfacing with our database. We are using POSTGRES for
    as our database, but if you want to change it then all you have to do
    is modify this file.

    Attributes
    ----------
    db: str
        The name of the database to connect to.
    """
    def __init__(self):
        self.db = "arc"
        self.host = "postgres"
        self.port = 5432
        self.conn = None

    # A special thanks to OWASP for this awesome regex. Check out their page here:
    # https://www.owasp.org/index.php/OWASP_Validation_Regex_Repository
    @staticmethod
    def _is_valid_email(email: str):
        return bool(re.match("^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$", email))

    @staticmethod
    def _hash_password(password: str):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    @staticmethod
    def _hash_email(email: str):
        cleaned = email.lstrip().rstrip().lower()
        return hashlib.md5(cleaned.encode("utf-8")).hexdigest()

    # FIXME: this has 1 flaw, the id's are not time sortable.
    # So for now lets stick with postgresql's default serial.
    # @staticmethod
    # def generate_id():
    #     return uuid.uuid4().hex

    # Fetch a list of all available users.
    def get_all_users(self):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM users")
                return cur.fetchall()

    # Fetch a list of all the channels.
    def get_all_channels(self):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM channels")
                return cur.fetchall()

    # --- USER METHODS ---
    def create_user(self, username: str, email: str, password: str):
        """
        Create a new user. This method is called during the registration process.

        Raises
        ------
        LengthError
            Raised when password length is less than 8 or greater than 72 characters.
            Why 72? because bcrypt only works properly till 72.
        """
        if len(password) < 8 or len(password) > 72:
            raise LengthError("password", "Password length should be between 8 and 72 characters.")

        if not self._is_valid_email(email):
            raise ValidationError("Please enter a valid email-id.")

        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        INSERT INTO users (user_name, user_email, user_password_hash, user_timestamp, user_avatar)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (username, email, self._hash_password(password), datetime.utcnow(), self._hash_email(email))
                    )
                    return True

                # For now, this happens when the unique email constraint
                # is violated.
                except psycopg2.IntegrityError:
                    return False

    def verify_user(self, email: str, password: str):
        """
        Verify user on login.

        Raises
        ------
        NoUserError
            Raised when user's email-id does not exist.

        Returns
        -------
        bool
            Whether verification succeeded or failed.
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_password_hash FROM users WHERE user_email = %s
                    """,
                    (email, )
                )
                results = cur.fetchall()
                if len(results) == 0:
                    raise NoUserError("User does not exist. Do you want to register a new account?")

                return bcrypt.checkpw(password.encode("utf-8"), results[0][0].encode("utf-8"))

    # This is used with myInfo api endpoint
    def get_user_info(self, email: str):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id, user_name, user_avatar FROM users WHERE user_email = %s
                    """,
                    (email,)
                )
                results = cur.fetchall()
                if len(results) == 0:
                    raise NoUserError("User does not exist. Do you want to register a new account?")

                return results[0]

    # --- CHANNEL METHODS ---
    def create_channel(self, chan_name: str, chan_desc: str = None):
        """
        Create a new channel.

        Raises
        ------
        LengthError
            Raised when channel name is less than 1 or more than 50 characters.
        """
        if len(chan_name) < 1 or len(chan_name) > 50:
            raise LengthError("chan_name", "Channel name should be between 1 and 50 characters.")

        if chan_desc and len(chan_desc) > 512:
            raise LengthError("chan_desc", "Channel descriptions should be between 1 and 50 characters.")

        # TODO: catch integrity errors
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO channels (chan_name, chan_desc, chan_timestamp)
                    VALUES (%s, %s, %s)
                    """,
                    (chan_name, chan_desc, datetime.utcnow())
                )
                return True

    # The most crucial method
    def connect(self):
        """
        Initialize the database connection.
        **This should be called before using any other methods.**
        """
        self.conn = psycopg2.connect(
            dbname=self.db,
            user=os.environ.get("POSTGRES_USER") or "arc_admin",
            password=os.environ.get("POSTGRES_PASSWORD") or "this_is_a_really_long_fucking_password",
            host=self.host,  # "192.168.99.100"
            port=self.port
        )
