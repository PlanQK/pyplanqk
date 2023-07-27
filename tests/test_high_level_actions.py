import uuid

from pyplanqk.high_level_actions import PyPlanQK
from pyplanqk.low_level_actions import *
from conftest import cleanup_services_and_applications

logger = logging.getLogger("pyplanqk")


def test_create_application_service(config, api_key):
    logger.debug("test_create_application_service")

    try:
        application_name = f"application_{str(uuid.uuid4())}"
        plnqk = PyPlanQK(api_key["apiKey"])
        result = plnqk.create_application_service(config, application_name)
        service = result["service"]
        application = result["application"]
        assert service is not None
        assert application is not None
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)


def test_execute_application_service_train(full_application, api_key, train_data, train_params):
    logger.debug("test_execute_application_service_train")

    try:
        application, service, consumer_key, consumer_secret = full_application
        plnqk = PyPlanQK(api_key["apiKey"])
        service_name = service["name"]
        result = plnqk.execute_application_service(service_name,
                                                   consumer_key,
                                                   consumer_secret,
                                                   train_data,
                                                   train_params)
        assert result
    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)


def test_execute_application_service_predict(full_application, api_key, train_data, train_params):
    logger.debug("test_execute_application_service_predict")

    try:
        application, service, consumer_key, consumer_secret = full_application
        plnqk = PyPlanQK(api_key["apiKey"])
        service_name = service["name"]
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

    except Exception as e:
        logger.debug(e)

    applications = [application]
    services = [service]
    cleanup_services_and_applications(applications, services, api_key)
