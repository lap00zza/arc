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
import jwt
from datetime import datetime


class Auth:
    def __init__(self, secret, algorithm):
        self.secret = secret
        self.algorithm = algorithm

    # TODO: remember this part will validate against postgres
    def generate_token(self, email, password):
        return jwt.encode({
            "email": email,
            "iss": "arc",
            "iat": datetime.utcnow()
        }, self.secret, self.algorithm).decode("utf-8")
