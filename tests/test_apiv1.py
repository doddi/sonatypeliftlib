#!/usr/bin/env python3
import io
import sys
from sonatypeliftlib.apiv1 import ApiV1, ToolNote


def test_tool_applicable():
    response = ApiV1.is_applicable()
    assert response == True

def test_tool_not_applicable():
    response = ApiV1.is_not_applicable()
    assert response == False

def test_displays_api_version():
    api = ApiV1Test('unknown')
    api.service()

    assert api.getoutput() == "1"

def test_display_tool_name():
    api = ApiV1Test('name')
    api.service()

    assert api.getoutput() == "Foo"

def test_displays_info():
    def dummy():
        return

    # Temporarily override sys.stdout
    original = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer

    # Temporarily override sys.exit
    original_exit = sys.exit
    sys.exit = dummy

    api = ApiV1('Foo', [])

    sys.stdout = original
    sys.exit = original_exit
    assert buffer.getvalue().strip() == """{"version": 1, "name": "Foo"}"""

def test_tool_run():
    api = ApiV1Test('run')
    api.service()

    assert api.getoutput() == """[{"type": "Foo", "message": "Foo Message", "line": 0}, {"type": "Bar", "message": "Bar Message", "line": 1}]""".strip()

class ApiV1Test(ApiV1):
    def __init__(self, command):
        super().__init__("Foo", ['Foo', '.', '1', command])
        self.redirected_output = io.StringIO()
        self.setoutput(self.redirected_output)

    def getoutput(self):
        return self.redirected_output.getvalue().strip()

    def tool_applicable(self):
        return ApiV1.is_applicable()

    def tool_run(self):
        tool_notes = []

        tn1 = ToolNote("Foo", "Foo Message", None, None, None)
        tool_notes.append(tn1)

        tn2 = ToolNote("Bar", "Bar Message", None, 1, None)
        tool_notes.append(tn2)
        return tool_notes
