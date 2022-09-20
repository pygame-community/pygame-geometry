# Contributing Guidelines
In order to contribute to the project, you must follow these guidelines...
1. Follow PEP8 convention naming rules for C and Python
2. Lint your code with [black](https://github.com/psf/black)
3. Please make an issue first before submitting a pull request
4. Always add unittests when you're introducing something new
5. For C code, try to use `FASTCALL` as much as you can
6. Make sure your code actually works before you submit a pull
request
7. Please be patient when waiting for pull request reviews,
we are all unpaid-volunteers

See below to see how to build pygame_geometry from source...

## Windows 10 / Windows 11
1. Install Python 3.7+
2. Install [Visual Studio Build Tools 2017](https://aka.ms/vs/15/release/vs_buildtools.exe) and make sure you mark `MSVC v140 - VS 2015 C++ build tools (v14.00)` with the installation
3. Run `python -m pip install setuptools -U`
4. Install the latest version of [git](https://gitforwindows.org/)
5. Run `git clone https://github.com/novialriptide/pygame_geometry.git`
6. Run `cd pygame_geometry; python -m pip install .`

**If you are having trouble re-compiling, try deleting the `build` folder from the root directory if it exists**
