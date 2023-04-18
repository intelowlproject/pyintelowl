# PyIntelOwl

[![PyPI version](https://badge.fury.io/py/pyintelowl.svg)](https://badge.fury.io/py/pyintelowl)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/pyintelowl.svg)](https://pypi.python.org/pypi/pyintelowl/)

[![Pull request automation](https://github.com/intelowlproject/pyintelowl/actions/workflows/pull_request_automation.yml/badge.svg)](https://github.com/intelowlproject/pyintelowl/actions/workflows/pull_request_automation.yml)
[![codecov](https://codecov.io/gh/intelowlproject/pyintelowl/branch/master/graph/badge.svg?token=JF62UMZ0U6)](https://codecov.io/gh/intelowlproject/pyintelowl)
[![CodeFactor](https://www.codefactor.io/repository/github/intelowlproject/pyintelowl/badge)](https://www.codefactor.io/repository/github/intelowlproject/pyintelowl)

Robust Python **SDK** and **Command Line Client** for interacting with [IntelOwl](https://github.com/intelowlproject/IntelOwl)'s API.

## Features

- Easy one-time configuration with self documented help and hints along the way.
- Request new analysis for observables and files.
  - Select which analyzers you want to run for every analysis you perform.
  - Choose whether you want to HTTP poll for the analysis to finish or not.
- List all jobs or view one job in a prettified tabular form.
- List all tags or view one tag in a prettified tabular form.
- Tabular view of the `analyzer_config.json` and `connector_config.json` from IntelOwl with RegEx matching capabilities.

## Demo

[![pyintelowl asciicast](https://asciinema.org/a/z7L93lsIzOQ0Scve7hMl30mJJ.svg)](https://asciinema.org/a/z7L93lsIzOQ0Scve7hMl30mJJ?t=5)

## Installation

```bash
$ pip3 install pyintelowl
```

For development/testing, `pip3 install pyintelowl[dev]`

## Quickstart

### As Command Line Client

On successful installation, The `pyintelowl` entryscript should be directly invokable. For example,

```bash
$ pyintelowl
Usage: pyintelowl [OPTIONS] COMMAND [ARGS]...

Options:
  -d, --debug  Set log level to DEBUG
  --version    Show the version and exit.
  -h, --help   Show this message and exit.

Commands:
  analyse                Send new analysis request
  analyzer-healthcheck   Send healthcheck request for an analyzer...
  config                 Set or view config variables
  connector-healthcheck  Send healthcheck request for a connector
  get-analyzer-config    Get current state of `analyzer_config.json` from...
  get-connector-config   Get current state of `connector_config.json` from...
  jobs                   Manage Jobs
  tags                   Manage tags
```

### As a library / SDK

```python
from pyintelowl import IntelOwl
obj = IntelOwl("<your_api_key>", "<your_intelowl_instance_url>", "optional<path_to_pem_file>", "optional<proxies>")
```

For more comprehensive documentation, please see https://pyintelowl.readthedocs.io/.

## Changelog

View [CHANGELOG.md](https://github.com/intelowlproject/pyintelowl/blob/master/.github/CHANGELOG.md).

## FAQ

#### Generate API key

You need a valid API key to interact with the IntelOwl server.
Keys should be created from the admin interface of [IntelOwl](https://github.com/intelowlproject/intelowl): you have to go in the _Durin_ section (click on `Auth tokens`) and generate a key there.

#### Incompatibility after version 3.0

We did a complete rewrite of the PyIntelOwl client and CLI both for the version `3.0.0`. We very much recommend you to update to the latest version to enjoy all new features.

#### (old auth method) JWT Token Authentication

> this auth was available in IntelOwl versions <1.8.0 and pyintelowl versions <2.0.0

From the admin interface of IntelOwl, you have to go in the _Outstanding tokens_ section and generate a token there.

You can use it by pasting it into the file [api_token.txt](api_token.txt).
