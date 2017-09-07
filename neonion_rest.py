"""neonion_rest

   Copyright (c) 2017 Florian Berger <flberger@florian-berger.de>
"""

# Work started on 06. Sep 2017.

import logging
import cherrypy
import threading
from collections import OrderedDict
import json
import urllib.parse

VERSION = "0.1.0"

LOGGER = logging.getLogger("neonion_rest")
LOGGER.setLevel(logging.DEBUG)
STDERR_FORMATTER = logging.Formatter("neonion_rest [{levelname}] {funcName}(): {message} (l.{lineno})")
STDERR_HANDLER = logging.StreamHandler()
STDERR_HANDLER.setFormatter(STDERR_FORMATTER)
LOGGER.addHandler(STDERR_HANDLER)

PORT = 8301
THREADS = 4
AUTORELOAD = False
WRITE_LOCK = threading.Lock()

class WebApp:
    """Web application main class, suitable as cherrypy root.
    """

    def __init__(self):
        """Initialise WebApp.
        """

        # Make self.__call__ visible to cherrypy
        #
        self.exposed = True

        self.targets = Targets()
        
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
        <title>neonion Annotations REST API</title>
    </head>
    <body>
        <h1>neonion Annotations REST API</h1>
        <p>Please call the API endpoints using a JSON request body.</p>
       <p>See <a href="https://github.com/FUB-HCC/neonion-rest">https://github.com/FUB-HCC/neonion-rest</a> for details.</p>
    </body>
</html>
"""

@cherrypy.popargs('target_iri')
class Targets:
    """Target handler.
    """

    def __init__(self):
        """Initialise.
        """

        self.targets = OrderedDict()
        self.annotations = Annotations()

        return

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, target_iri = None):
        """Handle given target.
        """

        if cherrypy.request.method == 'GET':

            if target_iri is None:

                return list(self.targets.values())

            if target_iri not in self.targets.keys():

                raise cherrypy.HTTPError(404) 
        
            return self.targets[target_iri]

        elif cherrypy.request.method == 'PUT':

            if target_iri is None:

                raise cherrypy.HTTPError(400)

            if target_iri in self.targets.keys():

                raise cherrypy.HTTPError(409) 

            # TODO: Validate input

            self.targets[target_iri] = cherrypy.request.json

            cherrypy.response.status = 201
            
            return {'url': '/targets/{0}'.format(urllib.parse.quote_plus(cherrypy.request.json['id']))}

        else:

            raise cherrypy.HTTPError(501)


@cherrypy.popargs('annotation_iri')
class Annotations:
    """Annotation handler.
    """

    def __init__(self):
        """Initialise.
        """

        self.annotations = OrderedDict()

        return

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, target_iri = None, annotation_iri = None):
        """Handle given target.
        """

        if cherrypy.request.method == 'GET':

            if annotation_iri is None:

                return list(self.annotations.values())

            if annotation_iri not in self.annotations.keys():

                raise cherrypy.HTTPError(404) 
        
            return self.annotations[annotation_iri]

        elif cherrypy.request.method == 'PUT':

            if annotation_iri is None:

                raise cherrypy.HTTPError(400)

            if annotation_iri in self.annotations.keys():

                raise cherrypy.HTTPError(409) 

            # TODO: Validate input

            self.annotations[annotation_iri] = cherrypy.request.json

            cherrypy.response.status = 201
            
            return {'url': '/targets/{0}/annotations/{1}'.format(urllib.parse.quote_plus(target_iri),
                                                                 urllib.parse.quote_plus(cherrypy.request.json['id']))}

        else:

            raise cherrypy.HTTPError(501)

    

def main():
    """Main function, for IDE convenience.
    """

    root = WebApp()

    config_dict = {"/" : {"tools.sessions.on" : True,
                          "tools.sessions.timeout" : 60},
                   "global" : {"server.socket_host" : "0.0.0.0",
                               "server.socket_port" : PORT,
                               "server.thread_pool" : THREADS,
                               "request.show_tracebacks": False,
                               "request.show_mismatched_params": False,
                               "tools.trailing_slash.on": False
                                   }}

    # Conditionally turn off Autoreloader
    #
    if not AUTORELOAD:

        cherrypy.engine.autoreload.unsubscribe()

    cherrypy.quickstart(root, config = config_dict)

    return

if __name__ == "__main__":

    main()
