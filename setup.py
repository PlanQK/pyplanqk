"""
    Setup file for pyplanqk.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.4.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup

if __name__ == "__main__":
    try:
        f = open("requirements.txt", "r")
        install_requires = list(f.read().splitlines())
        setup(use_scm_version={"version_scheme": "no-guess-dev"}, install_requires=install_requires)
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
