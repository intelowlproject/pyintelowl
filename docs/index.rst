.. pyintelowl documentation master file, created by
   sphinx-quickstart on Sat Dec  5 23:00:08 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyIntelOwl's documentation!
======================================

Robust Python **SDK** and **Command Line Client** for interacting with `IntelOwl <https://github.com/intelowlproject/IntelOwl>`__ API.

Installation
--------------------------

.. code-block:: bash

   $ pip install pyintelowl


Usage as CLI
--------------------------

On successful installation, The ``pyintelowl`` entryscript should be directly invokable. For example,

.. code-block:: bash
  :emphasize-lines: 1

   $ pyintelowl
   Usage: pyintelowl [OPTIONS] COMMAND [ARGS]...

   Options:
   -d, --debug  Set log level to DEBUG
   --version    Show the version and exit.
   -h, --help   Show this message and exit.

   Commands:
   analyse              Send new analysis request
   config               Set or view config variables
   get-analyzer-config  Get current state of `analyzer_config.json` from the...
   get-connector-config  Get current state of `connector_config.json` from the...
   jobs                 Manage Jobs
   tags                 Manage tags

Configuration
^^^^^^^^^^^^^

You can use ``set`` to set the config variables and ``get`` to view them.

.. code-block:: bash
   :caption: `View on asciinema <https://asciinema.org/a/3y3nJeyWUoqQjUrCdXUAorlVW>`__

   $ pyintelowl config set -k 4bf03f20add626e7138f4023e4cf52b8 -u "http://localhost:80"
   $ pyintelowl config get

.. Hint::
   The CLI would is well-documented which will help you navigate various commands easily.
   Invoke ``pyintelowl -h`` or ``pyintelowl <command> -h`` to get help.


Usage as SDK/library
--------------------------

.. code-block:: python
  :linenos:

   from pyintelowl import IntelOwl, IntelOwlClientException
   obj = IntelOwl(
      "4bf03f20add626e7138f4023e4cf52b8",
      "http://localhost:80",
      None,
   )
   """
   obj = IntelOwl(
      "<your_api_key>",
      "<your_intelowl_instance_url>",
      "optional<path_to_pem_file>"
   )
   """

   try:
      ans = obj.get_analyzer_configs(1)
      print(ans)
   except IntelOwlClientException as e:
      print("Oh no! Error: ", e)

.. Tip:: We very much **recommend** going through the :class:`pyintelowl.pyintelowl.IntelOwl` docs.


API Client Docs
==================

.. toctree::
   :maxdepth: 3

   Index <index>
   pyintelowl
   tests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
