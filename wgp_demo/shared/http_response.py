import json
from flask import Response

from wgp_demo.shared import response_object as res


class HttpResponse(object):
    STATUS_CODES = {
        res.ResponseFailure.RESOURCE_ERROR: 404,
        res.ResponseFailure.PARAMETERS_ERROR: 400,
        res.ResponseFailure.SYSTEM_ERROR: 500
    }

    def __init__(self, response_object):
        self._response_object = response_object

    def json(self, encoder=None):
        if self._response_object:
            return Response(json.dumps(self._get_successful_response_value(), cls=encoder),
                            mimetype='application/json',
                            status=200)
        else:
            return Response(json.dumps(self._get_failure_response_value(), cls=encoder),
                            mimetype='application/json',
                            status=self.STATUS_CODES[self._response_object.type])

    def _get_failure_response_value(self):
        return self._response_object.value

    def _get_successful_response_value(self):
        return self._response_object.value
