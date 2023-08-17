import uuid

from pyplanqk.high_level_actions import PyPlanQK
from pyplanqk.low_level_actions import *

from conftest import cleanup_services_and_applications

from typing import Dict, Tuple

logger = logging.getLogger(__name__)


def test_create_service(config: Dict[str, Any],
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
        cleanup_services_and_applications(applications, services, api_key)
    except Exception as e:
        logger.debug(e)
        assert False


def test_create_already_created_service(service_info: Tuple[Dict[str, Any], Dict[str, Any]],
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
        assert service["name"] == config["name"]
        services.append(service)
        cleanup_services_and_applications(applications, services, api_key)
    except Exception as e:
        logger.debug(e)
        assert False


def test_execute_service_train_data_upload(config: Dict[str, Any],
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

        service_name = service["name"]
        result = plnqk.execute_service(service_name,
                                       data=train_data,
                                       params=train_params)
        assert result is not None
        cleanup_services_and_applications(applications, services, api_key)
    except Exception as e:
        logger.debug(e)
        assert False


def test_execute_service_train_data_pool(data_pool_with_data: Dict[str, Any],
                                         config: Dict[str, Any],
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

        f = open("data/params.json", "w")
        json.dump(train_params, f)
        f.close()

        service_name = service["name"]
        data_pool_name = data_pool_with_data["name"]
        file_infos = get_data_pool_file_information(data_pool_name, api_key["apiKey"])

        train_data = file_infos["data.json"]

        result = plnqk.execute_service(service_name,
                                       data_ref=train_data,
                                       params=train_params)
        assert result is not None
        cleanup_services_and_applications(applications, services, api_key)
    except Exception as e:
        logger.debug(e)
        assert False


def test_execute_service_predict(config: Dict[str, Any],
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

        service_name = service["name"]
        result_json = plnqk.execute_service(service_name,
                                            data=train_data,
                                            params=train_params)
        assert result_json is not None

        predict_data["model"] = result_json["model"]

        result = plnqk.execute_service(service_name,
                                       data=predict_data,
                                       params=predict_params)
        assert result is not None
        cleanup_services_and_applications(applications, services, api_key)
        assert True
    except Exception as e:
        logger.debug(e)
        assert False


def test_create_data_pool(api_key: Dict[str, str]):
    print()
    logger.debug("test_create_datapool")

    try:
        file = open("data/data.json", "rb")

        plnqk = PyPlanQK(api_key["apiKey"])
        data_pool_name = f"data_pool_{str(uuid.uuid4())}"
        file_info = plnqk.create_data_pool(data_pool_name, file)
        assert file_info is not None

        if data_pool_name is not None:
            remove_data_pool(data_pool_name, api_key["apiKey"])
        assert True
    except Exception as e:
        logger.debug(e)
        assert False
