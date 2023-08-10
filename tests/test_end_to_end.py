import uuid

import numpy as np

from pyplanqk.high_level_actions import PyPlanQK
from pyplanqk.low_level_actions import *
from conftest import cleanup_services_and_applications
from typing import Dict

from conftest import get_data, get_params, get_config

logger = logging.getLogger("pyplanqk")


def test_service_job(api_key: Dict[str, str]):
    logger.debug("test_service_job")
    applications = []
    services = []

    try:
        train_data = get_data(num_samples_train=800, num_samples_test=200)
        train_params = get_params(maxiter=100, reps=3)

        config = get_config(name=f"service_{str(uuid.uuid4())}",
                            description="Service for end to end unit testing.",
                            user_code="data/template.zip",
                            api_definition="data/openapi-spec.yml")

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

        predict_params = train_params
        predict_params["mode"] = "predict"

        for i in range(3):
            idx = np.random.randint(0, len(train_data["X_test"]))
            predict_data["x"] = [train_data["X_test"][idx]]
            result = plnqk.execute_service(service_name,
                                           predict_data,
                                           predict_params)
            assert result is not None
    except Exception as e:
        logger.debug(e)

    cleanup_services_and_applications(applications, services, api_key)
