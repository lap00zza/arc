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
import time
import math
ARC_EPOCH = 1496595546533


class Snowflake:
    """
    Arc snowflake has the following structure
    +------------------+-----------------+-----------------+
    | 41 bit timestamp | 13 bit shard_id | 10 bit sequence |
    +------------------+-----------------+-----------------+

    We use our custom epoch. Each components have the following
    upper limits:

        timestamp (2^41) - 1 = 2199023255551
        shard_id  (2^13) - 1 = 8191
        sequence  (2^10) - 1 = 1023

    So roughly speaking, we can generate 1024 id's per millisecond
    per shard.

    Credits:
    --------
    This id generation technique borrows heavily from instagram's
    implementation of twitter snowflake. You can read more about
    it here: https://engineering.instagram.com/sharding-ids-at-instagram-1cf5a71e5a5c
    """
    def __init__(self, shard_id=0):
        self.last_timestamp = 0
        self.sequence = 0
        self.SHARD_ID = shard_id

    def generate(self):
        timestamp = (math.floor(time.time()) * 1000) - ARC_EPOCH
        if self.last_timestamp == timestamp:
            self.sequence += 1
        else:
            self.sequence = 0

        if self.sequence >= 1023:
            print("Sleeping")
            time.sleep(1/1000)

        self.last_timestamp = timestamp
        gen_id = (timestamp << 23) + (self.SHARD_ID << 10) + self.sequence
        return gen_id

snowflake = Snowflake()
