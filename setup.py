"""
# PyIntelOwl
Robust Python SDK and CLI for interacting with IntelOwl's API.
## Docs & Example Usage: https://github.com/intelowlproject/pyintelowl
"""

import os
import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

with open(os.path.join("pyintelowl", "version.py"), "r") as f:
    exec(f.read())

GITHUB_URL = "https://github.com/intelowlproject/pyintelowl"

# Get requirements from files
requirements = (HERE / "requirements.txt").read_text().split("\n")
requirements_test = (HERE / "test-requirements.txt").read_text().split("\n")

# This call to setup() does all the work
setup(
    name="pyintelowl",
    version=__version__,
    description="Robust Python SDK and CLI for IntelOwl's API",
    long_description=README,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    author="Matteo Lodi",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=requirements,
    project_urls={
        "Documentation": GITHUB_URL,
        "Funding": "https://liberapay.com/IntelOwlProject/",
        "Source": GITHUB_URL,
        "Tracker": "{}/issues".format(GITHUB_URL),
    },
    keywords="intelowl sdk python command line osint threat intel malware",
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": requirements_test + requirements,
        "test": requirements_test + requirements,
    },
    # pip install --editable .
    entry_points="""
        [console_scripts]
        pyintelowl=pyintelowl.main:cli
    """,
)
