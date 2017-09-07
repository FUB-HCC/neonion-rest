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

    >>> url = 'http://{0}/targets'.format(API_HOST)
    >>> print(url)
    http://127.0.0.1:8301/targets
    >>> r = request('GET', url)
    >>> print('{0} {1}'.format(r.status_code, r.reason))
    200 OK
    >>> str(r.content, encoding = 'utf-8')
    '[{"id": "target:1"}]'
    >>>

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

### Read Annotations

### Update Annotations

Updating annotations is currently not supported.

### Delete Annotations

Deleting annotations is currently not supported.
