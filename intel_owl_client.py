import argparse
import hashlib
import logging
import os
import pprint
import requests
import time

from pyintelowl.pyintelowl import IntelOwl, IntelOwlClientException


def intel_owl_client():

    parser = argparse.ArgumentParser(description='Intel Owl classic client.')
    parser.add_argument("-k", "--api-key", required=True, help="your Intel Owl API key")
    parser.add_argument("-c", "--certificate", default=False, help="path to Intel Owl certificate")
    parser.add_argument("-i", "--instance", required=True, help="your instance URL")
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="debug mode")
    parser.add_argument("-l", "--log-to-file", help="log to specified file")
    parser.add_argument("-a", "--analyzers-list", required=True, action='append',
                        help="list of analyzers to launch")
    parser.add_argument("-p", "--force-privacy", action="store_true", default=False,
                        help="disable analyzers that could impact privacy")
    parser.add_argument("-r", "--check-reported-analysis-too", action="store_true", default=False,
                        help="check reported analysis too, not only 'running' ones")

    subparsers = parser.add_subparsers(help='choose type of analysis', dest='command')
    parser_sample = subparsers.add_parser('file', help='File analysis')
    parser_observable = subparsers.add_parser('observable', help='Observables analysis')

    parser_sample.add_argument("-f", "--file", required=True, help="file to analyze")
    parser_observable.add_argument("-v", "--value", required=True, help="observable to analyze")

    args = parser.parse_args()

    logger = get_logger(args.debug, args.log_to_file)

    md5 = None
    results = []
    elapsed_time = None
    try:
        filename = None
        binary = None
        if args.command == 'file':
            if not os.path.exists(args.file):
                raise IntelOwlClientException("{} does not exists".format(args.file))
            with open(args.file, "rb") as f:
                binary = f.read()
                filename = os.path.basename(f.name)
            md5 = hashlib.md5(binary).hexdigest()
        elif args.command == 'observable':
            md5 = hashlib.md5(args.value.encode('utf-8')).hexdigest()
        else:
            raise IntelOwlClientException("you must specify the type of the analysis: [observable, file]")

        pyintelowl_client = IntelOwl(args.api_key, args.certificate, args.instance, args.debug)

        job_id_to_get = None
        # first step: ask analysis availability
        logger.info("about to request ask_analysis_availability for md5: {}, analyzers: {}"
                    "".format(md5, args.analyzers_list))
        analysis_available = False

        api_request_result = pyintelowl_client.ask_analysis_availability(md5, args.analyzers_list,
                                                                         args.check_reported_analysis_too)
        errors = api_request_result.get('errors', [])
        if errors:
            raise IntelOwlClientException("API ask_analysis_availability failed. Errors: {}"
                                          "".format(errors))
        answer = api_request_result.get('answer', {})
        status = answer.get('status', '')
        if not status:
            raise IntelOwlClientException("API ask_analysis_availability gave result without status!?!?"
                                          "answer:{}".format(answer))
        elif status != 'not_available':
            analysis_available = True
            job_id_to_get = answer.get('job_id', '')
            if job_id_to_get:
                logger.info("found already existing job with id {} and status {} for md5 {} and analyzers {}"
                            "".format(job_id_to_get, status, md5, args.analyzers_list))
            else:
                raise IntelOwlClientException(
                    "API ask_analysis_availability gave result without job_id!?!? answer:{}"
                    "".format(answer))

        # second step: in case there are no analysis available, start a new analysis
        if not analysis_available:

            if args.command == 'file':
                api_request_result = pyintelowl_client.send_file_analysis_request(md5, args.analyzers_list, filename,
                                                                                  binary, args.force_privacy)
            elif args.command == 'observable':
                api_request_result = pyintelowl_client.send_observable_analysis_request(md5, args.analyzers_list,
                                                                                        args.value, args.force_privacy)
            else:
                raise NotImplementedError()

            # both cases share the same logic for the management of the result retrieved from the API
            errors = api_request_result.get('errors', [])
            if errors:
                raise IntelOwlClientException("API send_analysis_request failed. Errors: {}"
                                              "".format(errors))
            answer = api_request_result.get('answer', {})
            logger.info("md5 {} received response from intel_owl: {}".format(md5, answer))
            status = answer.get('status', '')
            if not status:
                raise IntelOwlClientException(
                    "API send_analysis_request gave result without status!?!? answer:{}"
                    "".format(answer))
            elif status != "accepted":
                raise IntelOwlClientException("API send_analysis_request gave unexpected result status:{}"
                                              "".format(status))
            else:
                job_id_to_get = answer.get('job_id', '')
                analyzers_running = answer.get('analyzers_running', '')
                warnings = answer.get('warnings', [])
                if job_id_to_get:
                    logger.info("started job with id {} and status {} for md5 {} and analyzers {}. Warnings:{}"
                                "".format(job_id_to_get, status, md5, analyzers_running, warnings))
                else:
                    raise IntelOwlClientException("API send_analysis_request gave result without job_id!?!?"
                                                  "answer:{}".format(answer))

        # third step: at this moment we must have a job_id to check for results
        polling_max_tries = 60 * 20
        polling_interval = 1
        logger.info("started polling")
        for chance in range(polling_max_tries):
            time.sleep(polling_interval)
            api_request_result = pyintelowl_client.ask_analysis_result(job_id_to_get)
            errors = api_request_result.get('errors', [])
            if errors:
                raise IntelOwlClientException("API ask_analysis_result failed. Errors: {}"
                                              "".format(errors))
            answer = api_request_result.get('answer', {})
            status = answer.get('status', '')
            if not status:
                raise IntelOwlClientException(
                    "API ask_analysis_result gave result without status!?!? job_id:{} answer:{}"
                    "".format(job_id_to_get, answer))
            elif status in ['invalid_id', 'not_available']:
                raise IntelOwlClientException("API send_analysis_request gave status {}".format(status))
            elif status == 'running':
                continue
            elif status == 'pending':
                logger.warning("API ask_analysis_result check job in status 'pending'. Maybe it is stuck"
                               "job_id:{} md5:{} analyzer_list:{}".format(job_id_to_get, md5, args.analyzers_list))
            elif status in ['reported_without_fails', 'reported_with_fails', 'failed']:
                logger.info("job_id {} Analysis finished. Status: {} "
                            "md5:{} analyzer_list:{}".format(job_id_to_get, status, md5, args.analyzers_list))
                results = answer.get('results', [])
                elapsed_time = answer.get('elapsed_time_in_seconds', [])
                break
        if not results:
            raise IntelOwlClientException("reached polling timeout without results. Job_id {}"
                                          "".format(job_id_to_get))

    except IntelOwlClientException as e:
        logger.error("Error:{} md5:{}".format(e, md5))
    except requests.exceptions.HTTPError as e:
        logger.error(e)
    except Exception as e:
        logger.exception(e)

    logger.info("elapsed time: {}".format(elapsed_time))
    logger.info("results:")
    pprint.pprint(results)


def get_logger(debug_mode, log_to_file):
    if debug_mode:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    if log_to_file:
        handler = logging.FileHandler(log_to_file)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s',
                                  '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    intel_owl_client()
