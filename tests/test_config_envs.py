# -*- coding: utf-8 -*-
"""Test configs."""
from wgp_demo.app import create_app
from wgp_demo.settings import DevConfig, TestConfig, ProdConfig


def test_dev_config():
    app = create_app(DevConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True


def test_test_config():
    app = create_app(TestConfig)
    assert app.config['ENV'] == 'test'
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is True


def test_prod_config():
    app = create_app(ProdConfig)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
