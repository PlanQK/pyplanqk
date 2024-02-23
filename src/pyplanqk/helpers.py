import logging
import os
import time
from typing import Dict

import requests

from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformJobsApi, ServicePlatformServicesApi
from openapi_client.configuration import Configuration

logger = logging.getLogger(__name__)


def wait_for_service_to_be_created(
        service_id: str,
        version_id: str,
        api_key: Dict[str, str],
        timeout: int = 500,
        step: int = 1,
) -> bool:
    """
    The wait_for_service_to_be_created function waits for a service to be created.

    Args:
        service_id: str: Specify the service_id of a service
        version_id: str: Specify the version of the service to be deleted
        api_key: Dict[str: Pass the api_key as a dictionary
        str]: Define the type of the parameter
        timeout: int: Set the maximum time to wait for the service to be created
        step: int: Specify the time interval between each check
        : Get the service id and version id

    Returns:
        True if the service is created successfully

    Doc Author:
        Trelent
    """
    logger.debug("Wait for service to be created")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    timer = 0
    build_status = services_api.get_build_status(service_id, version_id)
    assert build_status is not None
    while build_status["status"] != "SUCCESS" or build_status["status"] != "FAILED":
        time.sleep(step)
        timer += step
        if timer > timeout:
            return False
        # Check build status again to see if job failed or succeeded
        build_status = services_api.get_build_status(service_id=service_id, version_id=version_id)
        assert build_status is not None
        if build_status["status"] == "SUCCESS":
            logger.debug("")
            return True
        if build_status["status"] in ["FAILED", "CANCELLED"]:
            logger.debug("")
            return False

        logger.debug("%d|%s Creating service...", timer + 1, timeout)
    return True


def wait_for_application_job_to_be_finished(url: str, access_token: str, timeout: int = 500, step: int = 1) -> bool:
    """
    The wait_for_application_job_to_be_finished function waits for the application job to be finished.

    Args:
        url: str: Define the url of the execution
        access_token: str: Authenticate the user
        timeout: int: Set the timeout for the job to finish
        step: int: Specify the time interval between each request

    Returns:
        True if the execution is finished and false otherwise

    Doc Author:
        Trelent
    """
    logger.debug("Wait for execution to be finished")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    status_timer = 0
    execution_status = requests.get(url=url, headers=headers, timeout=30).json()["status"]
    while execution_status not in ["SUCCEEDED", "FAILED"]:
        time.sleep(step)
        status_timer += step
        if status_timer > timeout:
            logger.debug("")
            logger.debug("Execution timeout")
            return False
        execution_status = requests.get(url=url, headers=headers, timeout=30).json()["status"]
        if execution_status == "SUCCEEDED":
            logger.debug("Execution succeeded")
            return True
        if execution_status == "FAILED":
            logger.debug("Execution failed")
            return False

        logger.debug("%d|%s Wait for job...", status_timer + 1, timeout)
    return True


def wait_for_service_job_to_be_finished(job_id: str,
                                        api_key: Dict[str, str],
                                        timeout: int = 500,
                                        step: int = 1) -> bool:
    """
    The wait_for_service_job_to_be_finished function is used to wait for a service job to be finished.
        It takes the following parameters:
            - job_id: The ID of the service job that we want to wait for.
            - api_key: A dictionary containing an API key and its corresponding secret, which are needed in order
                to access the Service Platform's APIs. This parameter is optional; if it isn't provided, then
                default values will be used instead (see below). If you do provide this parameter, then it should have
                two keys named &quot;apiKey&quot; and &quot;apiSecret&quot;, whose values

    Args:
        job_id: str: Identify the job
        api_key: Dict[str: Define the api key as a dictionary
        str]: Define the job_id as a string
        timeout: int: Set the time limit for waiting for a job to finish
        step: int: Define the time interval between each status check

    Returns:
        True if the service job is finished

    Doc Author:
        Trelent
    """
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
        if status == "SUCCEEDED":
            logger.debug("Execution succeeded")
            return True
        if status == "FAILED":
            logger.debug("Execution failed")
            return False

        logger.debug("%d|%s Wait for job...", status_timer + 1, timeout)
    return True


def get_path_delimiter() -> str:
    """
    The get_path_delimiter function returns the path delimiter for the current operating system.

    Args:

    Returns:
        The appropriate path delimiter for the operating system

    Doc Author:
        Trelent
    """
    path_delimiter: str = ""
    if os.name == "nt":
        path_delimiter: str = "\\"
    elif os.name == "posix":
        path_delimiter: str = "/"
    return path_delimiter
