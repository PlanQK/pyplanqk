import uuid

from typing import Tuple

from util import *

from openapi_client.models import *

logger = logging.getLogger(__name__)


def test_create_managed_service(config: ConfigModel,
                                api_key: Dict[str, str]):
    print()
    logger.debug("test_create_managed_service")
    applications = []
    services = []

    try:
        service = create_managed_service(config.model_dump(), api_key)
        assert service is not None
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
    print()
    logger.debug("test_create_application")
    applications = []
    services = []

    try:
        application_name = f"application_{str(uuid.uuid4())}"
        application = create_application(application_name, api_key)
        assert application is not None
        applications.append(application)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_application(api_key: Dict[str, str],
                         simple_application: ApplicationDto):
    print()
    logger.debug("test_get_application")
    applications = [simple_application]
    services = []
    try:
        application_name = simple_application.name
        application = get_application(application_name, api_key)
        assert application is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_remove_application(api_key: Dict[str, str],
                            simple_application: ApplicationDto):
    print()
    logger.debug("test_remove_application")
    applications = []
    services = []
    try:
        application_name = simple_application.name
        result = remove_application(application_name, api_key)
        assert result
    except Exception as e:
        logger.debug(e)
        applications.append(simple_application)

    cleanup_services_and_applications(applications, services, api_key)


def test_remove_service(api_key: Dict[str, str],
                        simple_service: ServiceDto):
    print()
    logger.debug("test_remove_service")
    applications = []
    services = []
    try:
        service_name = simple_service.name
        result = remove_service(service_name, api_key)
        assert result
    except Exception as e:
        logger.debug(e)
        services.append(simple_service)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_services(api_key: Dict[str, str],
                      simple_service: ServiceDto):
    print()
    logger.debug("test_get_services")
    applications = []
    services = [simple_service]
    try:
        services_ = get_services(api_key)
        assert services_ is not None
        assert len(services_) >= 1
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_service(api_key: Dict[str, str],
                     simple_service: ServiceDto):
    print()
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
    print()
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
    print()
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
    print()
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
    print()
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
    print()
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
                          token_url: str,
                          api_key: Dict[str, str]):
    print()
    logger.debug("test_get_access_token")

    application, consumer_key, consumer_secret = application_with_auth

    applications = [application]
    services = []

    try:
        access_token = get_access_token(consumer_key, consumer_secret, token_url)
        assert access_token is not None
        assert len(access_token) == 1037
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_get_all_service_jobs_for_service(simple_service: ServiceDto,
                                          api_key: Dict[str, str]):
    print()
    logger.debug("test_get_all_service_jobs_for_service")
    applications = []
    services = [simple_service]
    try:
        service_name = simple_service.name
        jobs = get_all_service_jobs_for_service(service_name, api_key)
        assert len(jobs) == 0
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_remove_subscription(api_key: Dict[str, str],
                             full_application: Tuple[ApplicationDto, ServiceDto, str, str]):
    print()
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
    print()
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
                                         train_params: Dict[str, str],
                                         predict_data: Dict[str, list],
                                         predict_params: Dict[str, str]):
    print()
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

        predict_data["model"] = result["model"]
        predict_params = train_params

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


