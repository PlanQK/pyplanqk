import uuid

from pyplanqk.high_level_actions import PyPlanQK
from pyplanqk.low_level_actions import *
from conftest import cleanup_services_and_applications
from typing import Tuple, Dict

logger = logging.getLogger("pyplanqk")


def test_create_application_service(config: Dict[str, str],
                                    api_key: Dict[str, str]):
    logger.debug("test_create_application_service")
    applications = []
    services = []

    try:
        application_name = f"application_{str(uuid.uuid4())}"
        plnqk = PyPlanQK(api_key["apiKey"])
        service, application = plnqk.create_application_service(
            config, application_name)
        assert type(service) == ServiceDto
        assert type(application) == ApplicationDto
        applications.append(application)
        services.append(service)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_execute_application_service_train(full_application: Tuple[ApplicationDto, ServiceDto, str, str],
                                           api_key: Dict[str, str],
                                           train_data: Dict[str, list],
                                           train_params: Dict[str, str]):
    logger.debug("test_execute_application_service_train")
    application, service, consumer_key, consumer_secret = full_application
    applications = [application]
    services = [service]

    try:
        plnqk = PyPlanQK(api_key["apiKey"])
        service_name = service.name
        result = plnqk.execute_application_service(service_name,
                                                   consumer_key,
                                                   consumer_secret,
                                                   train_data,
                                                   train_params)
        assert result
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_execute_application_service_predict(full_application: Tuple[ApplicationDto, ServiceDto, str, str],
                                             api_key: Dict[str, str],
                                             train_data: Dict[str, list],
                                             train_params: Dict[str, str]):
    logger.debug("test_execute_application_service_predict")
    applications = []
    services = []

    try:
        application, service, consumer_key, consumer_secret = full_application
        plnqk = PyPlanQK(api_key["apiKey"])
        service_name = service.name
        result = plnqk.execute_application_service(service_name,
                                                   consumer_key,
                                                   consumer_secret,
                                                   train_data,
                                                   train_params)
        assert result is not None

        model = result["model"]

        predict_data = dict()
        predict_data["model"] = model
        predict_data["x"] = [train_data["X_test"][0]]

        predict_params = train_params
        predict_params["mode"] = "predict"

        result = plnqk.execute_application_service(service_name,
                                                   consumer_key,
                                                   consumer_secret,
                                                   predict_data,
                                                   predict_params)
        assert result is not None
        applications.append(application)
        services.append(service)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)
