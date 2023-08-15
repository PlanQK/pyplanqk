import uuid
import json
import logging
import pyplanqk

from conftest import cleanup_services_and_applications
from conftest import get_data, get_params, get_config
from pyplanqk.low_level_actions import remove_data_pool

from typing import Dict


logger = logging.getLogger(__name__)


def test_service_job_from_data_upload(api_key: Dict[str, str]):
    print()
    logger.debug("test_service_job_from_data_upload")

    applications = []
    services = []

    try:
        train_data = get_data(num_samples_train=800, num_samples_test=200)
        train_params = get_params(maxiter=100, reps=3)

        config = get_config(name=f"service_{str(uuid.uuid4())}",
                            description="Service for end to end unit testing.",
                            user_code="data/template.zip",
                            api_definition="data/openapi-spec.yml")

        plnqk = pyplanqk.PyPlanQK(api_key["apiKey"])
        service = plnqk.create_service(config.model_dump())
        assert service is not None
        services.append(service)

        service_name = service.name
        result_json = plnqk.execute_service(service_name,
                                            data=train_data,
                                            params=train_params)
        assert result_json is not None

        result = result_json["result"]
        model = result["model"]

        predict_data = dict()
        predict_data["model"] = model

        predict_params = train_params
        predict_params["mode"] = "predict"

        for i in range(3):
            predict_data["x"] = [train_data["X_test"][0]]
            result = plnqk.execute_service(service_name,
                                           data=predict_data,
                                           params=predict_params)
            assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)


def test_service_job_from_data_pool(api_key: Dict[str, str]):
    print()
    logger.debug("test_service_job_from_data_pool")

    applications = []
    services = []

    try:
        train_data = get_data(num_samples_train=800, num_samples_test=200)
        f_data = open("/tmp/data.json", "w")
        json.dump(train_data, f_data)
        f_data.close()

        f_data = open("/tmp/data.json", "rb")

        train_params = get_params(maxiter=100, reps=3)

        config = get_config(name=f"service_{str(uuid.uuid4())}",
                            description="Service for end to end unit testing.",
                            user_code="data/template.zip",
                            api_definition="data/openapi-spec.yml")

        plnqk = pyplanqk.PyPlanQK(api_key["apiKey"])

        data_pool_name = f"data_pool_{str(uuid.uuid4())}"
        data_ref = plnqk.create_data_pool(data_pool_name, file=f_data)
        assert data_ref

        service = plnqk.create_service(config.model_dump())
        assert service is not None
        services.append(service)

        service_name = service.name
        result_json = plnqk.execute_service(service_name,
                                            data_ref=data_ref,
                                            params=train_params)
        assert result_json is not None

        result = result_json["result"]
        model = result["model"]

        predict_data = dict()
        predict_data["model"] = model

        predict_params = train_params
        predict_params["mode"] = "predict"

        for i in range(3):
            predict_data["x"] = [train_data["X_test"][0]]
            result = plnqk.execute_service(service_name,
                                           data=predict_data,
                                           params=predict_params)
            assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)

    if data_pool_name is not None:
        remove_data_pool(data_pool_name, api_key["apiKey"])
