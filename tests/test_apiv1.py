#!/usr/bin/env python3
from sonatypeliftlib.apiv1 import ApiV1


def test_tool_applicable():
    response = ApiV1.is_applicable()
    assert response == True

def test_tool_not_applicable():
    response = ApiV1.is_not_applicable()
    assert response == False

def test_displays_info():
    api = ApiV1("Foo")
    response = api.info()

    assert response == {}