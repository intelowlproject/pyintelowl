import ipaddress
import logging
import pathlib
import re
import requests
import hashlib

from typing import List, Dict, Any

from json import dumps as json_dumps

from .exceptions import IntelOwlClientException


class IntelOwl:
    logger: logging.Logger

    def __init__(
        self,
        token: str,
        instance_url: str,
        certificate: str = None,
        logger: logging.Logger = None,
    ):
        self.token = token
        self.instance = instance_url
        self.certificate = certificate
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

    @property
    def session(self):
        if not hasattr(self, "_session"):
            session = requests.Session()
            if self.certificate:
                session.verify = self.certificate
            session.headers.update(
                {
                    "Authorization": f"Token {self.token}",
                    "User-Agent": "IntelOwlClient/3.0.0",
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
    ):
        answer = None
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
        runtime_configuration: Dict = {},
    ):
        answer = None
        try:
            data = {
                "is_sample": True,
                "md5": self.get_md5(binary, type_="binary"),
                "analyzers_requested": analyzers_requested,
                "run_all_available_analyzers": run_all_available_analyzers,
                "force_privacy": force_privacy,
                "private": private_job,
                "disable_external_analyzers": disable_external_analyzers,
                "file_name": filename,
            }
            if runtime_configuration:
                data["runtime_configuration"] = json_dumps(runtime_configuration)
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
        runtime_configuration: Dict = {},
    ):
        answer = None
        try:
            data = {
                "is_sample": False,
                "md5": self.get_md5(observable_name, type_="observable"),
                "analyzers_requested": analyzers_requested,
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
                data["runtime_configuration"] = json_dumps(runtime_configuration)
            answer = self.__send_analysis_request(data=data, files=None)
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def __send_analysis_request(self, data=None, files=None):
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
            err = """
            Request failed..
            Error: [i yellow]After the filter, no analyzers can be run.
                Try with other analyzers.[/]
            """
            raise IntelOwlClientException(err)
        warnings = answer.get("warnings", [])
        self.logger.info(
            f"""New Job running..
            ID: {answer['job_id']} | Status: [u blue]{answer['status']}[/].
            Got {len(warnings)} warnings:
            [i yellow]{warnings if warnings else None}[/]
        """
        )
        response.raise_for_status()
        return answer

    def ask_analysis_result(self, job_id):
        answer = None
        try:
            params = {"job_id": job_id}
            url = self.instance + "/api/ask_analysis_result"
            response = self.session.get(url, params=params)
            self.logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_analyzer_configs(self):
        answer = None
        try:
            url = self.instance + "/api/get_analyzer_configs"
            response = self.session.get(url)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_all_tags(self):
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

    def get_all_jobs(self):
        answer = None
        try:
            url = self.instance + "/api/jobs"
            response = self.session.get(url)
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_tag_by_id(self, tag_id):
        answer = None
        try:
            url = self.instance + "/api/tags/"
            response = self.session.get(url + str(tag_id))
            self.logger.debug(msg=(response.url, response.status_code))
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            raise IntelOwlClientException(e)
        return answer

    def get_job_by_id(self, job_id):
        answer = None
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
    def get_md5(to_hash: Any, type_="observable"):
        md5 = None
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
        run_all: bool,
        force_privacy,
        private_job,
        disable_external_analyzers,
        check,
    ):
        # CLI sanity checks
        if analyzers_list and run_all:
            self.logger.warn(
                """
                Can't use -al and -aa options together. See usage with -h.
                """
            )
            return
        if not (analyzers_list or run_all):
            self.logger.warn(
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
            _ = self.send_observable_analysis_request(
                analyzers_requested=analyzers_list,
                observable_name=obj,
                force_privacy=force_privacy,
                private_job=private_job,
                disable_external_analyzers=disable_external_analyzers,
                run_all_available_analyzers=run_all,
            )
        else:
            path = pathlib.Path(obj)
            _ = self.send_file_analysis_request(
                analyzers_requested=analyzers_list,
                filename=path.name,
                binary=path.read_bytes(),
                force_privacy=force_privacy,
                private_job=private_job,
                disable_external_analyzers=disable_external_analyzers,
                run_all_available_analyzers=run_all,
            )
        # 3rd step: poll for result
        # todo

    @staticmethod
    def _get_observable_classification(value):
        # only following types are supported:
        # ip - domain - url - hash (md5, sha1, sha256)
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
            ):
                classification = "hash"
            else:
                raise IntelOwlClientException(
                    f"{value} is neither a domain nor a URL nor a IP not a hash"
                )
        else:
            # its a simple IP
            classification = "ip"

        return classification
