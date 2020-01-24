# -*- coding: UTF-8 -*-
from __future__ import print_function
from gnr.web.gnrwebpage import GnrUserNotAllowed,GnrBasicAuthenticationError
from json import loads as json_loads, dumps as json_dumps
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from json_utils import JsonError
from decimal import Decimal
from  webob import exc


def default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


class JsonRpc(BaseComponent):
    skip_connection = True
    _debug = Debug

    def common_headers(self):
        return None
        # return {'Access-Control-Allow-Origin':'*')
        #         "Access-Control-Allow-Headers":"Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
        # }

    def rootPage(self, *args, **kwargs):
        self.response.content_type = 'application/json'  # normal responses forced to be json

        common_headers = self.common_headers()
        if common_headers:
            for kk, vv in common_headers.items():
                self.response.add_header(kk, vv)

        if self.request.method=='OPTIONS':
            return '{}'
        try:
            method_name = 'json_%s' % args[0] if args else 'index'
            try:
                # getPublicMethod allow to manage tags
                method = self.getPublicMethod('rpc', method_name)
            except (GnrUserNotAllowed, GnrBasicAuthenticationError) as err:
                if self._debug:
                    raise
                return JsonError(code=401, msg=err, headers=common_headers)
                
            if method is None:
                return JsonError(code=501, msg="Method method '%s' does not exist" % method_name[len("json_"):], headers=common_headers)
            try:
                body = self.request._request.body
                if body=='':
                    #print("NULL")
                    body="{}"
                body_json = json_loads(body)
            except Exception as err:
                if self._debug:
                    raise
                raise JsonError(code=400, msg="Unable to deserialize input data (malformed json request?)\n%s"%err, headers=common_headers)
            result = method(body_json)
            if self.response.content_type == 'application/json':
                jresult = json_dumps(result, default=default) #, cls=_DecimalEncoder)
                return jresult
            else:
                # per altri tipi di risposta
                return result

            # # trying to limit response length
            # max_mb = 4
            # if len(jresult)>1024*1024*max_mb:
            #     # max 5mb
            #     raise exc.HTTPInternalServerError('Response is too big (>%sMb)' % max_mb)

        except exc.WSGIHTTPException as err:
            if self._debug:
                raise
            # we can raise every webob.exc HTTP error
            #print("ERR1", err, file=sys.stderr)
            return JsonError(code=err.code, msg=err.body, headers=common_headers) 
        except JsonError as err:
            if self._debug:
                raise
            #print("ERR2", err, file=sys.stderr)
            return err
        except Exception as err:
            if self._debug:
                raise
            #print("ERR2", err, file=sys.stderr)
            return JsonError(code=500, msg=err, headers=common_headers)

    @public_method
    def index(self, json):
        # overwrite this if you need
        return JsonError(code=500, msg="Index method does not exist at root '/'", headers=self.common_headers())
