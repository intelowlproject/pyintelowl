import ipaddress
import logging
import pathlib
import json
import re
import requests
import hashlib
from typing import List, Dict, Any, Union, AnyStr

from .exceptions import IntelOwlClientException


class IntelOwl:
    logger: logging.Logger

    def __init__(
        self,
        token: str,
        instance_url: str,
        certificate: str = None,
        logger: logging.Logger = None,
        cli: bool = False,
    ):
        self.token = token
        self.instance = instance_url
        self.certificate = certificate
        self.cli = cli
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

    @property
    def session(self) -> requests.Session:
        """
        Internal use only.
        """
        if not hasattr(self, "_session"):
            session = requests.Session()
            if self.certificate is not True:
                session.verify = self.certificate
            session.headers.update(
                {
                    "Authorization": f"Token {self.token}",
                    "User-Agent": "IntelOwlClient/3.1.3",
                }
            )
            self._session = session

        return self._session

    def ask_analysis_availability(
        self,
        md5: str,
        analyzers_needed: List[str],
        run_all_available_analyzers: bool = False,
        check_reported_analysis_too: bool = False,
    ) -> Dict:
        """Search for already available analysis.\n
        Endpoint: ``/api/ask_analysis_availability``

        Args:
            md5 (str): md5sum of the observable or file
            analyzers_needed (List[str]): list of analyzers to invoke
            run_all_available_analyzers (bool, optional):
            If True, runs all compatible analyzers. Defaults to ``False``.
            check_reported_analysis_too (bool, optional):
            Check against all existing jobs. Defaults to ``False``.

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict: JSON body
        """
        try:
            params = {"md5": md5, "analyzers_needed": analyzers_needed}
            if run_all_available_analyzers:
                params["run_all_available_analyzers"] = True
            if not check_reported_analysis_too:
                params["running_only"] = True
            url = self.instance + "/api/ask_analysis_availability"
            response = self.session.get(url, params=params)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
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
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def send_file_analysis_request(
        self,
        analyzers_requested: List[str],
        filename: str,
        binary: bytes,
        force_privacy: bool = False,
        private_job: bool = False,
        disable_external_analyzers: bool = False,
        run_all_available_analyzers: bool = False,
        runtime_configuration: Dict = None,
        tags: List[int] = None,
    ) -> Dict:
        """Send analysis request for a file.\n
        Endpoint: ``/api/send_analysis_request``

        Args:
            analyzers_requested (List[str]):
                List of analyzers to invoke
            filename (str):
                Filename
            binary (bytes):
                File contents as bytes
            force_privacy (bool, optional):
                Disable analyzers that can leak info. Defaults to ``False``.
            private_job (bool, optional):
                Limit view permissions to your groups . Defaults to ``False``.
            disable_external_analyzers (bool, optional):
                Disable analyzers that use external services. Defaults to ``False``.
            tags (List[int]):
                List of tags associated with this job
            run_all_available_analyzers (bool, optional):
                If True, runs all compatible analyzers. Defaults to ``False``.
            runtime_configuration (Dict, optional):
                Overwrite configuration for analyzers. Defaults to ``{}``.

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict: JSON body
        """
        try:
            if not tags:
                tags = []
            if not runtime_configuration:
                runtime_configuration = {}
            data = {
                "is_sample": True,
                "md5": self.get_md5(binary, type_="binary"),
                "analyzers_requested": analyzers_requested,
                "tags_id": tags,
                "run_all_available_analyzers": run_all_available_analyzers,
                "force_privacy": force_privacy,
                "private": private_job,
                "disable_external_analyzers": disable_external_analyzers,
                "file_name": filename,
            }
            if runtime_configuration:
                data["runtime_configuration"] = json.dumps(runtime_configuration)
            files = {"file": (filename, binary)}
            answer = self.__send_analysis_request(data=data, files=files)
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def send_observable_analysis_request(
        self,
        analyzers_requested: List[str],
        observable_name: str,
        force_privacy: bool = False,
        private_job: bool = False,
        disable_external_analyzers: bool = False,
        run_all_available_analyzers: bool = False,
        runtime_configuration: Dict = None,
        tags: List[int] = None,
    ) -> Dict:
        """Send analysis request for an observable.\n
        Endpoint: ``/api/send_analysis_request``

        Args:
            analyzers_requested (List[str]):
                List of analyzers to invoke
            observable_name (str):
                Observable value
            force_privacy (bool, optional):
                Disable analyzers that can leak info. Defaults to ``False``.
            private_job (bool, optional):
                Limit view permissions to your groups . Defaults to ``False``.
            disable_external_analyzers (bool, optional):
                Disable analyzers that use external services. Defaults to ``False``.
            tags (List[int]):
                List of tags associated with this job
            run_all_available_analyzers (bool, optional):
                If True, runs all compatible analyzers. Defaults to ``False``.
            runtime_configuration (Dict, optional):
                Overwrite configuration for analyzers. Defaults to ``{}``.

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict: JSON body
        """
        try:
            if not tags:
                tags = []
            if not runtime_configuration:
                runtime_configuration = {}
            data = {
                "is_sample": False,
                "md5": self.get_md5(observable_name, type_="observable"),
                "analyzers_requested": analyzers_requested,
                "tags_id": tags,
                "run_all_available_analyzers": run_all_available_analyzers,
                "force_privacy": force_privacy,
                "private": private_job,
                "disable_external_analyzers": disable_external_analyzers,
                "observable_name": observable_name,
                "observable_classification": self._get_observable_classification(
                    observable_name
                ),
            }
            if runtime_configuration:
                data["runtime_configuration"] = json.dumps(runtime_configuration)
            answer = self.__send_analysis_request(data=data, files=None)
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
                `value`, `type`, `analyzers_list`, `run_all`
                `force_privacy`, `private_job`, `disable_external_analyzers`,
                `check`.
        """
        for obj in rows:
            try:
                runtime_config = obj.get("runtime_config", {})
                if runtime_config:
                    with open(runtime_config) as fp:
                        runtime_config = json.load(fp)

                if not (obj.get("run_all", False)):
                    obj["analyzers_list"] = obj["analyzers_list"].split(",")

                self._new_analysis_cli(
                    obj["value"],
                    obj["type"],
                    obj.get("analyzers_list", None),
                    obj.get("run_all", False),
                    obj.get("force_privacy", False),
                    obj.get("private_job", False),
                    obj.get("disable_external_analyzers", False),
                    obj.get("check", None),
                    runtime_config,
                )
            except IntelOwlClientException as e:
                self.logger.fatal(str(e))

    def __send_analysis_request(self, data=None, files=None):
        """
        Internal use only.
        """
        url = self.instance + "/api/send_analysis_request"
        response = self.session.post(url, data=data, files=files)
        self.logger.debug(
            msg={
                "url": response.url,
                "code": response.status_code,
                "headers": response.headers,
                "body": response.json(),
            }
        )
        answer = response.json()
        if answer.get("error", "") == "814":
            if self.cli:
                err = """
                    Request failed..
                    Error: [i yellow]After the filter, no analyzers can be run.
                        Try with other analyzers.[/]
                    """
            else:
                err = "Request failed. After the filter, no analyzers can be run"
            raise IntelOwlClientException(err)
        warnings = answer.get("warnings", [])
        if self.cli:
            info_log = f"""New Job running..
                ID: {answer['job_id']} | Status: [u blue]{answer['status']}[/].
                Got {len(warnings)} warnings:
                [i yellow]{warnings if warnings else None}[/]
            """
        else:
            info_log = f"""New Job running..
                ID: {answer['job_id']} | Status: {answer['status']}.
                Got {len(warnings)} warnings:
                {warnings if warnings else None}
            """
        self.logger.info(info_log)
        response.raise_for_status()
        return answer

    def create_tag(self, label: str, color: str):
        """Creates new tag by sending a POST Request
        Endpoint: ``/api/tags``

        Args:
            label ([str]): [Label of the tag to be created]
            color ([str]): [Color of the tag to be created]
        """
        try:
            url = self.instance + "/api/tags"
            data = {"label": label, "color": color}
            response = self.session.post(url, data=data)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def edit_tag(self, tag_id: Union[int, str], label: str, color: str):
        """Edits existing tag by sending PUT request
        Endpoint: ``api/tags``

        Args:
            id ([int]): [Id of the existing tag]
            label ([str]): [Label of the tag to be created]
            color ([str]): [Color of the tag to be created]
        """
        try:
            url = self.instance + "/api/tags/" + str(tag_id)
            data = {"label": label, "color": color}
            response = self.session.put(url, data=data)
            self.logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_analyzer_configs(self):
        """
        Get current state of `analyzer_config.json` from the IntelOwl instance.\n
        Endpoint: ``/api/get_analyzer_configs``
        """
        try:
            url = self.instance + "/api/get_analyzer_configs"
            response = self.session.get(url)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_all_tags(self) -> List[Dict[str, str]]:
        """
        Fetch list of all tags.\n
        Endpoint: ``/api/tags``

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            List[Dict[str, str]]: List of tags
        """
        answer = None
        try:
            url = self.instance + "/api/tags"
            response = self.session.get(url)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """
        Fetch list of all jobs.\n
        Endpoint: ``/api/jobs``

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            List[Dict[str, Any]]: List of jobs
        """
        try:
            url = self.instance + "/api/jobs"
            response = self.session.get(url)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

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
        try:
            url = self.instance + "/api/tags/"
            response = self.session.get(url + str(tag_id))
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_job_by_id(self, job_id: Union[int, str]) -> Dict[str, Any]:
        """Fetch job info by ID.
        Endpoint: ``/api/job/{job_id}``

        Args:
            job_id (Union[int, str]): Job ID

        Raises:
            IntelOwlClientException: on client/HTTP error

        Returns:
            Dict[str, Any]: JSON body.
        """
        try:
            url = self.instance + "/api/jobs/" + str(job_id)
            response = self.session.get(url)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

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
        analyzers_list: List[str],
        tags_list: List[int],
        run_all: bool,
        force_privacy,
        private_job,
        disable_external_analyzers,
        check,
        runtime_configuration: Dict = None,
        should_poll: bool = False,
    ) -> None:
        """
        For internal use by the pyintelowl CLI.
        """
        if not runtime_configuration:
            runtime_configuration = {}
        # CLI sanity checks
        if analyzers_list and run_all:
            self.logger.warning(
                """
                Can't use -al and -aa options together. See usage with -h.
                """
            )
            return
        if not (analyzers_list or run_all):
            self.logger.warning(
                """
                Either one of -al, -aa must be specified. See usage with -h.
                """,
            )
            return
        analyzers = analyzers_list if analyzers_list else "all available analyzers"
        self.logger.info(
            f"""Requesting analysis..
            {type_}: [blue]{obj}[/]
            analyzers: [i green]{analyzers}[/]
            """
        )
        # 1st step: ask analysis availability
        if check != "force-new":
            md5 = self.get_md5(obj, type_=type_)
            resp = self.ask_analysis_availability(
                md5, analyzers_list, run_all, True if check == "reported" else False
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
                analyzers_requested=analyzers_list,
                observable_name=obj,
                force_privacy=force_privacy,
                private_job=private_job,
                disable_external_analyzers=disable_external_analyzers,
                tags=tags_list,
                run_all_available_analyzers=run_all,
                runtime_configuration=runtime_configuration,
            )
        else:
            path = pathlib.Path(obj)
            resp2 = self.send_file_analysis_request(
                analyzers_requested=analyzers_list,
                filename=path.name,
                binary=path.read_bytes(),
                force_privacy=force_privacy,
                private_job=private_job,
                disable_external_analyzers=disable_external_analyzers,
                tags=tags_list,
                run_all_available_analyzers=run_all,
                runtime_configuration=runtime_configuration,
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

    def _get_observable_classification(self, value: str) -> str:
        """Returns observable classification for the given value.\n
        Only following types are supported:
        ip, domain, url, hash (md5, sha1, sha256)

        Args:
            value (str):
                observable value

        Raises:
            IntelOwlClientException:
                if value type is not recognized

        Returns:
            str: one of `ip`, `url`, `domain` or `hash`.
        """
        try:
            ipaddress.ip_address(value)
        except ValueError:
            if re.match(
                "^(?:ht|f)tps?://[a-z\d-]{1,63}(?:\.[a-z\d-]{1,63})+"
                "(?:/[a-z\d-]{1,63})*(?:\.\w+)?",
                value,
            ):
                classification = "url"
            elif re.match("^(\.)?[a-z\d-]{1,63}(\.[a-z\d-]{1,63})+$", value):
                classification = "domain"
            elif (
                re.match("^[a-f\d]{32}$", value)
                or re.match("^[a-f\d]{40}$", value)
                or re.match("^[a-f\d]{64}$", value)
                or re.match("^[A-F\d]{32}$", value)
                or re.match("^[A-F\d]{40}$", value)
                or re.match("^[A-F\d]{64}$", value)
            ):
                classification = "hash"
            else:
                classification = "general"
                self.logger.warning(
                    f"{value} is neither a domain nor a URL nor a IP not a hash"
                )
        else:
            # its a simple IP
            classification = "ip"

        return classification

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

        killed = False
        try:
            url = self.instance + f"/api/jobs/{job_id}/kill"
            response = self.session.patch(url)
            self.logger.debug(msg=(response.url, response.status_code))
            killed = response.status_code == 200
            response.raise_for_status()
        except Exception as e:
            raise IntelOwlClientException(e)
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

        deleted = False
        try:
            url = self.instance + "/api/jobs/" + str(job_id)
            response = self.session.delete(url)
            self.logger.debug(msg=(response.url, response.status_code))
            deleted = response.status_code == 204
            response.raise_for_status()
        except Exception as e:
            raise IntelOwlClientException(e)
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

        deleted = False
        try:
            url = self.instance + "/api/tags/" + str(tag_id)
            response = self.session.delete(url)
            self.logger.debug(msg=(response.url, response.status_code))
            deleted = response.status_code == 204
            response.raise_for_status()
        except Exception as e:
            raise IntelOwlClientException(e)
        return deleted
