#!/usr/bin/env python3
import json
import sys
import subprocess
import os
import shutil
import hashlib

API_VERSION = 1

class ApiV1:
    def __init__(self, name):
        args = sys.argv

        self.name = name

        if (len(args) < 4):
            self.info()
            sys.exit()

        self.path = args[1]
        self.commit = args[2]
        self.command = args[3]

    def info(self):
        info = { "version": API_VERSION, "name": self.name }
        print(json.dumps(info))

    def version(self):
        print(API_VERSION)

    def tool_name(self):
        print(self.name)

    def _tool_run(self):
        response = self.tool_run()
        print(json.dumps(response, default=lambda o: o.__dict__))

    def tool_run(self):
        ApiV1.must_implement()

    def _tool_applicable(self):
        response = self.tool_applicable()
        print(json.dumps(response))

    def tool_applicable(self):
        ApiV1.must_implement()

    def service(self):
        args = sys.argv
        if (len(args) < 4):
            self.info()
        else:
            if self.command == "run":
                self._tool_run()
            elif self.command == "applicable":
                self._tool_applicable()
            elif self.command == "name":
                self.tool_name()
            else:
                self.version()

    @staticmethod
    def must_implement():
        print("This method must be overriden for your tool")
        sys.exit()

    @staticmethod
    def is_not_applicable():
        return False

    @staticmethod
    def is_applicable():
        return True

    @staticmethod
    def file_exists_recursive(path, file):
        for entry in os.scandir(path):
            if entry.is_file() and entry.name == file:
                return True
        return False

    @staticmethod
    def run_with_args(command, arguments):
        to_execute = command
        to_execute.extend(arguments)
        return subprocess.run(to_execute, capture_output=True)

    @staticmethod
    def reoutput_subprocess_io(executed, res):
        if len(res.stdout) > 0 or len(res.stderr) > 0:
            print("Called: " + str(executed), file=sys.stderr)
        if len(res.stdout) > 0:
            print(res.stdout.decode("utf-8"), file=sys.stderr)
        if len(res.stderr) > 0:
            print(res.stderr.decode("utf-8"), file=sys.stderr)


class ToolNote:
    def __init__(self, type, message, file, line, details_url):
        self.type = type
        if message != None:
            self.message = message
            
        if line != None:
            self.line = line
        else:
            self.line = 0

        if details_url != None:
            self.details_url = details_url
        if file != None:
            self.file = file

