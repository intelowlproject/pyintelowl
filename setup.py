"""
# PyIntelOwl
Robust Python SDK and CLI for interacting with IntelOwl's API.
## Docs & Example Usage: https://github.com/intelowlproject/pyintelowl
"""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

GITHUB_URL = "https://github.com/intelowlproject/pyintelowl"

requirements = [
    "requests==2.25.0",
    "geocoder==1.38.1",
    "click==7.1.2",
    "rich==9.2.0",
    "click-spinner==0.1.10",
]

# This call to setup() does all the work
setup(
    name="pyintelowl",
    version="3.0.0",
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["pyintelowl"],
    python_requires="~=3.6",
    include_package_data=True,
    install_requires=requirements,
    project_urls={
        "Documentation": "https://django-rest-durin.readthedocs.io/",
        "Funding": "https://liberapay.com/IntelOwlProject/",
        "Source": GITHUB_URL,
        "Tracker": "{}/issues".format(GITHUB_URL),
    },
    keywords="intelowl sdk python command line osint threat intel",
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": ["black==20.8b1", "flake8"] + requirements,
        "test": ["black==20.8b1", "flake8"] + requirements,
    },
)
