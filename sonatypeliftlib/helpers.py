import os
import sys
import subprocess

@staticmethod
def file_exists_in_path_recursive(path, file):
    for (dirpath, dirnames, entry) in os.walk(path):
        if entry.is_file() and entry.name == file:
            return True
    return False

@staticmethod
def path_has_extension_recursive(path, extension):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith(extension):
                return True

    return False   

@staticmethod
def run_with_args(command, arguments):
    to_execute = [command]
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
        
@staticmethod
def __get_commit(value):
    if os.environ[value] is not None:
        temp = os.environ[value]
        if temp.startswith("Commit"):
            temp = temp.strip("Commit")
            temp = temp.replace(' ', '')
            temp = temp.replace('"', "")
            return temp
    return None

@staticmethod
def __get_src_commit():
    return __get_commit("LIFT_DST_SHA")

@staticmethod
def __get_dst_commit():
    return __get_commit("LIFT_SRC_SHA")

@staticmethod
def __get_is_pr():
    if os.environ["LIFT_IS_PR_REQUEST"] is not None:
        value = os.environ["LIFT_IS_PR_REQUEST"]
        return bool(value)
    return False

@staticmethod
def __can_get_diffs():
    if __get_src_commit() is not None and __get_dst_commit() is not None:
        return True
    return False

@staticmethod
def get_diff_files():
    '''
    This function will return an array of files changed between the commits,
    otherwise `None`
    '''
    if __get_is_pr() and __can_get_diffs():
        res = run_with_args("git", ["diff", "--name-only", __get_src_commit(), __get_dst_commit()])
        lst = res.stdout.decode().split("\n")
        filtered = [var for var in lst if var]
        return filtered
    return None