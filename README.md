# pyintelowl

Simple Client for Intel Owl Project

2 ways to use it:
* as a library
* as a command line script

### Library
`pip3 install pyintelowl`

`from pyintelowl.pyintelowl import IntelOwl`


### Command line Client
2 Submodules: `file` and `observable`

##### Sample
Example:
`python3 intel_owl_client.py -k <api_key> -i <url> -a PE_Info -a File_Info file -f <path_to_file>`

##### Observable
Example:
`python3 intel_owl_client.py -k <api_key> -i <url> -a AbuseIPDB -a OTXQuery observable -v google.com`