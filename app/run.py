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
from flask import Flask, render_template

app = Flask(__name__, static_folder="src", template_folder="templates")


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/channel/")
def channel():
    return render_template("app.html")


# This is the default catch all route.
# We need this because of the vue app.
@app.route("/<path:path>")
def default(path):
    print(path)
    return render_template("app.html")


if __name__ == "__main__":
    app.run("0.0.0.0", 1000, debug=True)
