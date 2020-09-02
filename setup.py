import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyintelowl",
    version="1.3.5",
    description="Client and Library for Intel Owl",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/intelowlproject/pyintelowl",
    author="Matteo Lodi",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pyintelowl"],
    python_requires="~=3.6",
    include_package_data=True,
    install_requires=["requests", "geocoder"],
)