def test_trigger_service_job_data_upload_train(simple_service: ServiceDto,
                                               train_data: Dict[str, Any],
                                               train_params: Dict[str, Any],
                                               api_key: Dict[str, str],
                                               timeout: int,
                                               step: int):
    print()
    logger.debug("test_trigger_service_job_data_upload_train")

    applications = []
    services = [simple_service]

    try:
        service_name = simple_service.name
        job = trigger_service_job(service_name=service_name,
                                  data=train_data,
                                  params=train_params,
                                  api_key=api_key,
                                  mode="DATA_UPLOAD",
                                  timeout=timeout,
                                  step=step)
        assert job is not None
        assert job.status == "SUCCEEDED"
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_trigger_service_job_data_pool_train(data_pool_with_data: Dict[str, Any],
                                             train_params: Dict[str, Any],
                                             simple_service: ServiceDto,
                                             api_key: Dict[str, str],
                                             timeout: int,
                                             step: int):
    print()
    logger.debug("test_trigger_service_job_data_pool_train")

    applications = []
    services = [simple_service]

    try:
        service_name = simple_service.name
        data_pool_name = data_pool_with_data["name"]
        file_infos = get_data_pool_file_information(data_pool_name, api_key["apiKey"])

        train_data = file_infos["data.json"]

        job = trigger_service_job(service_name=service_name,
                                  api_key=api_key,
                                  data_ref=train_data,
                                  params=train_params,
                                  mode="DATA_POOL",
                                  timeout=timeout,
                                  step=step)
        assert job is not None
        assert job.status == "SUCCEEDED"
    except Exception as e:
        logger.debug(e)

    data_pool_name = data_pool_with_data["name"]
    remove_data_pool(data_pool_name, api_key["apiKey"])
    cleanup_services_and_applications(applications, services, api_key)


def test_get_data_pools(api_key: Dict[str, str]):
    print()
    logger.debug("test_get_data_pools")
    try:
        data_pools = get_data_pools(api_key["apiKey"])
        assert data_pools is not None
        assert len(data_pools) >= 0
    except Exception as e:
        logger.debug(e)


def test_create_data_pool(api_key: Dict[str, str]):
    print()
    logger.debug("test_create_data_pool")
    try:
        data_pool_name = f"datapool_{str(uuid.uuid4())}"
        data_pool = create_data_pool(data_pool_name, api_key["apiKey"])
        assert data_pool is not None
    except Exception as e:
        data_pool = None
        data_pool_name = None
        logger.debug(e)

    if data_pool is not None:
        remove_data_pool(data_pool_name, api_key["apiKey"])


def test_remove_data_pool(data_pool: Dict[str, str],
                          api_key: Dict[str, str]):
    print()
    logger.debug("test_remove_data_pool")
    try:
        data_pool_name = data_pool["name"]
        result = remove_data_pool(data_pool_name, api_key["apiKey"])
        assert result
    except Exception as e:
        data_pool_name = None
        logger.debug(e)

    if data_pool_name is not None:
        remove_data_pool(data_pool_name, api_key["apiKey"])


def test_add_data_to_data_pool(data_pool: Dict[str, str],
                               api_key: Dict[str, str]):
    print()
    logger.debug("test_add_data_to_data_pool")
    try:
        data_pool_name = data_pool["name"]
        file = open("data/data.json", "rb")
        result = add_data_to_data_pool(data_pool_name, file, api_key["apiKey"])
        assert result

        file = open("data/params.json", "rb")
        result = add_data_to_data_pool(data_pool_name, file, api_key["apiKey"])
        assert result

    except Exception as e:
        data_pool_name = None
        logger.debug(e)

    if data_pool_name is not None:
        remove_data_pool(data_pool_name, api_key["apiKey"])


def test_get_data_pool_file_information(data_pool_with_data: Dict[str, str],
                                        api_key: Dict[str, str]):
    print()
    logger.debug("test_get_data_pool_file_information")
    try:
        data_pool_name = "data_pool_134faedb-8d91-487a-90e0-0b81972e82ae"
        file_infos = get_data_pool_file_information(data_pool_name, api_key["apiKey"])
        assert file_infos is not None

        for k, v in file_infos.items():
            print(k, v)

    except Exception as e:
        data_pool_name = None
        logger.debug(e)

    if data_pool_name is not None:
        remove_data_pool(data_pool_name, api_key["apiKey"])


def test_remove_all_service_jobs(api_key: Dict[str, str]):
    print()
    logger.debug("test_remove_all_service_jobs")
    jobs = get_all_service_jobs(api_key)

    for job in jobs:
        result = remove_service_job(job["id"], api_key)
        assert result


def test_save_data(train_data, train_params):
    print()
    logger.debug("test_save_data")
    save_data(train_data, train_params)
