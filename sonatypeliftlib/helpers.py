import os
import sys
import subprocess

def file_exists_in_path_recursive(path, file):
    for (dirpath, dirnames, entry) in os.walk(path):
        if entry.is_file() and entry.name == file:
            return True
    return False

def path_has_extension_recursive(path, extension):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith(extension):
                return True

    return False   

def run_with_args(command, arguments):
    to_execute = [command]
    to_execute.extend(arguments)
    return subprocess.run(to_execute, capture_output=True)

def reoutput_subprocess_io(executed, res):
    if len(res.stdout) > 0 or len(res.stderr) > 0:
        print("Called: " + str(executed), file=sys.stderr)
    if len(res.stdout) > 0:
        print(res.stdout.decode("utf-8"), file=sys.stderr)
    if len(res.stderr) > 0:
        print(res.stderr.decode("utf-8"), file=sys.stderr)
        
def __get_commit(value):
    if os.getenv(value) is not None:
        return os.getenv(value)
    return None

def __get_src_commit():
    return __get_commit("LIFT_DST_SHA")

def __get_dst_commit():
    return __get_commit("LIFT_SRC_SHA")

def __get_is_pr():
    if os.getenv("LIFT_IS_PR_REQUEST") is not None:
        value = os.getenv("LIFT_IS_PR_REQUEST")
        return value.lower() in ['true', '1', 1]
    return False

def __can_get_diffs():
    if __get_src_commit() is not None and __get_dst_commit() is not None:
        return True
    return False

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