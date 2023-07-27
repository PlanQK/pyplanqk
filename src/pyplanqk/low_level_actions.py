import requests
import os
import logging

from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.apis import ServicePlatformApplicationsApi
from openapi_client.configuration import Configuration
from openapi_client.model.create_application_request import CreateApplicationRequest
from openapi_client.model.create_internal_subscription_request import CreateInternalSubscriptionRequest
from typing import Dict

logger = logging.getLogger("pyplanqk")


def create_managed_service(config: Dict[str, str], api_key: Dict[str, str]):
    logger.debug("Create service")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = services_api.create_managed_service(**config)
        logger.debug("Service creation triggered.")
    except Exception as e:
        service = None
        logger.debug("Service creation failed.")
        logger.debug(e)

    return service


def create_application(application_name: str, api_key: Dict[str, str]):
    logger.debug("Create application")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        create_app_request = CreateApplicationRequest(name=application_name)
        application = applications_api.create_application(create_application_request=create_app_request)
        logger.debug("Application created.")
    except Exception as e:
        application = None
        logger.debug("Create application failed.")
        logger.debug(e)

    return application


def publish_service_internally(service_id: str, version_id: str, api_key: Dict[str, str]):
    logger.debug("Publish service internally")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = services_api.publish_service_internal(service_id, version_id)
        logger.debug("Service published internally")
    except Exception as e:
        service = None
        logger.debug("Service publishing failed")
        logger.debug(e)

    return service


def unpublish_service(service_id: str, version_id: str, api_key: Dict[str, str]):
    logger.debug("Unpublish service")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = services_api.unpublish_service(service_id, version_id)
        logger.debug("Service unpublished")
    except Exception as e:
        service = None
        logger.debug("Service unpublishing failed")
        logger.debug(e)

    return service


def remove_service(service_id: str, api_key: Dict[str, str]):
    logger.debug("Remove service")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        services_api.delete_service(service_id)
        response = ""
        logger.debug("Service removed")
    except Exception as e:
        response = None
        logger.debug("Service removing failed")
        logger.debug(e)

    return response


def remove_application(application_id: str, api_key: Dict[str, str]):
    logger.debug("Remove application")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        applications_api.delete_application(application_id)
        response = ""
        logger.debug("Application removed")
    except Exception as e:
        response = None
        logger.debug("Application removing failed")
        logger.debug(e)

    return response


def remove_subscription(application_id: str, subscription_id: str, api_key: Dict[str, str]):
    logger.debug("Remove subscription")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        applications_api.delete_application_subscription(application_id, subscription_id)
        response = ""
        logger.debug("Subscription removed")
    except Exception as e:
        response = None
        logger.debug("Subscription removal failed")
        logger.debug(e)

    return response


def subscribe_application_to_service(application_id: str, service_id: str, api_key: Dict[str, str]):
    logger.debug("Subscribe application to service")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        subscription_request = CreateInternalSubscriptionRequest(application_id=application_id,
                                                                 service_id=service_id)
        applications_api.create_internal_subscription(
            id=application_id,
            create_internal_subscription_request=subscription_request
        )
        response = ""
        logger.debug("Application subscribed")
    except Exception as e:
        response = None
        logger.debug("Application subscription failed")
        logger.debug(e)

    return response


def get_application(application_name: str, api_key: Dict[str, str]):
    logger.debug("Get application")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        applications = applications_api.get_applications()

        found_application = None
        for application in applications:
            if application_name == application["name"]:
                found_application = application
    except Exception as e:
        found_application = None
        logger.debug("Application retrieval failed")
        logger.debug(e)

    return found_application


def get_service(service_name: str, api_key: Dict[str, str], lifecycle: str = "CREATED"):
    logger.debug("Get service")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        services = services_api.get_services(lifecycle=lifecycle)

        found_service = None
        for service in services:
            if service_name == service["name"]:
                found_service = service
    except Exception as e:
        found_service = None
        logger.debug("Service retrieval failed")
        logger.debug(e)

    return found_service


