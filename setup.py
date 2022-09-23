from pathlib import Path
from setuptools import setup, Extension
import subprocess
import json
import shlex
import sys
import os


extra_compiler_options = []

if sys.platform == "linux" or sys.platform == "linux2":
    extra_compiler_options.append("-mavx2")
elif sys.platform == "win32":
    extra_compiler_options.append("/arch:AVX2")
elif sys.platform == "darwin":
    pass

extensions = [
    Extension(
        "geometry",
        sources=["src_c/geometry.c"],
        extra_compile_args=extra_compiler_options,
    )
]


def consume_arg(arg: str) -> bool:
    if arg in sys.argv:
        sys.argv.remove(arg)
        return True
    return False


def get_geometry_cache_dir() -> Path:
    path = Path("./__geometry_cache__")

    path.mkdir(exist_ok=True)

    return path


def get_times_json_file() -> Path:
    path = get_geometry_cache_dir() / "times.json"

    path.touch(exist_ok=True)

    return path


def update_times_file() -> None:
    files = list(Path("./src_c/").glob("**/*.[c|h]"))

    data: Dict[str, float] = {str(file): os.path.getmtime(str(file)) for file in files}

    with open(get_times_json_file(), "w") as f:
        f.truncate(0)
        f.write(json.dumps(data, indent=4))


def needs_to_be_rebuild() -> bool:
    files = list(Path("./src_c/").glob("**/*.[c|h]"))

    with open(get_times_json_file(), "r+") as f:
        file_contents = f.read()
        data: Dict[str, float]

        if file_contents == "":
            data = {}
        else:
            data = json.loads(file_contents)

        if not data:
            for file in files:
                data[str(file)] = os.path.getmtime(str(file))

            f.write(json.dumps(data, indent=4))

            return True

        result = False

        for file in files:
            if data[str(file)] != os.path.getmtime(str(file)):
                data[str(file)] = os.path.getmtime(str(file))
                result = True

    with open(get_times_json_file(), "w") as f:
        f.truncate(0)
        f.write(json.dumps(data, indent=4))

    return result


def build() -> None:
    if not needs_to_be_rebuild():
        return

    with open("src_c/geometry.c", "rb+") as f:
        f.write(b"")

    setup(
        name="geometry",
        ext_modules=extensions,
    )

    # we are updating the times because we changed geometry.c
    # to rebuild the project
    update_times_file()


def main() -> None:
    if consume_arg("--format"):
        cmd = ["clang-format", "-i"] + [
            str(file) for file in Path("./src_c/").glob("**/*.[c|h]")
        ]
        print(shlex.join(cmd))
        subprocess.call(cmd)

        cmd = ["black", "."]
        print(shlex.join(cmd))
        subprocess.call(cmd)

    if consume_arg("--test"):
        cmd = ["python", "-m", "unittest"] + [
            str(file) for file in Path("./test/").glob("test_*.py")
        ]
        print(shlex.join(cmd))
        subprocess.call(cmd)

    build()


if __name__ == "__main__":
    main()
