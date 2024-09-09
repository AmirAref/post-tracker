import os

compat_os_name = os._name if os.name == "java" else os.name

if compat_os_name in ("nt", "ce"):

    def compat_expanduser(path: str) -> str:
        home_dir = os.environ.get("HOME")
        if not home_dir:
            return os.path.expanduser(path)
        elif not path.startswith("~"):
            return path
        i = path.replace("\\", "/", 1).find("/")  # ~user
        if i < 0:
            i = len(path)
        userhome = (
            os.path.join(os.path.dirname(home_dir), path[1:i]) if i > 1 else home_dir
        )
        return userhome + path[i:]
else:
    compat_expanduser = os.path.expanduser
