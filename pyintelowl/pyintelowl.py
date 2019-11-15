import ipaddress
import logging
import magic
import re
import requests
import sys

logger = logging.getLogger(__name__)


class IntelOwlClientException(Exception):
    pass


class IntelOwl:

    def __init__(self, api_key, certificate, instance, debug):
        self.api_key = api_key
        self.certificate = certificate
        self.instance = instance
        if debug:
            # if debug add stdout logging
            logger.setLevel(logging.DEBUG)
            logger.addHandler(logging.StreamHandler(sys.stdout))

    @property
    def session(self):
        if not hasattr(self, '_session'):
            session = requests.Session()
            session.verify = self.certificate
            session.headers.update({
                'Authorization': 'Token {}'.format(self.api_key),
                'User-Agent': 'IntelOwlClient/0.1',
            })
            self._session = session

        return self._session

    def ask_analysis_availability(self, md5, analyzers_needed, check_reported_analysis_too=False):
        answer = {}
        errors = []
        try:
            params = {
                "md5": md5,
                "analyzers_needed": analyzers_needed
            }
            if not check_reported_analysis_too:
                params['running_only'] = True
            url = self.instance + "/api/ask_analysis_availability"
            response = self.session.get(url, params=params)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}

    def send_file_analysis_request(self, md5, analyzers_requested, filename, binary,
                                   force_privacy=False, disable_external_analyzers=False):
        answer = {}
        errors = []
        try:
            data = {
                "md5": md5,
                "analyzers_requested": analyzers_requested,
                "force_privacy": force_privacy,
                "disable_external_analyzers": disable_external_analyzers,
                "is_sample": True,
                "file_name": filename,
                "file_mimetype": magic.from_buffer(binary, mime=True),
            }
            files = {"file": (filename, binary)}
            url = self.instance + "/api/send_analysis_request"
            response = self.session.post(url, data=data, files=files)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}

    def send_observable_analysis_request(self, md5, analyzers_requested, observable_name,
                                         force_privacy=False, disable_external_analyzers=False):
        answer = {}
        errors = []
        try:
            data = {
                "md5": md5,
                "analyzers_requested": analyzers_requested,
                "force_privacy": force_privacy,
                "disable_external_analyzers": disable_external_analyzers,
                "is_sample": False,
                "observable_name": observable_name,
                "observable_classification": get_observable_classification(observable_name),
            }
            url = self.instance + "/api/send_analysis_request"
            response = self.session.post(url, data=data)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}

    def ask_analysis_result(self, job_id):
        answer = {}
        errors = []
        try:
            params = {
                "job_id": job_id
            }
            url = self.instance + "/api/ask_analysis_result"
            response = self.session.get(url, params=params)
            logger.debug(response.url)
            response.raise_for_status()
            answer = response.json()
        except Exception as e:
            errors.append(str(e))
        return {"errors": errors, "answer": answer}


def get_observable_classification(value):
    # only following types are supported:
    # ip - domain - url - hash (md5, sha1, sha256)
    try:
        ipaddress.ip_address(value)
    except ValueError:
        if re.match("^(?:ht|f)tps?://[a-z\d-]{1,63}(?:\.[a-z\d-]{1,63})+(?:/[a-z\d-]{1,63})*(?:\.\w+)?", value):
            classification = 'url'
        elif re.match("^(\.)?[a-z\d-]{1,63}(\.[a-z\d-]{1,63})+$", value):
            classification = 'domain'
        elif re.match("^[a-f\d]{32}$", value) or re.match("^[a-f\d]{40}$", value) or re.match("^[a-f\d]{64}$", value):
            classification = 'hash'
        else:
            raise IntelOwlClientException("{} is neither a domain nor a URL nor a IP not a hash".format(value))
    else:
        # its a simple IP
        classification = 'ip'

    return classification
