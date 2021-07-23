#!/usr/bin/env python3
import json
import sys
import subprocess
import os

API_VERSION = 1

class ApiV1:
    def __init__(self, name, args):
        self.output = sys.stdout
        self.name = name

        if (len(args) < 4):
            self.__info()
            sys.exit()
            return

        self.path = args[1]
        self.commit = args[2]
        self.command = args[3]

    # This method is mainly used for testing to alter the output 
    def setoutput(self, out):
        self.output = out

    def __info(self):
        info = { "version": API_VERSION, "name": self.name }
        print(json.dumps(info), file = self.output)

    def __version(self):
        print(API_VERSION, file = self.output)

    def __tool_name(self):
        print(self.name, file = self.output)

    def __tool_run(self):
        response = self.tool_run()
        print(json.dumps(response, default=lambda o: o.__dict__), file = self.output)

    def tool_run(self):
        ApiV1.__must_implement()

    def __tool_applicable(self):
        response = self.tool_applicable()
        print(json.dumps(response))

    def tool_applicable(self):
        ApiV1.__must_implement()

    def service(self):
        if self.command == "run":
            self.__tool_run()
        elif self.command == "applicable":
            self.__tool_applicable()
        elif self.command == "name":
            self.__tool_name()
        else:
            self.__version()

    @staticmethod
    def __must_implement():
        print("This method must be overriden for your tool")
        sys.exit()

    @staticmethod
    def is_not_applicable():
        return False

    @staticmethod
    def is_applicable():
        return True     

class ToolNote:
    def __init__(self, type, message, file, line, details_url):
        self.type = type
        if message != None:
            self.message = message
            
        if line != None:
            self.line = line
        else:
            self.line = 1

        if details_url != None:
            self.details_url = details_url
        if file != None:
            self.file = file
        else:
            self.file = "unknown"

