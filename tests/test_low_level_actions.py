import uuid

from pyplanqk.low_level_actions import *
from conftest import cleanup_services_and_applications
from pyplanqk.helpers import *

logger = logging.getLogger("pyplanqk")


def test_create_managed_service(api_key: Dict[str, str]):
    logger.debug("test_create_managed_service")
    try:
        config = dict()
        config["name"] = f"service_{str(uuid.uuid4())}"
        config["description"] = "Service"
        # config["quantum_backend"] = "NONE"
        # config["use_platform_token"] = "FALSE"
        config["milli_cpus"] = 1000
        config["memory_in_megabytes"] = 4096
        config["runtime"] = "PYTHON_TEMPLATE"
        config["gpu_count"] = 0
        config["gpu_accelerator"] = "NONE"
        config["user_code"] = open("data/template.zip", "rb")
        config["api_definition"] = open("data/openapi-spec.yml", "rb")

        service = create_managed_service(config, api_key)
        assert service is not None
    except Exception as e:
        logger.debug(e)

    applications = []
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)


def test_create_application(api_key: Dict[str, str]):
    logger.debug("test_create_application")
    try:
        application_name = f"application_{str(uuid.uuid4())}"
        application = create_application(application_name, api_key)
        assert application is not None
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = []
    cleanup_services_and_applications(applications, services, api_key)


def test_get_application(api_key: Dict[str, str], simple_application):
    logger.debug("test_get_application")
    simple_application, consumer_key, consumer_secret = simple_application
    try:
        application_name = simple_application["name"]
        application = get_application(application_name, api_key)
        assert application is not None
    except Exception as e:
        logger.debug(e)

    applications = [simple_application]
    services = []
    cleanup_services_and_applications(applications, services, api_key)


def test_remove_application(api_key: Dict[str, str], simple_application):
    logger.debug("test_remove_application")
    try:
        application_id = simple_application["id"]
        result = remove_application(application_id, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

        applications = [simple_application]
        services = []
        cleanup_services_and_applications(applications, services, api_key)


def test_remove_service(api_key: Dict[str, str], simple_service):
    logger.debug("test_remove_service")
    try:
        service_id = simple_service["id"]
        result = remove_service(service_id, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

        applications = []
        services = [simple_service]
        cleanup_services_and_applications(applications, services, api_key)


def test_get_service(api_key: Dict[str, str], simple_service):
    logger.debug("test_get_service")
    try:
        service_name = simple_service["name"]
        service = get_service(service_name, api_key, lifecycle="ACCESSIBLE")
        assert service is not None
    except Exception as e:
        logger.debug(e)

    applications = []
    services = [simple_service]
    cleanup_services_and_applications(applications, services, api_key)


def test_get_version(api_key: Dict[str, str], simple_service):
    logger.debug("test_get_version")
    try:
        service_name = simple_service["name"]
        service = get_service(service_name, api_key, lifecycle="CREATED")
        service_id = service["id"]
        version = get_version(service_id, api_key)
        assert version is not None
    except Exception as e:
        logger.debug(e)

    applications = []
    services = [simple_service]
    cleanup_services_and_applications(applications, services, api_key)


def test_publish_service_internally(api_key: Dict[str, str], simple_service):
    logger.debug("test_publish_service_internally")
    try:
        service_name = simple_service["name"]
        service = get_service(service_name, api_key, lifecycle="CREATED")
        service_id = service["id"]
        version = get_version(service_id, api_key)
        version_id = version["id"]
        application = publish_service_internally(service_id, version_id, api_key)
        assert application is not None
        unpublish_service(service_id, version_id, api_key)
    except Exception as e:
        logger.debug(e)

    applications = []
    services = [simple_service]
    cleanup_services_and_applications(applications, services, api_key)


def test_unpublish_service(api_key: Dict[str, str], internally_published_service: Dict[str, str]):
    logger.debug("test_unpublish_service")
    try:
        service_id = internally_published_service["id"]
        version = get_version(service_id, api_key)
        version_id = version["id"]
        unpublish_service(service_id, version_id, api_key)
    except Exception as e:
        logger.debug(e)

    applications = []
    services = [internally_published_service]
    cleanup_services_and_applications(applications, services, api_key)


def test_subscribe_application_to_service(api_key: Dict[str, str],
                                          full_application):
    logger.debug("test_subscribe_application_to_service")
    application, service, consumer_key, consumer_secret = full_application
    try:
        application_id = application["id"]
        service_id = service["id"]
        result = subscribe_application_to_service(application_id, service_id, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)


def test_get_all_subscriptions(api_key: Dict[str, str],
                               full_application):
    logger.debug("test_get_all_subscriptions")
    application, service, consumer_key, consumer_secret = full_application
    try:
        application_id = application["id"]
        service_id = service["id"]
        result = subscribe_application_to_service(application_id, service_id, api_key)
        assert result is not None
        subscriptions = get_all_subscriptions(application_id, api_key)
        assert subscriptions is not None
        service_ids = [subscription["api"]["service_id"] for subscription in subscriptions]
        assert service_id in service_ids
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)


def test_get_access_token(application_with_auth, token_url: str):
    logger.debug("test_get_access_token")
    application, consumer_key, consumer_secret = application_with_auth
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    logger.debug(access_token)
    assert access_token is not None
    assert len(access_token) == 1037


def test_get_all_service_jobs(simple_service, api_key: Dict[str, str]):
    try:
        logger.debug("test_get_all_service_jobs")
        service_id = simple_service["id"]
        jobs = get_all_service_jobs(service_id, api_key)
        assert len(jobs) == 0
    except Exception as e:
        logger.debug(e)

    applications = []
    services = [simple_service]
    cleanup_services_and_applications(applications, services, api_key)


# def test_get_service_job(generic_service: Dict[str, str], api_key: Dict[str, str]):
#     logger.debug("test_get_service_job")
#     service_id = generic_service["id"]
#     job_id = "c58d0972-7a3b-4e64-9cc6-3e9512a36d09"
#     job = get_service_job(service_id, job_id, api_key)
#     assert job is None
#
#
# def test_get_application_job_info(access_token: str, api_key: Dict[str, str]):
#     logger.debug("test_get_application_job_info")
#     service_id = "17bb1f36-75bd-447b-8e75-608a5a9a70e2"
#     job_id = "c58d0972-7a3b-4e64-9cc6-3e9512a36d09"
#     info = get_application_job_info(service_id, job_id, access_token, api_key)
#     logger.debug(info)
#     assert info is not None
#
#
# def test_get_application_job_status(access_token: str, api_key: Dict[str, str]):
#     logger.debug("test_get_application_job_status")
#     service_id = "17bb1f36-75bd-447b-8e75-608a5a9a70e2"
#     job_id = "c58d0972-7a3b-4e64-9cc6-3e9512a36d09"
#     status = get_application_job_status(service_id, job_id, access_token, api_key)
#     logger.debug(status)
#     assert status is not None


def test_remove_subscription(api_key: Dict[str, str],
                             full_application):
    logger.debug("test_remove_subscription")
    application, service, consumer_key, consumer_secret = full_application
    try:
        application_id = application["id"]
        service_id = service["id"]
        result = subscribe_application_to_service(application_id, service_id, api_key)
        assert result is not None
        subscriptions = get_all_subscriptions(application_id, api_key)

        for subscription in subscriptions:
            subscription_id = subscription["id"]
            result = remove_subscription(application_id, subscription_id, api_key)
            assert result is not None
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)


