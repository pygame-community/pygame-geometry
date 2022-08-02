from setuptools import setup, Extension
import subprocess
import shlex
import glob
import sys

extensions = [
    Extension(
        "geometry",
        sources=["src_c/geometry.c"]
    )
]


def build() -> None:
    setup(
        name="geometry",
        ext_modules=extensions,
    )


if __name__ == "__main__":
    if "format" in sys.argv:
        c_files = glob.glob("src_c/*.c")
        h_files = glob.glob("src_c/include/*.h")

        cmd = ["clang-format", "-i"] + c_files + h_files
        print(shlex.join(cmd))
        sys.exit(subprocess.call(cmd))

    build()

