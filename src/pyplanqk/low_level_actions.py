import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

import requests

from openapi_client import ApiClient, Configuration
from openapi_client.api.service_platform___jobs_api import ServicePlatformJobsApi
from openapi_client.api.service_platform___services_api import ServicePlatformServicesApi
from openapi_client.apis import ServicePlatformApplicationsApi
from openapi_client.model.create_application_request import CreateApplicationRequest
from openapi_client.model.create_job_request import CreateJobRequest
from openapi_client.model.data_pool_ref import DataPoolRef
from pyplanqk.helpers import wait_for_service_job_to_be_finished

logger = logging.getLogger(__name__)


def create_managed_service(config: Dict[str, Any], api_key: Dict[str, str]) -> Dict[str, Any]:
    """
    The create_managed_service function creates a managed service in the Service Platform.

    Args:
        config: Dict[str: Pass the configuration parameters to the function
        Any]: Specify the type of the return value
        api_key: Dict[str: Pass in the api key to the function
        str]: Specify the type of the variable

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Create managed service.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = services_api.create_managed_service(**config)
        service = service.to_dict()
        logger.debug("Service creation triggered.")
        return service
    except Exception as e:
        logger.error("Service creation failed.")
        logger.error(e)
        raise e


def create_application(application_name: str, api_key: Dict[str, str]) -> Dict[str, Any]:
    """
    The create_application function creates a new application in the Service Platform.

    Args:
        application_name: str: Specify the name of the application
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the type of the parameter

    Returns:
        A dictionary

    Doc Author:
        Trelent
    """
    logger.debug("Create application.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        create_app_request = CreateApplicationRequest(name=application_name)
        application = applications_api.create_application(create_application_request=create_app_request)
        logger.debug("Application created.")
        return application
    except Exception as e:
        logger.error("Create application failed.")
        logger.error(e)
        raise e


def publish_service_internally(service_name: str, api_key: Dict[str, str]) -> Dict[str, Any]:
    """
    The publish_service_internally function publishes a service internally.

    Args:
        service_name: str: Get the service name
        api_key: Dict[str: Pass in the api key for authentication
        str]: Specify the service name

    Returns:
        A service object

    Doc Author:
        Trelent
    """
    logger.debug("Publish service internally.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = get_service(service_name, api_key)
        assert service is not None
        version = get_version(service_name, api_key)
        assert version is not None
        service_id = service["id"]
        version_id = version["id"]
        service = services_api.publish_service_internal(service_id, version_id)
        logger.debug("Service published internally succeeded.")
        return service
    except Exception as e:
        logger.error("Service publishing internally failed.")
        logger.error(e)
        raise e


def unpublish_service(service_name: str, api_key: Dict[str, str]) -> Dict[str, Any]:
    """
    The unpublish_service function unpublishes a service.

    Args:
        service_name: str: Specify the name of the service to be published
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the service name

    Returns:
        The service object

    Doc Author:
        Trelent
    """
    logger.debug("Unpublish service.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = get_service(service_name, api_key)
        assert service is not None
        version = get_version(service_name, api_key)
        assert version is not None
        service_id = service["id"]
        version_id = version["id"]
        service = services_api.unpublish_service(service_id, version_id)
        logger.debug("Service unpublished.")
        return service
    except Exception as e:
        logger.error("Service unpublishing failed.")
        logger.error(e)
        raise e


def remove_service(service_name: str, api_key: Dict[str, str]) -> bool:
    """
    The remove_service function removes a service from the Service Platform.

    Args:
        service_name: str: Identify the service to be removed
        api_key: Dict[str: Specify the type of the parameter
        str]: Specify the type of the parameter

    Returns:
        True if the service was removed successfully

    Doc Author:
        Trelent
    """
    logger.debug("Remove service.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = get_service(service_name, api_key)
        assert service is not None

        service_id = service["id"]
        services_api.delete_service(service_id)
        logger.debug("Service removed.")
        return True
    except Exception as e:
        logger.error("Service removing failed.")
        logger.error(e)
        raise e


def remove_application(application_name: str, api_key: Dict[str, str]) -> bool:
    """
    The remove_application function removes an application from the Service Platform.

    Args:
        application_name: str: Identify the application to be removed
        api_key: Dict[str: Specify the type of the parameter
        str]: Specify the type of the parameter

    Returns:
        True if the application is removed

    Doc Author:
        Trelent
    """
    logger.debug("Remove application.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        application = get_application(application_name, api_key)
        assert application is not None
        application_id = application["id"]
        applications_api.delete_application(application_id)
        logger.debug("Application removed.")
        return True
    except Exception as e:
        logger.error("Application removing failed.")
        logger.error(e)
        raise e


def remove_subscription(application_name: str, api_key: Dict[str, str]) -> bool:
    """
    The remove_subscription function removes a subscription for an application.

    Args:
        application_name: str: Identify the application
        api_key: Dict[str: Pass the api key as a dictionary
        str]: Specify the type of the parameter

    Returns:
        True if the subscription is removed

    Doc Author:
        Trelent
    """
    logger.debug("Remove subscription.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        application = get_application(application_name, api_key)
        assert application is not None
        subscription = get_subscription(application_name, api_key)
        application_id = application["id"]
        subscription_id = subscription["id"]
        applications_api.delete_application_subscription(application_id, subscription_id)
        logger.debug("Subscription removed.")
        return True
    except Exception as e:
        logger.error("Subscription removal failed.")
        logger.error(e)
        raise e


def subscribe_application_to_service(
    application_name: str, service_name: str, api_key: Dict[str, str]
) -> Dict[str, Any]:
    """
    The subscribe_application_to_service function subscribes an application to a service.

    Args:
        application_name: str: Specify the name of the application to be subscribed
        service_name: str: Specify the name of the service to be subscribed to
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the type of data that is expected in the function

    Returns:
        A subscription object

    Doc Author:
        Trelent
    """
    logger.debug("Subscribe application to service.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        service = get_service(service_name, api_key)
        assert service is not None
        application = get_application(application_name, api_key)
        assert application is not None
        service_id = service["id"]
        application_id = application["id"]
        subscription_request = CreateInternalSubscriptionRequest(application_id=application_id, service_id=service_id)
        subscription = applications_api.create_internal_subscription(
            id=application_id, create_internal_subscription_request=subscription_request
        )
        logger.debug("Application subscribed.")
        return subscription
    except Exception as e:
        logger.error("Application subscription failed.")
        logger.error(e)
        raise e


def get_application(application_name: str, api_key: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    The get_application function retrieves the application with the given name from the Service Platform.

    Args:
        application_name: str: Specify the name of the application to retrieve
        api_key: Dict[str: Pass in the api key as a dictionary
        str]: Specify the type of the application_name variable

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Get application.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        applications = applications_api.get_applications()

        found_application = None
        for application in applications:
            if application_name == application["name"]:
                found_application = application
        return found_application
    except Exception as e:
        logger.error("Application retrieval failed.")
        logger.error(e)
        raise e


def get_services(api_key: Dict[str, str], lifecycle: str = None) -> List[Dict[str, Any]]:
    """
    The get_services function retrieves all services from the Service Platform.

    Args:
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the type of the parameter
        lifecycle: str: Filter the services based on their lifecycle

    Returns:
        A list of dictionaries

    Doc Author:
        Trelent
    """
    logger.debug("Get services.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        if lifecycle is None:
            created_services = services_api.get_services(lifecycle="CREATED")
            accessible_services = services_api.get_services(lifecycle="ACCESSIBLE")
            published_services = services_api.get_services(lifecycle="PUBLISHED")

            services = []
            services.extend(created_services)
            services.extend(accessible_services)
            services.extend(published_services)
            services = [service.to_dict() for service in services]
        else:
            services = services_api.get_services(lifecycle=lifecycle)
            services = [service.to_dict() for service in services]
        return services
    except Exception as e:
        logger.error("Services retrieval failed.")
        logger.error(e)
        raise e


def get_service(service_name: str, api_key: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    The get_service function retrieves a service from the Service Platform.

    Args:
        service_name: str: Specify the name of the service to be retrieved
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the type of the parameter

    Returns:
        A service

    Doc Author:
        Trelent
    """
    logger.debug("Get service.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        services = get_services(api_key)
        assert services is not None

        found_service = None
        for service in services:
            if service_name == service["name"]:
                found_service = service

        if found_service is not None:
            service_id = found_service["id"]
            found_service = services_api.get_service(service_id)
            found_service = found_service.to_dict()

        return found_service
    except Exception as e:
        logger.error("Service retrieval failed.")
        logger.error(e)
        raise e


def get_version(service_name: str, api_key: Dict[str, str]) -> Dict[str, Any]:
    """
    The get_version function returns the version of a service.

    Args:
        service_name: str: Specify the service name
        api_key: Dict[str: Specify the type of data that is expected to be passed into the function
        str]: Specify the type of the parameter

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Get version.")

    try:
        service = get_service(service_name, api_key)
        assert service is not None
        return service["service_definitions"][0]
    except Exception as e:
        logger.error("Version retrieval failed.")
        logger.error(e)
        raise e


def get_all_subscriptions(application_name: str, api_key: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    The get_all_subscriptions function retrieves all subscriptions for a given application.

    Args:
        application_name: str: Specify the name of the application that you want to get subscriptions for
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the type of the return value

    Returns:
        A list of dictionaries

    Doc Author:
        Trelent
    """
    logger.debug("Get subscriptions.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        application = get_application(application_name, api_key)
        assert application is not None
        application_id = application["id"]
        subscriptions = applications_api.get_application_subscriptions(application_id)
        return subscriptions
    except Exception as e:
        logger.error("Subscriptions retrieval failed.")
        logger.error(e)
        raise e


def get_subscription(application_name: str, api_key: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    The get_subscription function retrieves the subscription for a given application.

    Args:
        application_name: str: Specify the name of the application
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the type of the return value

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Get subscriptions.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        application = get_application(application_name, api_key)
        assert application is not None
        application_id = application["id"]
        subscriptions = applications_api.get_application_subscriptions(application_id)
        subscription = subscriptions[0]
        return subscription
    except Exception as e:
        logger.error("Subscriptions retrieval failed.")
        logger.error(e)
        raise e


def get_access_token(consumer_key: str, consumer_secret: str, token_url: str) -> str:
    """
    The get_access_token function is used to get an access token from the OAuth2 server.

    Args:
        consumer_key: str: Pass in the consumer key for the api
        consumer_secret: str: Authenticate the client
        token_url: str: Specify the url of the token endpoint

    Returns:
        A string

    Doc Author:
        Trelent
    """
    logger.debug("Get access_token.")

    try:
        data = {"grant_type": "client_credentials"}

        response = requests.post(
            token_url, data=data, verify=False, allow_redirects=False, auth=(consumer_key, consumer_secret), timeout=30
        )
        assert response.status_code in [200, 201, 204]
        json_response = response.json()
        return json_response["access_token"]
    except Exception as e:
        logger.error("Get access_token failed.")
        logger.error(e)
        raise e


def get_all_jobs_for_managed_service(service_name: str, api_key: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    The get_all_jobs_for_managed_service function returns a list of all jobs for the specified service.

    Args:
        service_name: str: Specify the name of the service
        api_key: Dict[str: Pass in the api key
        str]: Specify the service name

    Returns:
        A list of all jobs for a managed service

    Doc Author:
        Trelent
    """
    logger.debug("Get all service jobs for managed service.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = get_service(service_name, api_key)
        assert service is not None
        version = get_version(service_name, api_key)
        assert version is not None
        service_id = service["id"]
        version_id = version["id"]
        jobs = services_api.get_managed_service_executions(service_id, version_id)
        return jobs
    except Exception as e:
        logger.error("Get all service jobs failed.")
        logger.error(e)
        raise e


def get_all_service_jobs(api_key: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    The get_all_service_jobs function returns a list of all service jobs.

    Args:
        api_key: Dict[str: Pass in the api key for authentication
        str]: Specify the type of the parameter

    Returns:
        A list of dictionaries

    Doc Author:
        Trelent
    """
    logger.debug("Get all service jobs.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    try:
        jobs = service_jobs_api.get_jobs()
        assert jobs is not None
        return jobs
    except Exception as e:
        logger.error("Get all service jobs failed.")
        logger.error(e)
        raise e


def get_service_jobs(service_name: str, api_key: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    The get_service_jobs function returns a list of all jobs for the service.

    Args:
        service_name: str: Specify the name of the service to get jobs for
        api_key: Dict[str: Pass in the api key to authenticate with the platform
        str]: Specify the service name

    Returns:
        A list of jobs for a service

    Doc Author:
        Trelent
    """
    logger.debug("Get service jobs for service.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    try:
        service = get_service(service_name, api_key)
        assert service is not None
        service_definition_id = service["service_definitions"][0]["id"]
        jobs = service_jobs_api.get_jobs()
        assert jobs is not None
        service_jobs = []
        for service_job in jobs:
            service_job_definition_id = service_job["service_definition"]["id"]
            if service_job_definition_id == service_definition_id:
                service_jobs.append(service_job.to_dict())
        return service_jobs
    except Exception as e:
        logger.error("Get all service jobs failed.")
        logger.error(e)
        raise e


def get_managed_service_job(service_name: str, job_id: str, api_key: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    The get_managed_service_job function returns a job for the specified service.

    Args:
        service_name: str: Identify the service that you want to get a job for
        job_id: str: Specify the job to get
        api_key: Dict[str: Pass in the api key for authentication
        str]: Specify the type of the parameter

    Returns:
        The job with the given id

    Doc Author:
        Trelent
    """
    logger.debug("Get managed service job.")

    try:
        jobs = get_all_jobs_for_managed_service(service_name, api_key)

        found_job = None
        for job in jobs:
            if job["id"] == job_id:
                found_job = job
        return found_job
    except Exception as e:
        logger.error("Get service job failed.")
        logger.error(e)
        raise e


def get_service_job(job_id: str, api_key: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    The get_service_job function retrieves a service job from the Service Platform.

    Args:
        job_id: str: Specify the job id of the service job you want to get
        api_key: Dict[str: Pass in the api key for authentication
        str]: Specify the job id

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Get managed service job.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    try:
        job = service_jobs_api.get_job(job_id)
        assert job is not None
        return job.to_dict()
    except Exception as e:
        logger.error("Get service job failed.")
        logger.error(e)
        raise e


def trigger_application_job(
    service_name: str,
    data: Dict[str, list],
    params: Dict[str, str],
    access_token: str,
    api_key: Dict[str, str],
) -> Dict[str, Any]:
    """
    The trigger_application_job function is used to trigger the execution of a service.

    Args:
        service_name: str: Identify the service that is being called
        data: Dict[str: Pass the data to the application
        list]: Specify the list of data to be passed to the application
        params: Dict[str: Pass parameters to the application
        str]: Specify the service name
        access_token: str: Authenticate the user
        api_key: Dict[str: Get the api key from the user
        str]: Specify the service name
        : Get the version of the service

    Returns:
        The job id

    Doc Author:
        Trelent
    """
    logger.debug("Trigger application execution.")

    try:
        version = get_version(service_name, api_key)
        service_endpoint = version["gateway_endpoint"]
        service_endpoint = f"{service_endpoint}/"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {"data": data, "params": params}

        response = requests.post(service_endpoint, json=payload, headers=headers, timeout=30)
        assert response.status_code in [200, 201, 204]
        json_response = response.json()
        return json_response
    except Exception as e:
        logger.error("Trigger application execution failed.")
        logger.error(e)
        raise e


def trigger_service_job(
    service_name: str,
    api_key: Dict[str, str],
    data: Dict[str, Any] = None,
    params: Dict[str, Any] = None,
    mode: str = "DATA_UPLOAD",
    data_ref: Dict[str, Any] = None,
    timeout=500,
    step=1,
) -> Dict[str, Any]:
    """
    The trigger_service_job function triggers a service job on the platform.

    Args:
        service_name: str: Specify the name of the service
        api_key: Dict[str: Authenticate the user
        str]: Specify the service name
        data: Dict[str: Pass in the input data to the service
        Any]: Define the type of data that is returned from the function
        params: Dict[str: Pass parameters to the service
        Any]: Specify that the function can return any type of data
        mode: str: Specify whether the service job is triggered with data from a data pool or by uploading the data
        data_ref: Dict[str: Specify the data pool reference
        Any]: Specify that the function can return any type of data
        timeout: Set the maximum time to wait for a job to finish
        step: Control the polling interval
        : Specify the service name

    Returns:
        The job object

    Doc Author:
        Trelent
    """
    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    try:
        service = get_service(service_name, api_key)
        assert service is not None

        service_definition_id = service["service_definitions"][0]["id"]

        if mode == "DATA_UPLOAD":
            create_job_request = CreateJobRequest(
                service_definition_id=service_definition_id,
                input_data=json.dumps(data),
                parameters=json.dumps(params),
                persist_result=True,
            )
        elif mode == "DATA_POOL":
            data_ref = DataPoolRef(**data_ref)

            create_job_request = CreateJobRequest(
                service_definition_id=service_definition_id,
                input_data_ref=data_ref,
                parameters=json.dumps(params),
                persist_result=True,
            )
        else:
            raise Exception("Invalid mode, allowed modes are: [DATA_UPLOAD, DATA_POOL].")

        job = service_jobs_api.create_job(create_job_request=create_job_request)
        job_id = job["id"]
        logger.info("Started service job: %s.", job_id)
        wait_for_service_job_to_be_finished(job_id, api_key, timeout=timeout, step=step)
        job = service_jobs_api.get_job(job_id)
        return job
    except Exception as e:
        logger.error("Trigger service job failed.")
        logger.error(e)
        raise e


def remove_service_job(job_id: str, api_key: Dict[str, str]) -> bool:
    """
    The remove_service_job function removes a service job from the platform.

    Args:
        job_id: str: Identify the job to be removed
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the job id

    Returns:
        A boolean value

    Doc Author:
        Trelent
    """
    logger.debug("Remove service job.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    try:
        service_jobs_api.delete_job(job_id)
        return True
    except Exception as e:
        logger.error("Remove service job failed.")
        logger.error(e)
        raise e


def get_service_job_status(job_id: str, api_key: Dict[str, str]) -> str:
    """
    The get_service_job_status function returns the status of a service job.

    Args:
        job_id: str: Identify the job
        api_key: Dict[str: Pass in the api key
        str]: Specify the type of data that is being passed into the function

    Returns:
        The status of the service job

    Doc Author:
        Trelent
    """
    logger.debug("Get service job status.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    try:
        job = service_jobs_api.get_job(job_id)
        status = job["status"]
        return status
    except Exception as e:
        logger.error("Get service job status failed.")
        logger.error(e)
        raise e


def get_service_job_result(job_id: str, api_key: Dict[str, str]) -> Dict[str, Any]:
    """
    The get_service_job_result function is used to retrieve the result of a service job.

    Args:
        job_id: str: Specify the job id of the service job
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the job id

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Get service job result.")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    try:
        job = service_jobs_api.get_job(job_id)
        result_string = job["result"]
        result = json.loads(result_string)
        result = result["result"]
        logger.debug("Service job result returned.")
        return result
    except Exception as e:
        logger.error("Get service job status failed.")
        logger.error(e)
        raise e


def get_application_job_info(
    service_name: str, job_id: str, access_token: str, api_key: Dict[str, str]
) -> Dict[str, Any]:
    """
    The get_application_job_info function is used to retrieve the status of a job that has been submitted to an application.

    Args:
        service_name: str: Identify the service
        job_id: str: Identify the job
        access_token: str: Authenticate the user
        api_key: Dict[str: Pass in the api key for the service
        str]: Get the service name

    Returns:
        A dictionary that contains the job id, status, and result

    Doc Author:
        Trelent
    """
    logger.debug("Get application job info.")

    try:
        version = get_version(service_name, api_key)
        assert version is not None
        service_endpoint = version["gateway_endpoint"]
        service_endpoint = os.path.join(service_endpoint, job_id)
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(service_endpoint, headers=headers, timeout=30)
        json_response = response.json()
        return json_response
    except Exception as e:
        logger.error("Get application job info failed.")
        logger.error(e)
        raise e


def get_application_job_status(service_name: str, job_id: str, access_token: str, api_key: Dict[str, str]) -> str:
    """
    The get_application_job_status function is used to get the status of a job.

    Args:
        service_name: str: Specify the service name
        job_id: str: Identify the job
        access_token: str: Authenticate the user
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the service name

    Returns:
        The status of the application job

    Doc Author:
        Trelent
    """
    logger.debug("Get application job status.")

    try:
        version = get_version(service_name, api_key)
        assert version is not None
        service_endpoint = version["gateway_endpoint"]
        service_endpoint = os.path.join(service_endpoint, job_id)
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(service_endpoint, headers=headers, timeout=30)
        json_response = response.json()
        status = json_response["status"]
        return status
    except Exception as e:
        logger.error("Get application job status failed.")
        logger.error(e)
        raise e


def get_application_job_result(
    service_name: str, job_id: str, access_token: str, api_key: Dict[str, str]
) -> Dict[str, Any]:
    """
    The get_application_job_result function is used to retrieve the result of a job that has been submitted to an application.

    Args:
        service_name: str: Specify the name of the service
        job_id: str: Identify the job
        access_token: str: Authenticate the user
        api_key: Dict[str: Pass the api key to the function
        str]: Specify the service name

    Returns:
        The result of the job

    Doc Author:
        Trelent
    """
    logger.debug("Get application job result.")

    try:
        version = get_version(service_name, api_key)
        assert version is not None
        service_endpoint = version["gateway_endpoint"]
        service_endpoint = os.path.join(service_endpoint, job_id, "result")
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(service_endpoint, headers=headers, timeout=30)
        assert response.status_code in [200, 201, 204]
        json_response = response.json()
        result = json_response["result"]
        return result
    except Exception as e:
        logger.error("Get application job result failed.")
        logger.error(e)
        raise e


def get_data_pools(api_key: str) -> List[Dict[str, Any]]:
    """
    The get_data_pools function returns a list of dictionaries containing the data pools.

    Args:
        api_key: str: Authenticate the user

    Returns:
        A list of data pools

    Doc Author:
        Trelent
    """
    logger.debug("Get data pools.")

    try:
        url = "https://platform.planqk.de/qc-catalog/data-pools"

        headers = {"Content-Type": "application/json", "X-Auth-Token": api_key}

        response = requests.get(url, headers=headers, timeout=30)
        assert response.status_code in [200, 201, 204]
        data_pools = response.json()["content"]
        return data_pools
    except Exception as e:
        logger.error("Get data pools failed.")
        logger.error(e)
        raise e


def create_data_pool(data_pool_name: str, api_key: str) -> Dict[str, Any]:
    """
    The create_data_pool function creates a data pool on the PlanQK platform.

    Args:
        data_pool_name: str: Name the data pool
        api_key: str: Authenticate the user

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Create data pool.")

    try:
        url = "https://platform.planqk.de/qc-catalog/data-pools"

        headers = {"Content-Type": "application/json", "X-Auth-Token": api_key}

        data = {"name": data_pool_name}

        response = requests.post(url, headers=headers, json=data, timeout=30)
        assert response.status_code in [200, 201, 204]
        data_pool = response.json()
        return data_pool
    except Exception as e:
        logger.error("Create data pool failed.")
        logger.error(e)
        raise e


def get_data_pool(data_pool_name: str, api_key: str) -> Optional[Dict[str, str]]:
    """
    The get_data_pool function takes a data pool name and an API key as input.
    It then calls the get_data_pools function to retrieve all of the data pools in your account.
    The function then iterates through each of these data pools, looking for one with a matching name.
    If it finds one, it returns that dictionary object representing that specific data pool.

    Args:
        data_pool_name: str: Specify the name of the data pool to be deleted
        api_key: str: Authenticate the user

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Trelent
    """
    logger.debug("Get data pool.")

    try:
        data_pools = get_data_pools(api_key)
        assert data_pools is not None

        found_data_pool = None
        for data_pool in data_pools:
            if data_pool_name == data_pool["name"]:
                logger.debug("Get Pool: Found it!")
                found_data_pool = data_pool
                return found_data_pool
        logger.debug("Get Pool: Didn't found it!")

        return found_data_pool
    except Exception as e:
        logger.error("Get data pool failed.")
        logger.error(e)
        raise e


def remove_data_pool(data_pool_name: str, api_key: str) -> bool:
    """
    The remove_data_pool function removes a data pool from the PlanQK platform.

    Args:
        data_pool_name: str: Identify the data pool
        api_key: str: Authenticate the user

    Returns:
        A boolean value

    Doc Author:
        Trelent
    """
    logger.debug("Remove data pool.")

    try:
        headers = {"Content-Type": "application/json", "X-Auth-Token": api_key}

        data_pool = get_data_pool(data_pool_name, api_key)
        assert data_pool is not None

        data_pool_id = data_pool["id"]
        url = f"https://platform.planqk.de/qc-catalog/data-pools/{data_pool_id}"

        response = requests.delete(url, headers=headers, timeout=30)
        result = response.status_code in [200, 201, 204]
        return result
    except Exception as e:
        logger.error("Remove data pool failed.")
        logger.error(e)
        raise e


def get_data_pool_file_information(data_pool_name: str, api_key: str) -> Dict[str, Any]:
    """
    The get_data_pool_file_information function returns a dictionary of dictionaries containing information about the files in a data pool.
    The keys of the outer dictionary are file names, and each inner dictionary contains information about one file.
    The following keys are available: identifier, data_pool_id, data_source_descriptor_id and file id.

    Args:
        data_pool_name: str: Specify the name of the data pool
        api_key: str: Authenticate the user

    Returns:
        A dictionary with information about the data pool files

    Doc Author:
        Trelent
    """
    logger.debug("Get data pool file information.")

    try:
        data_pool = get_data_pool(data_pool_name, api_key)
        assert data_pool is not None
        data_pool_id = data_pool["id"]

        url = f"https://platform.planqk.de/qc-catalog/data-pools/{data_pool_id}/data-source-descriptors"

        headers = {"Content-Type": "application/json", "X-Auth-Token": api_key}

        response = requests.get(url, headers=headers, timeout=30)
        assert response.status_code in [200, 201, 204]
        response_json = response.json()

        file_infos = {}
        for entry in response_json:
            name = entry["files"][0]["name"]
            file_infos[name] = {}
            file_infos[name]["identifier"] = name
            file_infos[name]["data_pool_id"] = data_pool_id
            file_infos[name]["data_source_descriptor_id"] = entry["id"]
            file_infos[name]["file_id"] = entry["files"][0]["id"]
        return file_infos
    except Exception as e:
        logger.error("Get data pool file information failed.")
        logger.error(e)
        raise e


def add_data_to_data_pool(data_pool_name: str, file, api_key: str) -> bool:
    """
    The add_data_to_data_pool function adds a data source to the specified data pool.

    Args:
        data_pool_name: str: Specify the name of the data pool
        file: Upload a file to the data pool
        api_key: str: Authenticate the user

    Returns:
        A boolean value

    Doc Author:
        Trelent
    """
    logger.debug("Add data to data pool.")
    try:
        for count in range(10):
            logger.debug("Get pool try: %d", count + 1)
            data_pool = get_data_pool(data_pool_name, api_key)
            if data_pool is not None:
                break
            time.sleep(1)

        assert data_pool is not None
        data_pool_id = data_pool["id"]

        url = f"https://platform.planqk.de/qc-catalog/data-pools/{data_pool_id}/data-source-descriptors"

        headers = {"X-Auth-Token": api_key}

        files = {"file": file}

        response = requests.post(url, headers=headers, files=files, timeout=30)
        result = response.status_code in [200, 201, 204]
        return result
    except Exception as e:
        logger.error("Add data to data pool failed.")
        logger.error(e)
        raise e
