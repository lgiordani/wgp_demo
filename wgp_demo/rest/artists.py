import os

from flask import Blueprint, request, current_app

from wgp_demo.shared import http_response as hres

from wgp_demo.repositories import artist_json_repository as ajr
from wgp_demo.serializers import artist_serializer as asr
from wgp_demo.use_cases import artist_use_cases as auc
from wgp_demo.use_cases import request_object as ro


blueprint = Blueprint('artist', __name__)


@blueprint.route('/artists', methods=['GET'])
def artists():
    qrystr_params = {
        'filters': {},
        'weights': {}
    }

    for arg, values in request.args.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values
        elif arg.startswith('weight_'):
            qrystr_params['weights'][arg.replace('weight_', '')] = values

    request_object = ro.ArtistListRequestObject.from_dict(qrystr_params)

    repo = ajr.ArtistJsonRepository(current_app.config['JSON_DATA_FILE'])
    use_case = auc.ArtistListUseCase(repo)
    return hres.HttpResponse(use_case.execute(request_object)).json(asr.ArtistEncoder)