def test_trigger_application_execution_train(full_application,
                                             api_key: Dict[str, str],
                                             token_url: str,
                                             train_data,
                                             train_params):
    logger.debug("test_trigger_application_execution")
    application, service, consumer_key, consumer_secret = full_application
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    try:
        service_id = service["id"]
        application_id = application["id"]
        result = subscribe_application_to_service(application_id, service_id, api_key)
        assert result is not None
        job = trigger_application_execution(service_id, train_data, train_params, access_token, api_key)
        status = job["status"]
        job_id = job["id"]
        assert status in ["PENDING", "SUCCEEDED"]

        version = get_version(service_id, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/{job_id}"
        result = wait_for_execution_to_be_finished(service_endpoint, access_token)
        assert result
        result = get_application_job_result(service_id, job_id, access_token, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)


def test_trigger_application_execution_predict(full_application,
                                               api_key: Dict[str, str],
                                               token_url: str,
                                               train_data,
                                               train_params):
    logger.debug("test_trigger_application_execution")
    application, service, consumer_key, consumer_secret = full_application
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    try:
        service_id = service["id"]
        application_id = application["id"]
        result = subscribe_application_to_service(application_id, service_id, api_key)
        assert result is not None
        job = trigger_application_execution(service_id, train_data, train_params, access_token, api_key)
        status = job["status"]
        job_id = job["id"]
        assert status in ["PENDING", "SUCCEEDED"]

        version = get_version(service_id, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/{job_id}"
        result = wait_for_execution_to_be_finished(service_endpoint, access_token)
        assert result
        result = get_application_job_result(service_id, job_id, access_token, api_key)
        assert result is not None

        model = result["model"]

        predict_data = dict()
        predict_data["model"] = model
        predict_data["x"] = [train_data["X_test"][0]]

        predict_params = train_params
        predict_params["mode"] = "predict"

        job = trigger_application_execution(service_id, predict_data, predict_params, access_token, api_key)
        status = job["status"]
        job_id = job["id"]
        assert status in ["PENDING", "SUCCEEDED"]

        version = get_version(service_id, api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/{job_id}"
        result = wait_for_execution_to_be_finished(service_endpoint, access_token)
        assert result
        result = get_application_job_result(service_id, job_id, access_token, api_key)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)