def get_version(service_id: str, api_key: Dict[str, str]):
    logger.debug("Get version")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    try:
        service = services_api.get_service(service_id)
    except Exception as e:
        service = None
        logger.debug("Version retrieval failed")
        logger.debug(e)

    return service["service_definitions"][0]


def get_all_subscriptions(application_id: str, api_key: Dict[str, str]):
    logger.debug("Get subscriptions")

    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    applications_api = ServicePlatformApplicationsApi(api_client=api_client)

    try:
        subscriptions = applications_api.get_application_subscriptions(application_id)
    except Exception as e:
        subscriptions = None
        logger.debug("Subscriptions retrieval failed")
        logger.debug(e)

    return subscriptions


def get_access_token(consumer_key: str, consumer_secret, token_url: str):
    logger.debug("Get access_token")
    data = {'grant_type': 'client_credentials'}

    try:
        response = requests.post(token_url,
                                 data=data,
                                 verify=False,
                                 allow_redirects=False,
                                 auth=(consumer_key, consumer_secret))

        json_response = response.json()
        return json_response["access_token"]
    except Exception as e:
        logger.debug("Get access_token failed")
        logger.debug(e)
        return None


def get_all_service_jobs(service_id: str, api_key: Dict[str, str]):
    logger.debug("Get all service jobs")
    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    services_api = ServicePlatformServicesApi(api_client=api_client)

    version = get_version(service_id, api_key)
    version_id = version["id"]
    jobs = services_api.get_managed_service_executions(service_id, version_id)

    return jobs


def get_service_job(service_id: str, job_id: str, api_key: Dict[str, str]):
    logger.debug("Get service job")
    jobs = get_all_service_jobs(service_id, api_key)

    for job in jobs:
        if job["id"] == job_id:
            return job

    return None


def trigger_application_execution(service_id: str, data, params, access_token: str, api_key: Dict[str, str]):
    logger.debug("Trigger application execution")
    try:
        version = get_version(service_id, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/"

        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "data": data,
            "params": params
        }

        response = requests.post(service_endpoint, json=payload, headers=headers)
        json_response = response.json()
        return json_response
    except Exception as e:
        logger.debug(e)
        return None


def cancel_service_job(job_id: str, api_key: Dict[str, str]):
    raise NotImplementedError("This feature is not implemented yet.")


def delete_service_job(job_id: str, api_key: Dict[str, str]):
    raise NotImplementedError("This feature is not implemented yet.")


def start_service_job(job_id: str, api_key: Dict[str, str]):
    raise NotImplementedError("This feature is not implemented yet.")


def get_service_job_logs(job_id: str, api_key: Dict[str, str]):
    raise NotImplementedError("This feature is not implemented yet.")


def get_application_job_info(service_id: str, job_id: str, access_token: str, api_key: Dict[str, str]):
    logger.debug("Get application job info")
    try:
        version = get_version(service_id, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = os.path.join(service_endpoint, job_id)
        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(service_endpoint, headers=headers)
        json_response = response.json()
        return json_response
    except Exception as e:
        logger.debug(e)
        return None


def get_application_job_status(service_id: str, job_id: str, access_token: str, api_key: Dict[str, str]):
    logger.debug("Get application job status")
    try:
        version = get_version(service_id, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = os.path.join(service_endpoint, job_id)
        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(service_endpoint, headers=headers)
        json_response = response.json()
        status = json_response["status"]
        return status
    except Exception as e:
        logger.debug(e)
        return None


def get_application_job_result(service_id: str, job_id: str, access_token: str, api_key: Dict[str, str]):
    logger.debug("Get application job result")
    try:
        version = get_version(service_id, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = os.path.join(service_endpoint, job_id, "result")
        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(service_endpoint, headers=headers)
        json_response = response.json()
        result = json_response["result"]
        return result
    except Exception as e:
        logger.debug(e)
        return None
