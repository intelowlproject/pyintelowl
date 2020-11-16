import ipaddress
import logging
import re
import requests
import sys
import hashlib

from typing import List, Dict

from json import dumps as json_dumps

from .exceptions import IntelOwlClientException

logger = logging.getLogger(__name__)


class IntelOwl:
    def __init__(
        self,
        token: str,
        instance_url: str,
        certificate: str = None,
        debug: bool = False,
    ):
        self.token = token
        self.instance = instance_url
        self.certificate = certificate
        self.__debug__hndlr = logging.StreamHandler(sys.stdout)
        self.debug(debug)

    def debug(self, on: bool) -> None:
        if on:
            # if debug add stdout logging
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self.__debug__hndlr)
        else:
            logger.setLevel(logging.INFO)
            logger.removeHandler(self.__debug__hndlr)

    @property
    def session(self):
        if not hasattr(self, "_session"):
            session = requests.Session()
            if self.certificate:
                session.verify = self.certificate
            session.headers.update(
                {
                    "Authorization": f"Token {self.token}",
                    "User-Agent": "IntelOwlClient/2.0.0",
                }
            )
            self._session = session

        return self._session

    def ask_analysis_availability(
        self,
        md5,
        analyzers_needed,
        run_all_available_analyzers=False,
        check_reported_analysis_too=False,
    ):
        answer = {}
        errors = []
        try:
            params = {"md5": md5, "analyzers_needed": analyzers_needed}
            if run_all_available_analyzers:
                params["run_all_available_analyzers"] = True
            if not check_reported_analysis_too:
                params["running_only"] = True
            url = self.instance + "/api/ask_analysis_availability"
            response = self.session.get(url, params=params)
            logger.debug(response.url)
            logger.debug(response.headers)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}

    def send_file_analysis_request(
        self,
        md5,
        analyzers_requested,
        filename,
        binary,
        force_privacy=False,
        private_job=False,
        disable_external_analyzers=False,
        run_all_available_analyzers=False,
        runtime_configuration=None,
    ):
        if runtime_configuration is None:
            runtime_configuration = {}
        answer = {}
        errors = []
        try:
            data = {
                "md5": md5,
                "analyzers_requested": analyzers_requested,
                "run_all_available_analyzers": run_all_available_analyzers,
                "force_privacy": force_privacy,
                "private": private_job,
                "disable_external_analyzers": disable_external_analyzers,
                "is_sample": True,
                "file_name": filename,
            }
            if runtime_configuration:
                data["runtime_configuration"] = json_dumps(runtime_configuration)
            files = {"file": (filename, binary)}
            url = self.instance + "/api/send_analysis_request"
            response = self.session.post(url, data=data, files=files)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}

    def send_observable_analysis_request(
        self,
        analyzers_requested: List[str],
        observable_name: str,
        md5: str = None,
        force_privacy: bool = False,
        private_job: bool = False,
        disable_external_analyzers: bool = False,
        run_all_available_analyzers: bool = False,
        runtime_configuration: Dict = {},
    ):
        answer = {}
        errors = []
        if not md5:
            md5 = hashlib.md5(observable_name.encode("utf-8")).hexdigest()
        try:
            data = {
                "is_sample": False,
                "md5": md5,
                "analyzers_requested": analyzers_requested,
                "run_all_available_analyzers": run_all_available_analyzers,
                "force_privacy": force_privacy,
                "private": private_job,
                "disable_external_analyzers": disable_external_analyzers,
                "observable_name": observable_name,
                "observable_classification": get_observable_classification(
                    observable_name
                ),
            }
            if runtime_configuration:
                data["runtime_configuration"] = json_dumps(runtime_configuration)
            url = self.instance + "/api/send_analysis_request"
            response = self.session.post(url, data=data)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return answer, errors

    def ask_analysis_result(self, job_id):
        answer = {}
        errors = []
        try:
            params = {"job_id": job_id}
            url = self.instance + "/api/ask_analysis_result"
            response = self.session.get(url, params=params)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}

    def get_analyzer_configs(self):
        answer = None
        error = None
        try:
            url = self.instance + "/api/get_analyzer_configs"
            response = self.session.get(url)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            error = e
        return answer, error

    def get_all_jobs(self):
        answer = []
        errors = []
        try:
            url = self.instance + "/api/jobs"
            response = self.session.get(url)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}

    def get_job_by_id(self, job_id):
        answer = {}
        errors = []
        url = self.instance + "/api/jobs/" + str(job_id)
        response = self.session.get(url)
        logger.debug(response.url)
        answer = response.json()
        return {"errors": errors, "answer": answer}


def get_observable_classification(value):
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
