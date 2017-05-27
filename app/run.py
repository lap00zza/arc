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
from flask import Flask

app = Flask(__name__, static_folder="src")


@app.route("/")
def index():
    return "<em>Yo</em>"


@app.route("/channel/")
def channel():
    print("YO")
    return app.send_static_file("index.html")


@app.route("/<path:path>")
def default(path):
    print(path)
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run("0.0.0.0", 1000)
