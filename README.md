# sonatype-lift-lib

Sonatype Lift Lib contains helper methods to easily get up and running with Sonatype Lift V1 Api for introducing customised tools

## Example usage

```python
#!/usr/bin/env python3
from sonatypeliftlib.apiv1 import ApiV1, ToolNote

class ApiV1Test(ApiV1):
    pass

    def tool_applicable(self):
        return ApiV1.is_applicable()

    def tool_run(self):
        tool_notes = []

        tn1 = ToolNote("Foo", "Foo Message", None, None, None)
        tool_notes.append(tn1)

        tn2 = ToolNote("Bar", "Bar Message", None, 1, None)
        tool_notes.append(tn2)
        return tool_notes

def main():
    tool = ApiV1Test("Test")
    tool.service()

if __name__ == "__main__":
    main()
```

ApiV1 expects to receive 3 parameters, which are project_path, commit hash command where command can be `applicable`, `name`, `run`. The response from a `run` should be an array of `ToolNote`'s.

Running the example above, for example `python3 apiv1_example.py . 1234 run` will yield the following output:

```json
[
    {
        "name": "Foo", 
        "message": "Foo Message",
        "line": 0
    },
    {
        "name": "Bar", 
        "message": "Bar Message",
        "line": 1
    }
]
```

For further details on the Api see [Lift Docs](https://help.sonatype.com/lift/extending-lift#ExtendingLift-APICommands)