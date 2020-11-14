# PyIntelOwl

[![PyPI version](https://badge.fury.io/py/pyintelowl.svg)](https://badge.fury.io/py/pyintelowl)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/intelowlproject/pyintelowl.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mlodic/pyintelowl/context:python)
[![CodeFactor](https://www.codefactor.io/repository/github/intelowlproject/pyintelowl/badge)](https://www.codefactor.io/repository/github/intelowlproject/pyintelowl)

Robust Python **SDK** and **Command Line Client** for interacting with [IntelOwl](https://github.com/intelowlproject/IntelOwl)'s API.

You can select which analyzers you want to run for every analysis you perform.

For additional help, we suggest to check the ["How to use pyintelowl" Youtube Video](https://www.youtube.com/watch?v=fpd6Kt9EZdI) by [Kostas](https://github.com/tsale).


## Installation

```bash
$ pip3 install pyintelowl
```

For development/testing, `pip3 install pyintelowl[dev]`

## Usage

### As Command Line Client

```bash
$ python3 cli.py -h
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  -k, --api-key TEXT       API key to authenticate against a IntelOwl instance
                           [required]

  -u, --instance-url TEXT  IntelOwl instance URL  [required]
  -c, --certificate PATH   Path to SSL client certificate file (.pem)
  --debug / --no-debug     Set log level to DEBUG
  -h, --help               Show this message and exit.

Commands:
  analyse              Send new analysis request
  config               Set or view config variables
  get-analyzer-config  Get current state of analyzer_config.json from the IntelOwl instance
  jobs                 List jobs
  tags                 List tags
```

## As a library / SDK

`from pyintelowl.pyintelowl import IntelOwl`

#### Endpoints
`ask_analysis_availability` -> search for already available analysis

`send_file_analysis_request` -> send a file to be analyzed

`send_observable_analysis_request` -> send an observable to be analyzed

`ask_analysis_result` -> request analysis result by job ID

`get_analyzer_configs` -> get the analyzers configuration


## FAQ

### Generate API key
You need a valid API key to interact with the IntelOwl server. 
Keys should be created from the admin interface of [IntelOwl](https://github.com/intelowlproject/intelowl): you have to go in the *Durin* section (click on `Auth tokens`) and generate a key there.

You can use the  with the parameter `-k <api_key>` from CLI

#### (old auth method) JWT Token Authentication
> this auth was available in IntelOwl versions <1.8.0 and pyintelowl versions <2.0.0

From the admin interface of IntelOwl, you have to go in the *Outstanding tokens* section and generate a token there.

You can use it by pasting it into the file [api_token.txt](api_token.txt).