import time
import requests
import logging

from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.apis import ServicePlatformJobsApi
from openapi_client.configuration import Configuration

from typing import Dict


logger = logging.getLogger(__name__)


def wait_for_service_to_be_created(service_id: str,
                                   version_id: str,
                                   api_key: Dict[str, str],
                                   timeout: int = 500,
                                   step: int = 1) -> bool:
    logger.debug("Wait for service to be created")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    timer = 0
    build_status = services_api.get_build_status(service_id, version_id)
    assert build_status is not None
    while build_status['status'] != 'SUCCESS' or build_status['status'] != 'FAILED':
        time.sleep(step)
        timer += step
        if timer > timeout:
            return False
        # Check build status again to see if job failed or succeeded
        build_status = services_api.get_build_status(
            service_id=service_id, version_id=version_id)
        assert build_status is not None
        if build_status['status'] == 'SUCCESS':
            logger.debug("")
            return True
        elif build_status['status'] in ['FAILED', 'CANCELLED']:
            logger.debug("")
            return False
        else:
            logger.debug(f"{timer + 1}|{timeout} Creating service...")


def wait_for_application_job_to_be_finished(url: str,
                                            access_token: str,
                                            timeout: int = 500,
                                            step: int = 1) -> bool:
    logger.debug("Wait for execution to be finished")

    headers = {
        'accept': 'application/json',
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    status_timer = 0
    execution_status = requests.get(url=url, headers=headers).json()['status']
    while execution_status not in ["SUCCEEDED", "FAILED"]:
        time.sleep(step)
        status_timer += step
        if status_timer > timeout:
            logger.debug("")
            logger.debug("Execution timeout")
            return False
        execution_status = requests.get(url=url, headers=headers).json()['status']
        if execution_status == 'SUCCEEDED':
            logger.debug("Execution succeeded")
            return True
        elif execution_status == 'FAILED':
            logger.debug("Execution failed")
            return False
        else:
            logger.debug(f"{status_timer + 1}|{timeout} Wait for job...")


def wait_for_service_job_to_be_finished(job_id: str,
                                        api_key: Dict[str, str],
                                        timeout: int = 500,
                                        step: int = 1) -> bool:
    logger.debug("Wait for service job to be finished")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    status_timer = 0
    status = service_jobs_api.get_job(job_id).status

    while status not in ["SUCCEEDED", "FAILED"]:
        time.sleep(step)
        status_timer += step
        if status_timer > timeout:
            logger.debug("")
            logger.debug("Execution timeout")
            return False
        status = service_jobs_api.get_job(job_id).status
        if status == 'SUCCEEDED':
            logger.debug("Execution succeeded")
            return True
        elif status == 'FAILED':
            logger.debug("Execution failed")
            return False
        else:
            logger.debug(f"{status_timer + 1}|{timeout} Wait for job...")
