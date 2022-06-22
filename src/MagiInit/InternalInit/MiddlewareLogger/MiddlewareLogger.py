##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## Middleware Logger
##


### LOGIC
# I/O stream
import sys

### INFRA
# File for Logs
from Infrastructure.Utils.FileLogger.FileLogger import FileLogger

# How to add a middleware to a flask app:
#
## calling our middleware
## app.wsgi_app = MiddlewareLogger(app.wsgi_app)
#

# JSON  lib import
import json

from werkzeug.wrappers import Request, Response

class MiddlewareLogger():
    def __init__(self, app):
        self.app = app
        self.__FileLogger = FileLogger()


    def __call__(self, environ, start_response):
        self.__Environ = environ
        self.__LogRequest()

        return self.app(environ, start_response)

    def __LogRequest(self):
        request = Request(self.__Environ)
        buffer = "Incoming Request Environ:"
        for i in request.environ:
            buffer += "\n\t- \"" + i + "\" = " + str(request.environ[i])
        self.__FileLogger.Logger.info(buffer)

        # TO Create à middleware for response
        # @app.after_request
        # def modify_outgoing(response):
        #     html = response.get_data(as_text=True)
        #     response.data = {modify html}
        #     return response

        ## TODO: Find a way to get_json
        # Current problem: when calling get_json, json empty for next route
        # Exemple:
        #   New request
        #       Entering Middleware
        #          Calling get_json for logs
        #       Entering a Post/Get/Delete method
        #           Calling get_json from flask.globals
        #           Returning an empty json
        # self.__FileLogger.Logger.info("request.get_json()")
        # self.__FileLogger.Logger.info(request.get_json())


#### log: ####

#  class werkzeug.wrappers.Request(environ, populate_request=True, shallow=False)

## content_type
##     The Content-Type entity-header field indicates the media type of the entity-body sent to the recipient or, in the case of the HEAD method, the media type that would have been sent had the request been a GET.


##  date
##     The Date general-header field represents the date and time at which the message was originated, having the same semantics as orig-date in RFC 822

##  get_json(force=False, silent=False, cache=True)
##     Parse data as JSON.
##     If the mimetype does not indicate JSON (application/json, see is_json), or parsing fails, on_json_loading_failed() is called and its return value is used as the return value. By default this raises a 400 Bad Request error.
##     Parameters
##             force (bool) – Ignore the mimetype and always try to parse JSON.
##             silent (bool) – Silence mimetype and parsing errors, and return None instead.
##             cache (bool) – Store the parsed JSON to return for subsequent calls.
##     Return type
##         Optional[Any]


## headers
##     The headers received with the request.

### property host_url: str
###     The request URL scheme and host only.

##  input_stream
##     The WSGI input stream.

### method
###     The method the request was made with, such as GET.

### query_string
###     The part of the URL after the “?”. This is the raw value, use args for the parsed values.

### scheme
###     The URL scheme of the protocol the request used, such as https or wss.

### property url: str
###     The full request URL with the scheme, host, root path, path, and query string.


#  class werkzeug.wrappers.Response(response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False)


## __call__(environ, start_response)
##     Process this response as WSGI application.
##     Parameters
##             environ (WSGIEnvironment) – the WSGI environment.
##             start_response (StartResponse) – the response callable provided by the WSGI server.
##     Returns
##         an application iterator
##     Return type
##         Iterable[bytes]



### property status: str
###     The HTTP status code as a string.
