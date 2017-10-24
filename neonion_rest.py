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

def cors():
  if cherrypy.request.method == 'OPTIONS':
    print("CORS PREFLIGHT! requested OPTIONS")
    # preflign request
    # see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0
    cherrypy.response.headers['Access-Control-Allow-Methods'] = 'PUT'
    cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
    cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'
    # tell CherryPy no avoid normal handler
    return True
  else:
    print("ENABLE CORS Access-Control-Allow-Origin")
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)


class WebApp:
    """Web application main class, suitable as cherrypy root.
    """

    def __init__(self):
        """Initialise WebApp.
        """

        # Make self.__call__ visible to cherrypy
        #
        self.exposed = True

        self.targets_dict = OrderedDict()
        self.annotations_dict = OrderedDict()
        self.mapping_dict = {}

        self.targets = Targets(self.targets_dict, self.annotations_dict, self.mapping_dict)

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

    def __init__(self, targets_dict, annotations_dict, mapping_dict):
        """Initialise.
        """

        self.targets_dict = targets_dict
        self.annotations_dict = annotations_dict
        self.mapping_dict = mapping_dict

        self.annotations = Annotations(self.targets_dict, self.annotations_dict, self.mapping_dict)

        return

    @cherrypy.expose
    @cherrypy.config(**{'tools.cors.on': True})
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, target_iri = None):
        """Handle given target.
        """

        if target_iri is not None:

            target_iri = urllib.parse.unquote_plus(target_iri)

        if cherrypy.request.method == 'GET':

            if target_iri is None:

                return list(self.targets_dict.values())

            if target_iri not in self.targets_dict.keys():

                raise cherrypy.HTTPError(404)

            return self.targets_dict[target_iri]

        elif cherrypy.request.method == 'PUT':

            if target_iri is None:

                raise cherrypy.HTTPError(400)

            if not 'id' in cherrypy.request.json.keys():

                raise cherrypy.HTTPError(400)

            if not len(cherrypy.request.json['id']):

                raise cherrypy.HTTPError(400)

            if target_iri in self.targets_dict.keys():

                raise cherrypy.HTTPError(409)

            self.targets_dict[target_iri] = cherrypy.request.json

            self.mapping_dict[target_iri] = []

            cherrypy.response.status = 201

            return {'url': '/targets/{0}'.format(urllib.parse.quote_plus(cherrypy.request.json['id']))}

        else:

            raise cherrypy.HTTPError(501)


@cherrypy.popargs('annotation_iri')
class Annotations:
    """Annotation handler.
    """

    def __init__(self, targets_dict, annotations_dict, mapping_dict):
        """Initialise.
        """

        self.targets_dict = targets_dict
        self.annotations_dict = annotations_dict
        self.mapping_dict = mapping_dict

        return

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, target_iri = None, annotation_iri = None):
        """Handle given annotation.
        """

        if target_iri is not None:

            target_iri = urllib.parse.unquote_plus(target_iri)

        if annotation_iri is not None:

            annotation_iri = urllib.parse.unquote_plus(annotation_iri)

        if target_iri not in self.targets_dict.keys():

            raise cherrypy.HTTPError(404)

        if cherrypy.request.method == 'GET':

            if target_iri not in self.mapping_dict.keys():

                raise cherrypy.HTTPError(404)

            if annotation_iri is None:

                return [self.annotations_dict[iri] for iri in self.mapping_dict[target_iri]]

            if annotation_iri not in self.annotations_dict.keys():

                raise cherrypy.HTTPError(404)

            if annotation_iri not in self.mapping_dict[target_iri]:

                raise cherrypy.HTTPError(404)

            return self.annotations_dict[annotation_iri]

        elif cherrypy.request.method == 'PUT':

            if annotation_iri is None:

                print("1")

                raise cherrypy.HTTPError(400)

            print(list(cherrypy.request.json.keys()))

            if not '@context' in cherrypy.request.json.keys():

                print("2")

                raise cherrypy.HTTPError(400)

            if not cherrypy.request.json['@context'] == 'http://www.w3.org/ns/anno.jsonld':

                print("3")

                raise cherrypy.HTTPError(400)

            if not 'type' in cherrypy.request.json.keys():

                print("4")

                raise cherrypy.HTTPError(400)

            if not cherrypy.request.json['type'] == 'Annotation':

                print("5")

                raise cherrypy.HTTPError(400)

            if not 'id' in cherrypy.request.json.keys():

                print("6")

                raise cherrypy.HTTPError(400)

            if not len(cherrypy.request.json['id']):

                print("7")

                raise cherrypy.HTTPError(400)

            if not 'target' in cherrypy.request.json.keys():

                print("8")

                raise cherrypy.HTTPError(400)

            # TODO: Check for local target?
            #
            if not len(cherrypy.request.json['target']):

                print("9")

                raise cherrypy.HTTPError(400)

            if annotation_iri in self.annotations_dict.keys():

                raise cherrypy.HTTPError(409)

            self.annotations_dict[annotation_iri] = cherrypy.request.json

            self.mapping_dict[target_iri].append(annotation_iri)

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
                          "tools.sessions.timeout" : 60,
                          "tools.cors.on": True},
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
