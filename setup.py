from setuptools import setup, Extension
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
    build()

