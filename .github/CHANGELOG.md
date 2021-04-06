# Changelog

## 3.1.1 (https://github.com/intelowlproject/pyintelowl/releases/tag/3.1.1)
* Added basic testing suite
* Removed deprecated ask_analysis_result function
* Little fix to a problem in the logs for the ones that use pyintelowl as a library

## 3.1.0 (https://github.com/intelowlproject/pyintelowl/releases/tag/3.1.0)
With this, pyintelowl now supports all API endpoints of IntelOwl. Super!!
More info at: https://github.com/intelowlproject/IntelOwl/releases/tag/v2.2.0

## 3.0.1 (https://github.com/intelowlproject/pyintelowl/releases/tag/3.0.1)
This release was created mainly to solve a problem with the installation of the pip package.

Other changes:
* added support for adding tags when requesting a new job
* added support for creating/editing tags
* added support for "generic" classification of observables

## 3.0.0 (https://github.com/intelowlproject/pyintelowl/releases/tag/3.0.0)

*Note: Incompatible with previous versions*

This version brings a complete rewrite of the pyintelowl library as well as command line client. We very much recommend you to update to the latest version to enjoy all new features.

- The new CLI is written with [pallets/click](https://github.com/pallets/click) and supports all IntelOwl API endpoints. The CLI is well-documented and will help you navigate different commands; you can use it to request new analysis, view an old analysis, view `analyzer_config.json`, view list of tags, list of jobs, etc.
- Complete type-hinting and sphinx docs for the `pyintelowl.IntelOwl` class with helper member functions for each IntelOwl API endpoint.


## 2.0.0 (https://github.com/intelowlproject/pyintelowl/releases/tag/2.0.0)
**This version supports only IntelOwl versions >=1.8.0 (about to be released). To interact with previous IntelOwl versions programmatically please refer to pyintelowl version 1.3.5**

* we forced [black](https://github.com/psf/black) style, added linters and precommit configuration. In this way pyintelowl is aligned to IntelOwl.
* we have updated the authentication method from a JWT Token to a simple Token. In this way, it is easier to use pyintelowl for integrations with other products and there are no more concurrency problems on multiple simultaneous requests.

If you were using pyintelowl and IntelOwl before this version, you have to:
* update IntelOwl to version>=1.8.0
* retrieve a new API token from the Django Admin Interface for your user: you have to go in the *Durin* section (click on `Auth tokens`) and generate a key there. This token is valid until manually deleted.


## 1.3.5 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.5)
Now optional parameter "runtime_configuration" properly works

Please use this version of pyintelowl with version >= 1.5.x of IntelOwl


## 1.3.4 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.4)
see [1.3.3](https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.3) for details


## 1.3.3 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.3)
Some fixes:

*   pyintelowl did not work correctly against HTTPS-enabled IntelOwl Servers
*    fixed parameter name in send_observable_analysis_request

Please use this version of pyintelowl with v1.5.x of IntelOwl


## 1.3.2 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.2)
Patch Release after [1.3.0](https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.0).

- renamed `additional_configuration` to `runtime_configuration`.
- Formatting with psf/black formatter.

**Please use this version of pyintelowl with v1.5.x of IntelOwl.**


## 1.3.1 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.1)
Fixes and improvements to "--show-colors" option


## 1.3.0 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.3.0)
reformatted some code + added support for new parameter "additional_configuration"


## 1.2.0 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.2.0)
PR #16 for details.


## 1.1.0 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.1.0)
Added an option when executing pyintelowl as CLI: `-sc` will show the results in a colorful and organized way that helps the user in looking for useful information. By default, the results are still shown in the JSON format. Thanks to tsale to his idea and contribution.

**Example:**

```
python3 intel_owl_client.py -i <your_intelowl_instance> -sc -a VirusTotal_v2_Get_Observable -a HybridAnalysis_Get_Observable -a OTXQuery observable -v www.google.com
```


## 1.0.0 (https://github.com/intelowlproject/pyintelowl/releases/tag/1.0.0)
For all the details, check the official blog post:

https://www.honeynet.org/2020/07/05/intel-owl-release-v1-0-0/

This version is compatible only with the related (1.x) IntelOwl release.

## 0.2.1

## 0.2.0

## 0.1.2

## 0.1.1

