import uuid

from pyplanqk.high_level_actions import PyPlanQK
from pyplanqk.low_level_actions import *
from pyplanqk.models import ServiceConfig

from conftest import cleanup_services_and_applications

from typing import Dict, Tuple

logger = logging.getLogger(__name__)


def test_create_service(config: ServiceConfig,
                        api_key: Dict[str, str]):
    print()
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


def test_create_already_created_service(service_info: Tuple[ServiceDto, ServiceConfig],
                                        api_key: Dict[str, str]):
    print()
    logger.debug("test_create_already_created_service")

    simple_service, config = service_info

    applications = []
    services = []

    try:
        plnqk = PyPlanQK(api_key["apiKey"])
        service = plnqk.create_service(config)
        assert service is not None
        assert service.name == config.name
        services.append(service)
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_execute_service_train(config: ServiceConfig,
                               api_key: Dict[str, str],
                               train_data: Dict[str, Any],
                               train_params: Dict[str, Any]):
    print()
    logger.debug("test_execute_service_train")

    applications = []
    services = []

    try:
        plnqk = PyPlanQK(api_key["apiKey"])
        service = plnqk.create_service(config)
        assert service is not None
        services.append(service)

        f = open("data/data.json", "w")
        json.dump(train_data, f)
        f.close()

        f = open("data/params.json", "w")
        json.dump(train_params, f)
        f.close()

        service_name = service.name
        result = plnqk.execute_service(service_name,
                                       train_data,
                                       train_params)
        assert result
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_execute_service_predict(config: ServiceConfig,
                                 api_key: Dict[str, str],
                                 train_data: Dict[str, Any],
                                 train_params: Dict[str, Any],
                                 predict_data: Dict[str, Any],
                                 predict_params: Dict[str, Any]):
    print()
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

        predict_data["model"] = result_json["model"]

        result = plnqk.execute_service(service_name,
                                       predict_data,
                                       predict_params)
        assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_create_datapool(api_key: Dict[str, str]):
    print()
    logger.debug("test_create_datapool")

    try:
        plnqk = PyPlanQK(api_key["apiKey"])
        datapool_name = f"data_pool_{str(uuid.uuid4())}"
        datapool = plnqk.create_datapool(datapool_name)
        assert datapool is not None
    except Exception as e:
        logger.debug(e)
