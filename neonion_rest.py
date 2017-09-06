"""DESCRIPTION OF neonion_rest

   Copyright (c) 2017 Florian Berger <florian.berger@posteo.de>
"""

# This file is part of neonion_rest.
#
# neonion_rest is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# neonion_rest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with neonion_rest.  If not, see <http://www.gnu.org/licenses/>.

# Work started on 06. Sep 2017.

import logging
import cherrypy
import threading
from hashlib import sha256

VERSION = "0.1.0"

LOGGER = logging.getLogger("neonion_rest")
LOGGER.setLevel(logging.DEBUG)
STDERR_FORMATTER = logging.Formatter("neonion_rest [{levelname}] {funcName}(): {message} (l.{lineno})")
STDERR_HANDLER = logging.StreamHandler()
STDERR_HANDLER.setFormatter(STDERR_FORMATTER)
LOGGER.addHandler(STDERR_HANDLER)

PORT = 8399
THREADS = 4
AUTORELOAD = False
WRITE_LOCK = threading.Lock()



def logged_in(f):
    """A decorator to check for valid login before displaying a page.
    """

    def run_with_login_check(*args):

        if not cherrypy.session.get("logged_in"):

            return """<html>
    <head>
        <title>Login required</title>
    </head>
    <body>
        <p>Please <a href="/login">log in</a> to access this address.</p>
    </body>
</html>
"""

        return f(*args)

    return run_with_login_check

class WebApp:
    """Web application main class, suitable as cherrypy root.
    """

    def __init__(self):
        """Initialise WebApp.
        """

        self.login_hashes = [sha256("admin".encode("utf8") + "admin".encode("utf8")).hexdigest()]

        # Make self.__call__ visible to cherrypy
        #
        self.exposed = True

        return

    # Non-exposed method, acquiring a lock.
    #
    # Note that this is not thread or multi process safe, as
    # it ignores the current state of the file on disk or in
    # parallel threads / processes.
    #
    def write(self):
        """Write something to storage.
        """

        with WRITE_LOCK:

            with open("/tmp/safe_to_delete.txt", "wt", encoding = "utf8") as f:

                f.write("This file is safe to delete")

        return

    def __call__(self):
        """Called by cherrypy for the / root page.
        """

        return """<html>
    <head>
        <title>Hello World</title>
    </head>
    <body>
        <h1>Hello World</h1>
        <p><a href="/subpage">Go to subpage</a></p>
        <p><a href="/rss">View RSS</a></p>
        <p><a href="/admin">Go to admin page</a></p>
        <p><a href="/login">Log in</a></p>
        <p><a href="/logout">Log out</a></p>
    </body>
</html>
"""

    def subpage(self):

        return '<html><head><title>Hello World Subpage</title></head><body><h1>Hello World Subpage</h1><p><a href="/">Go to main page</a></p></body></html>'

    subpage.exposed = True

    # Example of a method with different Content-Type
    #
    @cherrypy.tools.response_headers(headers = [("Content-Type", "application/rss+xml")])
    def rss(self):
        """Return an RSS feed.
        """

        rss = """<?xml version="1.0"?>
<rss version="2.0">

   <channel>

      <title>{0}</title>
      <link>{1}</link>
      <description>A website running on {0}.</description>
      <generator>{0} v{2}</generator>
        """.format("WebApp", "https://#", VERSION)

        for item in [{"title": "An Item",
                      "uri": "http://#",
                      "description": "This is an item.",
                      "pubDate": "YYYY-MM-DD"}]:

            rss += """<item>
         <title>{}</title>
         <link>{}</link>
         <description>{}</description>
         <pubDate>{}</pubDate>
      </item>""".format(item["title"],
                        item["uri"],
                        item["description"],
                        item["pubDate"])

        rss += "</channel></rss>"

        # bytes output is required by the response_headers decorator
        #
        return bytes(rss, "utf8")

    rss.exposed = True

    def login(self, user = None, password = None):
        """If called without arguments, return a login form.
           If called with arguments, try to log in.
        """

        if (user is not None and password is not None):

            if sha256(user.encode("utf8") + password.encode("utf8")).hexdigest() in self.login_hashes:

                cherrypy.session["logged_in"] = True

                return "You are now logged in."

            else:
                return self.login()

        else:
            
            return """<html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <form action="/login" method="POST">
            <input type="text" name="user">
            <input type="password" name="password">
            <input type="submit">
        </form>
    </body>
</html>
"""

    login.exposed = True

    # Example of a page requiring login
    #
    @logged_in
    def admin(self):

        return "Admin access area."

    admin.exposed = True

    def logout(self):
        """Expire the current Cherrypy session for this user.
        """

        if cherrypy.session.get("logged_in"):

            cherrypy.lib.sessions.expire()

            return "You are now logged out."

        else:

            return "You are not logged in."

    logout.exposed = True

def main():
    """Main function, for IDE convenience.
    """

    root = WebApp()

    config_dict = {"/" : {"tools.sessions.on" : True,
                          "tools.sessions.timeout" : 60},
                   "global" : {"server.socket_host" : "127.0.0.1",
                               "server.socket_port" : PORT,
                               "server.thread_pool" : THREADS}}

    # Conditionally turn off Autoreloader
    #
    if not AUTORELOAD:

        cherrypy.engine.autoreload.unsubscribe()

    cherrypy.quickstart(root, config = config_dict)

    return

if __name__ == "__main__":

    main()
