# sonatype-lift-lib

Sonatype Lift Lib contains helper methods to easily get up and running with Sonatype Lift V1 Api for introducing customised tools

## Example usage

```python
#!/usr/bin/env python3
from sonatypeliftlib.apiv1 import ApiV1, ToolNote
import sonatypeliftlib.helpers as lift
import sys

def js_present_in_diffs():
    '''
    This is a helper method that will use a utility method to check if any of the files that
    have changed in the PR end with a '.js'. If no js files have changed then we dont need to run
    '''
    files = lift.get_diff_files()
    if files is not None:
        for file in files:
            if file.endswith(".js"):
                return True
    return False

class ApiV1Test(ApiV1):

    def tool_applicable(self):
        if js_present_in_diffs() is True:
            return ApiV1.is_applicable()
        return ApiV1.is_not_applicable()

    def tool_run(self):
        tool_notes = []

        tn1 = ToolNote("Foo", "Foo Message", "Foo.txt", None, None)
        tool_notes.append(tn1)

        tn2 = ToolNote("Bar", "Bar Message", "Bar.yml", 2, None)
        tool_notes.append(tn2)
        return tool_notes

def main():
    tool = ApiV1Test("Test", sys.argv)
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