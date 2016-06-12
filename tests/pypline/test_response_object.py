import pytest

from wgp_demo.pypline import request_object as plreq
from wgp_demo.pypline import response_object as plres


@pytest.fixture
def response_value():
    return {'key': ['value1', 'value2']}


@pytest.fixture
def response_type():
    return 'ResponseError'


@pytest.fixture
def response_message():
    return 'This is a response error'


def test_response_success_is_true(response_value):
    assert bool(plres.ResponseSuccess(response_value)) is True


def test_response_failure_is_false(response_type, response_message):
    assert bool(plres.ResponseFailure(response_type, response_message)) is False


def test_response_success_contains_value(response_value):
    response = plres.ResponseSuccess(response_value)

    assert response.value == response_value


def test_response_failure_has_type_and_message(response_type, response_message):
    response = plres.ResponseFailure(response_type, response_message)

    assert response.type == response_type
    assert response.message == response_message


def test_response_failure_contains_value(response_type, response_message):
    response = plres.ResponseFailure(response_type, response_message)

    assert response.value == {'type': response_type, 'message': response_message}


def test_response_failure_from_invalid_request_object():
    response = plres.ResponseFailure.build_from_invalid_request_object(plreq.InvalidRequestObject())

    assert bool(response) is False


def test_response_failure_from_invalid_request_object_with_errors():
    request_object = plreq.InvalidRequestObject()
    request_object.add_error('path', 'Is mandatory')
    request_object.add_error('path', "can't be blank")

    response = plres.ResponseFailure.build_from_invalid_request_object(request_object)

    assert bool(response) is False
    assert response.type == plres.ResponseFailure.PARAMETERS_ERROR
    assert response.message == "path: Is mandatory\npath: can't be blank"
