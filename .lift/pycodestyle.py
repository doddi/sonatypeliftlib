#!/usr/bin/env python3
import sys
from sonatypeliftlib.apiv1 import ApiV1, ToolNote
from sonatypeliftlib.helpers import path_has_extension_recursive, run_with_args


class PyCodeStyle(ApiV1):
    def tool_applicable(self):
        if path_has_extension_recursive(self.path, ".py"):
            return ApiV1.is_applicable()
        else:
            return ApiV1.is_not_applicable()

    def tool_run(self):
        tool_notes = []

        response = run_with_args("pycodestyle", [self.path])
        if len(response.stderr) != 0:
            tool_notes.append(ToolNote("error", response.stderr, "somefile", 1, None))
            return tool_notes

        lines = response.stdout.decode().split("\n")

        for line in lines:
            split_line = line.split(':')
            if len(split_line) == 4:
                tool_notes.append(self.create_pycode_toolnote(split_line))

        return tool_notes

    def create_pycode_toolnote(self, split_line):
        _file = split_line[0]
        _line = split_line[1]
        _message = split_line[3].strip()
        _type = _message.split()[0]
        return ToolNote(_type, _message, _file, int(_line), None)


def main():
    tool = PyCodeStyle("PyCodeStyle", sys.argv)
    tool.service()

if __name__ == "__main__":
    main()
