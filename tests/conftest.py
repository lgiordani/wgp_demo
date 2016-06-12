import pytest


from wgp_demo.app import create_app
from wgp_demo.settings import TestConfig


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()