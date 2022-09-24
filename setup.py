from setuptools import setup, Extension
import subprocess
import shlex
import glob
import sys
import os


compiler_options = {"unix": ["-mavx2"], "msvc": ["/arch:AVX2"]}

compiler_type = "msvc" if os.name == "nt" else "unix"


extensions = [
    Extension(
        "pygame_geometry",
        sources=["src_c/geometry.c"],
        extra_compile_args=compiler_options[compiler_type],
    )
]


def build() -> None:
    setup(
        name="pygame_geometry",
        ext_modules=extensions,
    )


if __name__ == "__main__":
    if "format" in sys.argv:
        c_files = glob.glob("src_c/*.c")
        h_files = glob.glob("src_c/include/*.h")

        cmd = ["clang-format", "-i"] + c_files + h_files
        print(shlex.join(cmd))
        subprocess.call(cmd)

        cmd = ["black", "."]
        print(shlex.join(cmd))
        subprocess.call(cmd)

        sys.exit(0)

    build()
