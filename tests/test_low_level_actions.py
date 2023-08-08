import uuid

from pyplanqk.low_level_actions import *
from conftest import cleanup_services_and_applications
from pyplanqk.helpers import *
from typing import Tuple

logger = logging.getLogger("pyplanqk")


def test_create_managed_service(config: Dict[str, str],
                                api_key: Dict[str, str]):
    logger.debug("test_create_managed_service")
    applications = []
    services = []

    try:
        service = create_managed_service(config, api_key)
        assert type(service) == ServiceDto
        services.append(service)
        assert service is not None
        service_id = service.id
        service_name = service.name
        version = get_version(service_name, api_key)
        version_id = version.id
        wait_for_service_to_be_created(service_id, version_id, api_key, timeout=500, step=5)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_create_application(api_key: Dict[str, str]):
    logger.debug("test_create_application")
    applications = []
    services = []

    try:
        application_name = f"application_{str(uuid.uuid4())}"
        application = create_application(application_name, api_key)
        assert type(application) == ApplicationDto
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_application(api_key: Dict[str, str],
                         simple_application: ServiceDto):
    logger.debug("test_get_application")
    simple_application, consumer_key, consumer_secret = simple_application
    applications = [simple_application]
    services = []
    try:
        application_name = simple_application.name
        application = get_application(application_name, api_key)
        assert type(application) == ApplicationDto
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_remove_application(api_key: Dict[str, str],
                            simple_application: ApplicationDto):
    logger.debug("test_remove_application")
    applications = [simple_application]
    services = []
    try:
        application_name = simple_application.name
        result = remove_application(application_name, api_key)
        assert result
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_remove_service(api_key: Dict[str, str],
                        simple_service: ServiceDto):
    logger.debug("test_remove_service")
    applications = []
    services = [simple_service]
    try:
        service_name = simple_service.name
        result = remove_service(service_name, api_key)
        assert result
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_services(api_key: Dict[str, str],
                     simple_service: ServiceDto):
    logger.debug("test_get_services")
    applications = []
    services = [simple_service]
    try:
        services = get_services(api_key)
        assert services is not None
        assert len(services) >= 1
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_service(api_key: Dict[str, str],
                     simple_service: ServiceDto):
    logger.debug("test_get_service")
    applications = []
    services = [simple_service]
    try:
        service_name = simple_service.name
        service = get_service(service_name, api_key)
        assert service is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_version(api_key: Dict[str, str],
                     simple_service: ServiceDto):
    logger.debug("test_get_version")
    applications = []
    services = [simple_service]
    try:
        service_name = simple_service.name
        service = get_service(service_name, api_key)
        service_id = service.id
        version = get_version(service_id, api_key)
        assert version is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_publish_service_internally(api_key: Dict[str, str],
                                    simple_service: ServiceDto):
    logger.debug("test_publish_service_internally")
    applications = []
    services = [simple_service]
    try:
        service_name = simple_service.name
        service = get_service(service_name, api_key, lifecycle="CREATED")
        service_id = service.id
        version = get_version(service_id, api_key)
        version_id = version.id
        application = publish_service_internally(service_id, version_id, api_key)
        assert application is not None
        unpublish_service(service_id, version_id, api_key)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_unpublish_service(api_key: Dict[str, str],
                           internally_published_service: ServiceDto):
    logger.debug("test_unpublish_service")
    applications = []
    services = [internally_published_service]
    try:
        service_name = internally_published_service.name
        unpublish_service(service_name, api_key)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_subscribe_application_to_service(api_key: Dict[str, str],
                                          full_application):
    logger.debug("test_subscribe_application_to_service")
    application, service, consumer_key, consumer_secret = full_application
    applications = [application]
    services = [service]
    try:
        application_name = application.name
        service_name = service.name
        result = subscribe_application_to_service(application_name, service_name, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_all_subscriptions(api_key: Dict[str, str],
                               full_application):
    logger.debug("test_get_all_subscriptions")
    application, service, consumer_key, consumer_secret = full_application
    applications = [application]
    services = [service]
    try:
        application_name = application.name
        service_id = service.id
        subscriptions = get_all_subscriptions(application_name, api_key)
        assert subscriptions is not None
        service_ids = [subscription.api.service_id for subscription in subscriptions]
        assert service_id in service_ids
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_access_token(application_with_auth: Tuple[ApplicationDto, str, str],
                          token_url: str):
    logger.debug("test_get_access_token")
    application, consumer_key, consumer_secret = application_with_auth
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    logger.debug(access_token)
    assert access_token is not None
    assert len(access_token) == 1037


def test_get_all_service_jobs(simple_service: ServiceDto,
                              api_key: Dict[str, str]):
    logger.debug("test_get_all_service_jobs")
    applications = []
    services = [simple_service]
    try:
        logger.debug("test_get_all_service_jobs")
        service_name = simple_service.name
        jobs = get_all_service_jobs(service_name, api_key)
        assert len(jobs) == 0
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_remove_subscription(api_key: Dict[str, str],
                             full_application: Tuple[ApplicationDto, ServiceDto, str, str]):
    logger.debug("test_remove_subscription")
    application, service, consumer_key, consumer_secret = full_application
    applications = [application]
    services = [service]
    try:
        application_name = application.name
        service_name = service.name
        result = subscribe_application_to_service(application_name, service_name, api_key)
        assert result is not None
        subscriptions = get_all_subscriptions(application_name, api_key)

        for _ in subscriptions:
            result = remove_subscription(application_name, api_key)
            assert result
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_trigger_application_job_train(full_application: Tuple[ApplicationDto, ServiceDto, str, str],
                                       api_key: Dict[str, str],
                                       token_url: str,
                                       train_data: Dict[str, list],
                                       train_params: Dict[str, str]):
    logger.debug("test_trigger_application_execution")
    application, service, consumer_key, consumer_secret = full_application
    applications = [application]
    services = [service]
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    try:
        service_name = service.name
        application_name = application.name
        result = subscribe_application_to_service(application_name, service_name, api_key)
        assert result
        job = trigger_application_job(
            service_name, train_data, train_params, access_token, api_key)
        status = job["status"]
        job_id = job["id"]
        assert status in ["PENDING", "SUCCEEDED"]

        version = get_version(service_name, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/{job_id}"
        result = wait_for_application_job_to_be_finished(service_endpoint, access_token)
        assert result
        result = get_application_job_result(service_name, job_id, access_token, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_trigger_application_job_predict(full_application: Tuple[ApplicationDto, ServiceDto, str, str],
                                         api_key: Dict[str, str],
                                         token_url: str,
                                         train_data: Dict[str, list],
                                         train_params: Dict[str, str]):
    logger.debug("test_trigger_application_execution")
    application, service, consumer_key, consumer_secret = full_application
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    applications = [application]
    services = [service]
    try:
        service_name = service.name
        application_name = application.name
        result = subscribe_application_to_service(application_name, service_name, api_key)
        assert result is not None
        job = trigger_application_job(
            service_name, train_data, train_params, access_token, api_key)
        status = job["status"]
        job_id = job["id"]
        assert status in ["PENDING", "SUCCEEDED"]

        version = get_version(service_name, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/{job_id}"
        result = wait_for_application_job_to_be_finished(service_endpoint, access_token)
        assert result
        result = get_application_job_result(service_name, job_id, access_token, api_key)
        assert result is not None

        model = result["model"]

        predict_data = dict()
        predict_data["model"] = model
        predict_data["x"] = [train_data["X_test"][0]]

        predict_params = train_params
        predict_params["mode"] = "predict"

        job = trigger_application_job(
            service_name, predict_data, predict_params, access_token, api_key)
        status = job["status"]
        job_id = job["id"]
        assert status in ["PENDING", "SUCCEEDED"]

        version = get_version(service_name, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/{job_id}"
        result = wait_for_application_job_to_be_finished(service_endpoint, access_token)
        assert result
        result = get_application_job_result(service_name, job_id, access_token, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_trigger_service_job_train(simple_service: ServiceDto,
                                   train_data: Dict[str, list],
                                   train_params: Dict[str, str],
                                   api_key: Dict[str, str],
                                   timeout: int,
                                   step: int):
    logger.debug("test_trigger_service_job_train")
    try:
        service_name = simple_service.name
        job = trigger_service_job(service_name, train_data, train_params, api_key, timeout=timeout, step=step)
        print(job)
        assert job is not None
        assert job.status == "SUCCEEDED"
        print(job.result)
    except Exception as e:
        logger.debug(e)
