neonion Annotations REST API
===================

This is a REST API specification and test server for the annotation database
of neonion [1] [2] .

[1] http://neonion.org/
[2] https://github.com/FUB-HCC/neonion


## Prerequisites

Test server and test script require Python [3].

[3] https://python.org/

The example server requires CherryPy [4] .

[4] http://cherrypy.org/

The API tests in this document require Requests [5].

[5] https://python-requests.org/


## Preparations

First, start the API test server:

    python neonion_rest.py

It will by default listen on port 8301 (from "n30n10n" :) ).

You can then run the examples in this document using

    python -m doctest README.md

## Setting up

    >>> from requests import request
    >>> import urllib.parse
    >>> API_HOST = '127.0.0.1:8301'
	>>>


## Targets

### Create a Target

*URI:* `/targets/TARGET_IRI`, where TARGET_IRI is a [percent-encoded URI](https://tools.ietf.org/html/rfc3986#section-2.1), with spaces replaced by plus signs.

*Method:* `PUT`

*Body:* A JSON represenation of the target.

*Returns:* A JSON object denoting the url of the newly created target on the server.

*Return codes:* `201` on success, `409` on conflict.

    >>> target_iri = urllib.parse.quote_plus('target:1')
    >>> url = 'http://{0}/targets/{1}'.format(API_HOST, target_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A1
    >>> r = request('PUT', url, json =  {"id": "target:1"})
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    201 Created
    >>> str(r.content, encoding = 'utf-8') 
    '{"url": "/targets/target%3A1"}'
    >>>

    >>> r = request('PUT', url, json =  {"id": "target:1"})
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    409 Conflict
    >>>


### Read Targets

URI: `/targets`

Method: `GET`

*Body:* Empty.

*Returns:* A list oft JSON target representations.

*Return codes:* `200`

    >>> url = 'http://{0}/targets'.format(API_HOST)
    >>> print(url)
    http://127.0.0.1:8301/targets
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    200 OK
    >>> str(r.content, encoding = 'utf-8')
    '[{"id": "target:1"}]'
    >>>

URI: `/targets/TARGET_IRI`, where TARGET_IRI is a [percent-encoded URI](https://tools.ietf.org/html/rfc3986#section-2.1), with spaces replaced by plus signs.

Method: `GET`

*Body:* Empty.

*Returns:* A JSON representation of the target.

*Return codes:* `200` on success, `404` if the target is not found.

    >>> target_iri = urllib.parse.quote_plus('target:1')
    >>> url = 'http://{0}/targets/{1}'.format(API_HOST, target_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A1
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    200 OK
    >>> str(r.content, encoding = 'utf-8') 
    '{"id": "target:1"}'
    >>>

    >>> target_iri = urllib.parse.quote_plus('target:DOES NOT EXIST')
    >>> url = 'http://{0}/targets/{1}'.format(API_HOST, target_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3ADOES+NOT+EXIST
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    404 Not Found
    >>>


### Update Targets

Updating targets is currently not supported.


### Delete Targets

Deleting targets is currently not supported.


## Annotations

### Create an Annotation

URI: `/targets/TARGET_IRI/annotations/ANNOTATION_IRI`, where TARGET_IRI and ANNOTATION_IRI are
[percent-encoded URIs](https://tools.ietf.org/html/rfc3986#section-2.1), with spaces replaced by plus signs.

Method: `PUT`

*Body:* A JSON represenation of the annotation.

*Returns:* A JSON object denoting the url of the newly created annotation on the server.

*Return codes:* `201` on success, `409` on conflict, `404` if the target to annotate is not found.

    >>> target_iri = urllib.parse.quote_plus('target:1')
    >>> annotation_iri = urllib.parse.quote_plus('annotation:1') 
    >>> url = 'http://{0}/targets/{1}/annotations/{2}'.format(API_HOST, target_iri, annotation_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A1/annotations/annotation%3A1
    >>> r = request('PUT', url, json =  {"id": "annotation:1"})
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    201 Created
    >>> str(r.content, encoding = 'utf-8') 
    '{"url": "/targets/target%3A1/annotations/annotation%3A1"}'
    >>>

    >>> r = request('PUT', url, json =  {"id": "annotation:1"})
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    409 Conflict
    >>>

    >>> target_iri = urllib.parse.quote_plus('target:DOES NOT EXIST')
    >>> annotation_iri = urllib.parse.quote_plus('annotation:2') 
    >>> url = 'http://{0}/targets/{1}/annotations/{2}'.format(API_HOST, target_iri, annotation_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3ADOES+NOT+EXIST/annotations/annotation%3A2
    >>> r = request('PUT', url, json =  {"id": "annotation:1"})
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    404 Not Found
    >>>


### Read Annotations

URI: `/targets/TARGET_IRI/annotations`, where TARGET_IRI is a [percent-encoded URI](https://tools.ietf.org/html/rfc3986#section-2.1), with spaces replaced by plus signs.

Method: `GET`

*Body:* Empty.

*Returns:* A list oft JSON annotation representations.

*Return codes:* `200`

    >>> target_iri = urllib.parse.quote_plus('target:1')
    >>> url = 'http://{0}/targets/{1}/annotations'.format(API_HOST, target_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A1/annotations
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    200 OK
    >>> str(r.content, encoding = 'utf-8')
    '[{"id": "annotation:1"}]'
    >>>

URI: `/targets/TARGET_IRI/annotations/ANNOTATION_IRI`, where TARGET_IRI and ANNOTATION_IRI are
[percent-encoded URIs](https://tools.ietf.org/html/rfc3986#section-2.1), with spaces replaced by plus signs.

Method: `GET`

*Body:* Empty.

*Returns:* A JSON representation of the annotation.

*Return codes:* `200` on success, `404` if the annotation or the target is not found.

    >>> target_iri = urllib.parse.quote_plus('target:1') 
    >>> annotation_iri = urllib.parse.quote_plus('annotation:1') 
    >>> url = 'http://{0}/targets/{1}/annotations/{2}'.format(API_HOST, target_iri, annotation_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A1/annotations/annotation%3A1
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    200 OK
    >>> str(r.content, encoding = 'utf-8') 
    '{"id": "annotation:1"}'
    >>>

    >>> target_iri = urllib.parse.quote_plus('target:1') 
    >>> annotation_iri = urllib.parse.quote_plus('annotation:DOES NOT EXIST')
    >>> url = 'http://{0}/targets/{1}/annotations/{2}'.format(API_HOST, target_iri, annotation_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A1/annotations/annotation%3ADOES+NOT+EXIST
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    404 Not Found
    >>>

    >>> target_iri = urllib.parse.quote_plus('target:DOES NOT EXIST') 
    >>> annotation_iri = urllib.parse.quote_plus('annotation:2') 
    >>> url = 'http://{0}/targets/{1}/annotations/{2}'.format(API_HOST, target_iri, annotation_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3ADOES+NOT+EXIST/annotations/annotation%3A2
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    404 Not Found
    >>>

The list of annotations of a target may be empty.

    >>> target_iri = urllib.parse.quote_plus('target:2')
    >>> url = 'http://{0}/targets/{1}'.format(API_HOST, target_iri)
    >>> r = request('PUT', url, json =  {"id": "target:2"})
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    201 Created
    >>>

    >>> target_iri = urllib.parse.quote_plus('target:2')
    >>> url = 'http://{0}/targets/{1}/annotations'.format(API_HOST, target_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A2/annotations
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    200 OK
    >>> str(r.content, encoding = 'utf-8')
    '[]'
    >>>

Double-checking that no existing annotations are found on newly created targets:

    >>> target_iri = urllib.parse.quote_plus('target:2') 
    >>> annotation_iri = urllib.parse.quote_plus('annotation:1') 
    >>> url = 'http://{0}/targets/{1}/annotations/{2}'.format(API_HOST, target_iri, annotation_iri)
    >>> print(url)
    http://127.0.0.1:8301/targets/target%3A2/annotations/annotation%3A1
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    404 Not Found
    >>>


### Update Annotations

Updating annotations is currently not supported.


### Delete Annotations

Deleting annotations is currently not supported.
