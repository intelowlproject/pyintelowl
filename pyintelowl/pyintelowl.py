import hashlib
import ipaddress
import json
import logging
import pathlib
import re
from typing import Any, AnyStr, Callable, Dict, List, Optional, Union

import requests
from typing_extensions import Literal

from pyintelowl.version import __version__

from .exceptions import IntelOwlClientException

TLPType = Literal["WHITE", "GREEN", "AMBER", "RED", "CLEAR"]


class IntelOwl:
    logger: logging.Logger

    def __init__(
        self,
        token: str,
        instance_url: str,
        certificate: str = None,
        proxies: dict = None,
        logger: logging.Logger = None,
        cli: bool = False,
    ):
        self.token = token
        self.instance = instance_url
        self.certificate = certificate
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
        if proxies and not isinstance(proxies, dict):
            raise TypeError("proxies param must be a dictionary")
        self.proxies = proxies
        self.cli = cli

    @property
    def session(self) -> requests.Session:
        """
        Internal use only.
        """
        if not hasattr(self, "_session"):
            session = requests.Session()
            if self.certificate is not True:
                session.verify = self.certificate
            if self.proxies:
                session.proxies = self.proxies
            session.headers.update(
                {
                    "Authorization": f"Token {self.token}",
                    "User-Agent": f"PyIntelOwl/{__version__}",
                }
            )
            self._session = session

        return self._session

    def __make_request(
        self,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET",
        *args,
        **kwargs,
    ) -> requests.Response:
        """
        For internal use only.
        """
        response: requests.Response = None
        requests_function_map: Dict[str, Callable] = {
            "GET": self.session.get,
            "POST": self.session.post,
            "PUT": self.session.put,
            "PATCH": self.session.patch,
            "DELETE": self.session.delete,
        }
        func = requests_function_map.get(method, None)
        if not func:
            raise RuntimeError(f"Unsupported method name: {method}")

        try:
            response = func(*args, **kwargs)
            self.logger.debug(
                msg=(response.url, response.status_code, response.content)
            )
            response.raise_for_status()
        except Exception as e:
            raise IntelOwlClientException(e, response=response)

        return response

    def ask_analysis_availability(
        self,
        md5: str,
        analyzers: List[str] = None,
        check_reported_analysis_too: bool = False,
        minutes_ago: int = None,
    ) -> Dict:
        """Search for already available analysis.\n
        Endpoint: ``/api/ask_analysis_availability``

        Args:
            md5 (str): md5sum of the observable or file
            analyzers (List[str], optional):
            list of analyzers to trigger.
            Defaults to `None` meaning automatically select all configured analyzers.
            check_reported_analysis_too (bool, optional):
            Check against all existing jobs. Defaults to ``False``.
            minutes_ago (int, optional):
            number of minutes to check back for analysis.
            Default is None so the check does not have any time limits.

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict: JSON body
        """
        if not analyzers:
            analyzers = []
        data = {"md5": md5, "analyzers": analyzers}
        if not check_reported_analysis_too:
            data["running_only"] = True
        if minutes_ago:
            data["minutes_ago"] = int(minutes_ago)
        url = self.instance + "/api/ask_analysis_availability"
        response = self.__make_request("POST", url=url, data=data)
        answer = response.json()
        status, job_id = answer.get("status", None), answer.get("job_id", None)
        # check sanity cases
        if not status:
            raise IntelOwlClientException(
                "API ask_analysis_availability gave result without status ?"
                f" Response: {answer}"
            )
        if status != "not_available" and not job_id:
            raise IntelOwlClientException(
                "API ask_analysis_availability gave result without job_id ?"
                f" Response: {answer}"
            )
        return answer

    def send_file_analysis_request(
        self,
        filename: str,
        binary: bytes,
        tlp: TLPType = "CLEAR",
        analyzers_requested: List[str] = None,
        connectors_requested: List[str] = None,
        runtime_configuration: Dict = None,
        tags_labels: List[str] = None,
    ) -> Dict:
        """Send analysis request for a file.\n
        Endpoint: ``/api/analyze_file``

        Args:

            filename (str):
                Filename
            binary (bytes):
                File contents as bytes
            analyzers_requested (List[str], optional):
                List of analyzers to invoke
                Defaults to ``[]`` i.e. all analyzers.
            connectors_requested (List[str], optional):
                List of specific connectors to invoke.
                Defaults to ``[]`` i.e. all connectors.
            tlp (str, optional):
                TLP for the analysis.
                (options: ``CLEAR, GREEN, AMBER, RED``).
            runtime_configuration (Dict, optional):
                Overwrite configuration for analyzers. Defaults to ``{}``.
            tags_labels (List[str], optional):
                List of tag labels to assign (creates non-existing tags)

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict: JSON body
        """
        try:
            if not tlp:
                tlp = "CLEAR"
            if not analyzers_requested:
                analyzers_requested = []
            if not connectors_requested:
                connectors_requested = []
            if not tags_labels:
                tags_labels = []
            if not runtime_configuration:
                runtime_configuration = {}
            data = {
                "file_name": filename,
                "analyzers_requested": analyzers_requested,
                "connectors_requested": connectors_requested,
                "tlp": tlp,
                "tags_labels": tags_labels,
            }
            if runtime_configuration:
                data["runtime_configuration"] = json.dumps(runtime_configuration)
            files = {"file": (filename, binary)}
            answer = self.__send_analysis_request(data=data, files=files)
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def send_file_analysis_playbook_request(
        self,
        filename: str,
        binary: bytes,
        playbook_requested: str,
        tlp: TLPType = "CLEAR",
        runtime_configuration: Dict = None,
        tags_labels: List[str] = None,
    ) -> Dict:
        """Send playbook analysis request for a file.\n
        Endpoint: ``/api/playbook/analyze_multiple_files``

        Args:

            filename (str):
                Filename
            binary (bytes):
                File contents as bytes
            playbook_requested (str, optional):
            tlp (str, optional):
                TLP for the analysis.
                (options: ``WHITE, GREEN, AMBER, RED``).
            runtime_configuration (Dict, optional):
                Overwrite configuration for analyzers. Defaults to ``{}``.
            tags_labels (List[str], optional):
                List of tag labels to assign (creates non-existing tags)

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict: JSON body
        """
        try:
            if not tags_labels:
                tags_labels = []
            if not runtime_configuration:
                runtime_configuration = {}
            data = {
                "playbook_requested": playbook_requested,
                "tags_labels": tags_labels,
            }
            # send this value only if populated,
            # otherwise the backend would give you 400
            if tlp:
                data["tlp"] = tlp

            if runtime_configuration:
                data["runtime_configuration"] = json.dumps(runtime_configuration)
            # `files` is wanted to be different from the other
            # /api/analyze_file endpoint
            # because the server is using different serializers
            files = {"files": (filename, binary)}
            answer = self.__send_analysis_request(
                data=data, files=files, playbook_mode=True
            )
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def send_observable_analysis_request(
        self,
        observable_name: str,
        tlp: TLPType = "CLEAR",
        analyzers_requested: List[str] = None,
        connectors_requested: List[str] = None,
        runtime_configuration: Dict = None,
        tags_labels: List[str] = None,
        observable_classification: str = None,
    ) -> Dict:
        """Send analysis request for an observable.\n
        Endpoint: ``/api/analyze_observable``

        Args:
            observable_name (str):
                Observable value
            analyzers_requested (List[str], optional):
                List of analyzers to invoke
                Defaults to ``[]`` i.e. all analyzers.
            connectors_requested (List[str], optional):
                List of specific connectors to invoke.
                Defaults to ``[]`` i.e. all connectors.
            tlp (str, optional):
                TLP for the analysis.
                (options: ``CLEAR, GREEN, AMBER, RED``).
            runtime_configuration (Dict, optional):
                Overwrite configuration for analyzers. Defaults to ``{}``.
            tags_labels (List[str], optional):
                List of tag labels to assign (creates non-existing tags)
            observable_classification (str):
                Observable classification, Default to None.
                By default launch analysis with an automatic classification.
                (options: ``url, domain, hash, ip, generic``)

        Raises:
            IntelOwlClientException: on client/HTTP error
            IntelOwlClientException: on wrong observable_classification

        Returns:
            Dict: JSON body
        """
        try:
            if not tlp:
                tlp = "CLEAR"
            if not analyzers_requested:
                analyzers_requested = []
            if not connectors_requested:
                connectors_requested = []
            if not tags_labels:
                tags_labels = []
            if not runtime_configuration:
                runtime_configuration = {}
            if not observable_classification:
                observable_classification = self._get_observable_classification(
                    observable_name
                )
            elif observable_classification not in [
                "generic",
                "hash",
                "ip",
                "domain",
                "url",
            ]:
                raise IntelOwlClientException(
                    "Observable classification only handle"
                    " 'generic', 'hash', 'ip', 'domain' and 'url' "
                )
            data = {
                "observable_name": observable_name,
                "observable_classification": observable_classification,
                "analyzers_requested": analyzers_requested,
                "connectors_requested": connectors_requested,
                "tlp": tlp,
                "tags_labels": tags_labels,
                "runtime_configuration": runtime_configuration,
            }
            answer = self.__send_analysis_request(data=data, files=None)
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def send_observable_analysis_playbook_request(
        self,
        observable_name: str,
        playbook_requested: str,
        tlp: TLPType = "CLEAR",
        runtime_configuration: Dict = None,
        tags_labels: List[str] = None,
        observable_classification: str = None,
    ) -> Dict:
        """Send playbook analysis request for an observable.\n
        Endpoint: ``/api/playbook/analyze_multiple_observables``

        Args:
            observable_name (str):
                Observable value
            playbook_requested str:
            tlp (str, optional):
                TLP for the analysis.
                (options: ``WHITE, GREEN, AMBER, RED``).
            runtime_configuration (Dict, optional):
                Overwrite configuration for analyzers. Defaults to ``{}``.
            tags_labels (List[str], optional):
                List of tag labels to assign (creates non-existing tags)
            observable_classification (str):
                Observable classification, Default to None.
                By default launch analysis with an automatic classification.
                (options: ``url, domain, hash, ip, generic``)

        Raises:
            IntelOwlClientException: on client/HTTP error
            IntelOwlClientException: on wrong observable_classification

        Returns:
            Dict: JSON body
        """
        try:
            if not tags_labels:
                tags_labels = []
            if not runtime_configuration:
                runtime_configuration = {}
            if not observable_classification:
                observable_classification = self._get_observable_classification(
                    observable_name
                )
            elif observable_classification not in [
                "generic",
                "hash",
                "ip",
                "domain",
                "url",
            ]:
                raise IntelOwlClientException(
                    "Observable classification only handle"
                    " 'generic', 'hash', 'ip', 'domain' and 'url' "
                )
            data = {
                "observables": [[observable_classification, observable_name]],
                "playbook_requested": playbook_requested,
                "tags_labels": tags_labels,
                "runtime_configuration": runtime_configuration,
            }
            # send this value only if populated,
            # otherwise the backend would give you 400
            if tlp:
                data["tlp"] = tlp
            answer = self.__send_analysis_request(
                data=data, files=None, playbook_mode=True
            )
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def send_analysis_batch(self, rows: List[Dict]):
        """
        Send multiple analysis requests.
        Can be mix of observable or file analysis requests.

        Used by the pyintelowl CLI.

        Args:
            rows (List[Dict]):
                Each row should be a dictionary with keys,
                `value`, `type`, `check`, `tlp`,
                `analyzers_list`, `connectors_list`, `runtime_config`
                `tags_list`.
        """
        for obj in rows:
            try:
                runtime_config = obj.get("runtime_config", {})
                if runtime_config:
                    with open(runtime_config) as fp:
                        runtime_config = json.load(fp)

                analyzers_list = obj.get("analyzers_list", [])
                connectors_list = obj.get("connectors_list", [])
                if isinstance(analyzers_list, str):
                    analyzers_list = analyzers_list.split(",")
                if isinstance(connectors_list, str):
                    connectors_list = connectors_list.split(",")

                self._new_analysis_cli(
                    obj["value"],
                    obj["type"],
                    obj.get("check", None),
                    obj.get("tlp", "WHITE"),
                    analyzers_list,
                    connectors_list,
                    runtime_config,
                    obj.get("tags_list", []),
                    obj.get("should_poll", False),
                )
            except IntelOwlClientException as e:
                self.logger.fatal(str(e))

    def __send_analysis_request(self, data=None, files=None, playbook_mode=False):
        """
        Internal use only.
        """
        response = None
        answer = {}
        if files is None:
            url = self.instance + "/api/analyze_observable"
            if playbook_mode:
                url = self.instance + "/api/playbook/analyze_multiple_observables"
            args = {"json": data}
        else:
            url = self.instance + "/api/analyze_file"
            if playbook_mode:
                url = self.instance + "/api/playbook/analyze_multiple_files"
            args = {"data": data, "files": files}
        try:
            response = self.session.post(url, **args)
            self.logger.debug(
                msg={
                    "url": response.url,
                    "code": response.status_code,
                    "request": response.request.headers,
                    "headers": response.headers,
                    "body": response.json(),
                }
            )
            answer = response.json()
            if playbook_mode:
                # right now, we are only supporting single input result
                answers = answer.get("results", [])
                if answers:
                    answer = answers[0]

            warnings = answer.get("warnings", [])
            errors = answer.get("errors", {})
            if self.cli:
                info_log = f"""New Job running..
                    ID: {answer.get('job_id')} | 
                    Status: [u blue]{answer.get('status')}[/].
                    Got {len(warnings)} warnings:
                    [i yellow]{warnings if warnings else None}[/]
                    Got {len(errors)} errors:
                    [i red]{errors if errors else None}[/]
                """
            else:
                info_log = (
                    f"New Job running.. ID: {answer.get('job_id')} "
                    f"| Status: {answer.get('status')}."
                    f" Got {len(warnings)} warnings:"
                    f" {warnings if warnings else None}"
                    f" Got {len(errors)} errors:"
                    f" {errors if errors else None}"
                )
            self.logger.info(info_log)
            response.raise_for_status()
        except Exception as e:
            raise IntelOwlClientException(e, response=response)
        return answer

    def create_tag(self, label: str, color: str):
        """Creates new tag by sending a POST Request
        Endpoint: ``/api/tags``

        Args:
            label ([str]): [Label of the tag to be created]
            color ([str]): [Color of the tag to be created]
        """
        url = self.instance + "/api/tags"
        data = {"label": label, "color": color}
        response = self.__make_request("POST", url=url, data=data)
        return response.json()

    def edit_tag(self, tag_id: Union[int, str], label: str, color: str):
        """Edits existing tag by sending PUT request
        Endpoint: ``api/tags``

        Args:
            id ([int]): [Id of the existing tag]
            label ([str]): [Label of the tag to be created]
            color ([str]): [Color of the tag to be created]
        """
        url = self.instance + "/api/tags/" + str(tag_id)
        data = {"label": label, "color": color}
        response = self.__make_request("PUT", url=url, data=data)
        return response.json()

    def get_analyzer_configs(self):
        """
        Get current state of `analyzer_config.json` from the IntelOwl instance.\n
        Endpoint: ``/api/get_analyzer_configs``
        """
        url = self.instance + "/api/get_analyzer_configs"
        response = self.__make_request("GET", url=url)
        return response.json()

    def get_connector_configs(self):
        """
        Get current state of `connector_config.json` from the IntelOwl instance.\n
        Endpoint: ``/api/get_connector_configs``
        """
        url = self.instance + "/api/get_connector_configs"
        response = self.__make_request("GET", url=url)
        return response.json()

    def get_playbook_configs(self):
        """
        Get current state of `playbook_config.json` from the IntelOwl instance.\n
        Endpoint: ``/api/get_playbook_configs``
        """
        url = self.instance + "/api/get_playbook_configs"
        response = self.__make_request("GET", url=url)
        return response.json()

    def get_all_tags(self) -> List[Dict[str, str]]:
        """
        Fetch list of all tags.\n
        Endpoint: ``/api/tags``

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            List[Dict[str, str]]: List of tags
        """
        url = self.instance + "/api/tags"
        response = self.__make_request("GET", url=url)
        return response.json()

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """
        Fetch list of all jobs.\n
        Endpoint: ``/api/jobs``

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict: Dict with 3 keys: "count", "total_pages", "results"
        """
        url = self.instance + "/api/jobs"
        response = self.__make_request("GET", url=url)
        return response.json()

    def get_tag_by_id(self, tag_id: Union[int, str]) -> Dict[str, str]:
        """Fetch tag info by ID.\n
        Endpoint: ``/api/tag/{tag_id}``

        Args:
            tag_id (Union[int, str]): Tag ID

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict[str, str]: Dict with 3 keys: `id`, `label` and `color`.
        """

        url = self.instance + "/api/tags/" + str(tag_id)
        response = self.__make_request("GET", url=url)
        return response.json()

    def get_job_by_id(self, job_id: Union[int, str]) -> Dict[str, Any]:
        """Fetch job info by ID.
        Endpoint: ``/api/jobs/{job_id}``

        Args:
            job_id (Union[int, str]): Job ID

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict[str, Any]: JSON body.
        """
        url = self.instance + "/api/jobs/" + str(job_id)
        response = self.__make_request("GET", url=url)
        return response.json()

    @staticmethod
    def get_md5(
        to_hash: AnyStr,
        type_="observable",
    ) -> str:
        """Returns md5sum of given observable or file object.

        Args:
            to_hash (AnyStr):
                either an observable string, file contents as bytes or path to a file
            type_ (Union["observable", "binary", "file"], optional):
                `observable`, `binary`, `file`. Defaults to "observable".

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            str: md5sum
        """
        md5 = ""
        if type_ == "observable":
            md5 = hashlib.md5(str(to_hash).lower().encode("utf-8")).hexdigest()
        elif type_ == "binary":
            md5 = hashlib.md5(to_hash).hexdigest()
        elif type_ == "file":
            path = pathlib.Path(to_hash)
            if not path.exists():
                raise IntelOwlClientException(f"{to_hash} does not exists")
            binary = path.read_bytes()
            md5 = hashlib.md5(binary).hexdigest()
        return md5

    def _new_analysis_cli(
        self,
        obj: str,
        type_: str,
        check,
        tlp: TLPType = None,
        analyzers_list: List[str] = None,
        connectors_list: List[str] = None,
        runtime_configuration: Dict = None,
        tags_labels: List[str] = None,
        should_poll: bool = False,
        minutes_ago: int = None,
    ) -> None:
        """
        For internal use by the pyintelowl CLI.
        """
        if not analyzers_list:
            analyzers_list = []
        if not connectors_list:
            connectors_list = []
        if not runtime_configuration:
            runtime_configuration = {}
        if not tags_labels:
            tags_labels = []
        self.logger.info(
            f"""Requesting analysis..
            {type_}: [blue]{obj}[/]
            analyzers: [i green]{analyzers_list if analyzers_list else 'all'}[/]
            connectors: [i green]{connectors_list if connectors_list else 'all'}[/]
            tags: [i green]{tags_labels}[/]
            """
        )
        # 1st step: ask analysis availability
        if check != "force-new":
            md5 = self.get_md5(obj, type_=type_)

            resp = self.ask_analysis_availability(
                md5,
                analyzers_list,
                True if check == "reported" else False,
                minutes_ago,
            )
            status, job_id = resp.get("status", None), resp.get("job_id", None)
            if status != "not_available":
                self.logger.info(
                    f"""Found existing analysis!
                Job: #{job_id}
                status: [u blue]{status}[/]

                [i]Hint: use [#854442]--check force-new[/] to perform new scan anyway[/]
                    """
                )
                return
        # 2nd step: send new analysis request
        if type_ == "observable":
            resp2 = self.send_observable_analysis_request(
                observable_name=obj,
                tlp=tlp,
                analyzers_requested=analyzers_list,
                connectors_requested=connectors_list,
                runtime_configuration=runtime_configuration,
                tags_labels=tags_labels,
            )
        else:
            path = pathlib.Path(obj)
            resp2 = self.send_file_analysis_request(
                filename=path.name,
                binary=path.read_bytes(),
                tlp=tlp,
                analyzers_requested=analyzers_list,
                connectors_requested=connectors_list,
                runtime_configuration=runtime_configuration,
                tags_labels=tags_labels,
            )
        # 3rd step: poll for result
        if should_poll:
            if resp2["status"] != "accepted":
                self.logger.fatal("Can't poll a failed job")
            # import poll function
            from .cli._jobs_utils import _poll_for_job_cli

            job_id = resp2["job_id"]
            _ = _poll_for_job_cli(self, job_id)
            self.logger.info(
                f"""
        Polling finished.
        Execute [i blue]pyintelowl jobs view {job_id}[/] to view the result
                """
            )

    def _new_analysis_playbook_cli(
        self,
        obj: str,
        type_: str,
        playbook: str,
        tlp: TLPType = None,
        runtime_configuration: Dict = None,
        tags_labels: List[str] = None,
        should_poll: bool = False,
    ) -> None:
        """
        For internal use by the pyintelowl CLI.
        """
        if not runtime_configuration:
            runtime_configuration = {}
        if not tags_labels:
            tags_labels = []

        self.logger.info(
            f"""Requesting analysis..
            {type_}: [blue]{obj}[/]
            playbook: [i green]{playbook}[/]
            tags: [i green]{tags_labels}[/]
            """
        )

        # 1st step, make request
        if type_ == "observable":
            resp = self.send_observable_analysis_playbook_request(
                observable_name=obj,
                playbook_requested=playbook,
                tlp=tlp,
                runtime_configuration=runtime_configuration,
                tags_labels=tags_labels,
            )
        else:
            path = pathlib.Path(obj)
            resp = self.send_file_analysis_playbook_request(
                filename=path.name,
                binary=path.read_bytes(),
                playbook_requested=playbook,
                tlp=tlp,
                runtime_configuration=runtime_configuration,
                tags_labels=tags_labels,
            )

        # 2nd step: poll for result
        if should_poll:
            if resp.get("status", "") != "accepted":
                self.logger.fatal("Can't poll a failed job")
            # import poll function
            from .cli._jobs_utils import _poll_for_job_cli

            job_id = resp.get("job_id", 0)
            _ = _poll_for_job_cli(self, job_id)
            self.logger.info(
                f"""
                    Polling finished.
                    Execute [i blue]pyintelowl jobs view {job_id}[/] to view the result
                """
            )

    def _get_observable_classification(self, value: str) -> str:
        """Returns observable classification for the given value.\n
        Only following types are supported:
        ip, domain, url, hash (md5, sha1, sha256), generic (if no match)

        Args:
            value (str):
                observable value

        Raises:
            IntelOwlClientException:
                if value type is not recognized

        Returns:
            str: one of `ip`, `url`, `domain`, `hash` or 'generic'.
        """
        try:
            ipaddress.ip_address(value)
        except ValueError:
            if re.match(
                r"^(?:htt|ft|tc)ps?://[a-z\d-]{1,63}(?:\.[a-z\d-]{1,63})+"
                r"(?:/[a-z\d-]{1,63})*(?:\.\w+)?",
                value,
            ):
                classification = "url"
            elif re.match(r"^(\.)?[a-z\d-]{1,63}(\.[a-z\d-]{1,63})+$", value):
                classification = "domain"
            elif (
                re.match(r"^[a-f\d]{32}$", value)
                or re.match(r"^[a-f\d]{40}$", value)
                or re.match(r"^[a-f\d]{64}$", value)
                or re.match(r"^[A-F\d]{32}$", value)
                or re.match(r"^[A-F\d]{40}$", value)
                or re.match(r"^[A-F\d]{64}$", value)
            ):
                classification = "hash"
            else:
                classification = "generic"
                self.logger.warning(
                    "Couldn't detect observable classification, setting as 'generic'..."
                )
        else:
            # its a simple IP
            classification = "ip"

        return classification

    def download_sample(self, job_id: int) -> bytes:
        """
        Download file sample from job.\n
        Method: GET
        Endpoint: ``/api/jobs/{job_id}/download_sample``

        Args:
            job_id (int):
                id of job to download sample from

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bytes: Raw file data.
        """

        url = self.instance + f"/api/jobs/{job_id}/download_sample"
        response = self.__make_request("GET", url=url)
        return response.content

    def kill_running_job(self, job_id: int) -> bool:
        """Send kill_running_job request.\n
        Method: PATCH
        Endpoint: ``/api/jobs/{job_id}/kill``

        Args:
            job_id (int):
                id of job to kill

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: killed or not
        """

        url = self.instance + f"/api/jobs/{job_id}/kill"
        response = self.__make_request("PATCH", url=url)
        killed = response.status_code == 204
        return killed

    def delete_job_by_id(self, job_id: int) -> bool:
        """Send delete job request.\n
        Method: DELETE
        Endpoint: ``/api/jobs/{job_id}``

        Args:
            job_id (int):
                id of job to kill

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: deleted or not
        """
        url = self.instance + "/api/jobs/" + str(job_id)
        response = self.__make_request("DELETE", url=url)
        deleted = response.status_code == 204
        return deleted

    def delete_tag_by_id(self, tag_id: int) -> bool:
        """Send delete tag request.\n
        Method: DELETE
        Endpoint: ``/api/tags/{tag_id}``

        Args:
            tag_id (int):
                id of tag to delete

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: deleted or not
        """

        url = self.instance + "/api/tags/" + str(tag_id)
        response = self.__make_request("DELETE", url=url)
        deleted = response.status_code == 204
        return deleted

    def __run_plugin_action(
        self, job_id: int, plugin_type: str, plugin_name: str, plugin_action: str
    ) -> bool:
        """Internal method for kill/retry for analyzer/connector"""
        response = None
        url = (
            self.instance
            + f"/api/jobs/{job_id}/{plugin_type}/{plugin_name}/{plugin_action}"
        )
        response = self.__make_request("PATCH", url=url)
        success = response.status_code == 204
        return success

    def kill_analyzer(self, job_id: int, analyzer_name: str) -> bool:
        """Send kill running/pending analyzer request.\n
        Method: PATCH
        Endpoint: ``/api/jobs/{job_id}/analyzer/{analyzer_name}/kill``

        Args:
            job_id (int):
                id of job
            analyzer_name (str):
                name of analyzer to kill

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: killed or not
        """

        killed = self.__run_plugin_action(
            job_id=job_id,
            plugin_name=analyzer_name,
            plugin_type="analyzer",
            plugin_action="kill",
        )
        return killed

    def kill_connector(self, job_id: int, connector_name: str) -> bool:
        """Send kill running/pending connector request.\n
        Method: PATCH
        Endpoint: ``/api/jobs/{job_id}/connector/{connector_name}/kill``

        Args:
            job_id (int):
                id of job
            connector_name (str):
                name of connector to kill

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: killed or not
        """

        killed = self.__run_plugin_action(
            job_id=job_id,
            plugin_name=connector_name,
            plugin_type="connector",
            plugin_action="kill",
        )
        return killed

    def retry_analyzer(self, job_id: int, analyzer_name: str) -> bool:
        """Send retry failed/killed analyzer request.\n
        Method: PATCH
        Endpoint: ``/api/jobs/{job_id}/analyzer/{analyzer_name}/retry``

        Args:
            job_id (int):
                id of job
            analyzer_name (str):
                name of analyzer to retry

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: success or not
        """

        success = self.__run_plugin_action(
            job_id=job_id,
            plugin_name=analyzer_name,
            plugin_type="analyzer",
            plugin_action="retry",
        )
        return success

    def retry_connector(self, job_id: int, connector_name: str) -> bool:
        """Send retry failed/killed connector request.\n
        Method: PATCH
        Endpoint: ``/api/jobs/{job_id}/connector/{connector_name}/retry``

        Args:
            job_id (int):
                id of job
            connector_name (str):
                name of connector to retry

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: success or not
        """

        success = self.__run_plugin_action(
            job_id=job_id,
            plugin_name=connector_name,
            plugin_type="connector",
            plugin_action="retry",
        )
        return success

    def analyzer_healthcheck(self, analyzer_name: str) -> Optional[bool]:
        """Send analyzer(docker-based) health check request.\n
        Method: GET
        Endpoint: ``/api/analyzer/{analyzer_name}/healthcheck``

        Args:
            analyzer_name (str):
                name of analyzer

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: success or not
        """

        url = self.instance + f"/api/analyzer/{analyzer_name}/healthcheck"
        response = self.__make_request("GET", url=url)
        return response.json().get("status", None)

    def connector_healthcheck(self, connector_name: str) -> Optional[bool]:
        """Send connector health check request.\n
        Method: GET
        Endpoint: ``/api/connector/{connector_name}/healthcheck``

        Args:
            connector_name (str):
                name of connector

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Bool: success or not
        """
        url = self.instance + f"/api/connector/{connector_name}/healthcheck"
        response = self.__make_request("GET", url=url)
        return response.json().get("status", None)
