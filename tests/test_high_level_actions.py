from pyplanqk.high_level_actions import PyPlanQK
from pyplanqk.low_level_actions import *
from conftest import cleanup_services_and_applications
from typing import Dict

from pyplanqk.models import ConfigModel

logger = logging.getLogger("pyplanqk")


def test_create_service(config: ConfigModel,
                        api_key: Dict[str, str]):
    logger.debug("test_create_service")
    applications = []
    services = []

    try:
        plnqk = PyPlanQK(api_key["apiKey"])
        service = plnqk.create_service(config)
        assert service is not None
        services.append(service)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_execute_service_train(config: ConfigModel,
                               api_key: Dict[str, str],
                               train_data: Dict[str, list],
                               train_params: Dict[str, str]):
    logger.debug("test_execute_service_train")

    applications = []
    services = []

    try:
        plnqk = PyPlanQK(api_key["apiKey"])
        service = plnqk.create_service(config)
        assert service is not None
        services.append(service)

        service_name = service.name
        result = plnqk.execute_service(service_name,
                                       train_data,
                                       train_params)
        assert result
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_execute_service_predict(config: ConfigModel,
                                 api_key: Dict[str, str],
                                 train_data: Dict[str, list],
                                 train_params: Dict[str, str]):
    logger.debug("test_execute_service_predict")
    applications = []
    services = []

    try:
        plnqk = PyPlanQK(api_key["apiKey"])
        service = plnqk.create_service(config)
        assert service is not None
        services.append(service)

        service_name = service.name
        result_json = plnqk.execute_service(service_name,
                                            train_data,
                                            train_params)
        assert result_json is not None

        result = result_json["result"]
        model = result["model"]

        predict_data = dict()
        predict_data["model"] = model
        predict_data["x"] = [train_data["X_test"][0]]

        predict_params = train_params
        predict_params["mode"] = "predict"

        result = plnqk.execute_service(service_name,
                                       predict_data,
                                       predict_params)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)
