Tests
======================================

Configuration
--------------------------------------

Some tests require file samples, which can be found in the encrypted folder ``tests/test_files.zip`` (password: "infected").
Unzip the archive in ``tests/test_files`` folder before running the tests.

**Please remember that these are dangerous malware! They come encrypted and locked for a reason!
Do NOT run them unless you are absolutely sure of what you are doing!
They are to be used only for launching specific tests that require them** (``__send_analysis_request``)

* With the following constants in ``__init__.py``, you can customize your tests:

  * **MOCKING_CONNECTIONS:** Mock connections to external API to test functions without a real connection or a valid API Key.

* If you prefer to use custom inputs for tests, you can change the following constants:

  * **TEST_JOB_ID**
  * **TEST_HASH**
  * **TEST_URL**
  * **TEST_IP**
  * **TEST_DOMAIN**
  * **TEST_GENERIC**
  * **TEST_FILE**
  * **TEST_FILE_HASH**

Launch Tests
-------------------------------------

* The test requirements are specified in the ``test-requirements.txt`` file. Install them using,
  
.. code-block:: bash

    $ pip3 install -r test-requirements.txt

* Launch the tests using ``tox``:
  
.. code-block:: bash

    $ tox


