"""
# PyIntelOwl
Robust Python SDK and CLI for interacting with IntelOwl's API.
## Docs & Example Usage: https://github.com/intelowlproject/pyintelowl
"""

import os
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

with open(os.path.join("pyintelowl", "version.py"), "r") as f:
    exec(f.read())

GITHUB_URL = "https://github.com/intelowlproject/pyintelowl"

requirements = [
    "requests==2.25.1",
    "geocoder==1.38.1",
    "click==7.1.2",
    "rich==9.13.0",
    "click-creds==0.0.1",
]

requirements_test = [
    "black==20.8b1",
    "flake8==3.9.1",
    "pre-commit==2.12.1",
    "tox==3.23.0",
    "tox-gh-actions==2.5.0",
]

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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
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
