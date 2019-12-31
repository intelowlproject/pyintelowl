# pyintelowl

Simple Client for the [Intel Owl Project](https://github.com/mlodic/intel_owl)

2 ways to use it:
* as a library
* as a command line script

You can select which analyzers you want to run for every analysis you perform.

### Library
`pip3 install pyintelowl`

`from pyintelowl.pyintelowl import IntelOwl`

#### Endpoints
`ask_analysis_availability` -> search for already available analysis

`send_file_analysis_request` -> send a file to be analyzed

`send_observable_analysis_request` -> send an observable to be analyzed

`ask_analysis_result` -> request analysis result by job ID


### Command line Client
2 Submodules: `file` and `observable`

#### Sample
Example:
`python3 intel_owl_client.py -k <api_key> -i <url> -a PE_Info -a File_Info file -f <path_to_file>`

#### Observable
Example:
`python3 intel_owl_client.py -k <api_key> -i <url> -a AbuseIPDB -a OTXQuery observable -v google.com`