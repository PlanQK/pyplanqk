import json
import os
from typing import Any, Dict, Tuple

import pytest
import requests
from dotenv import load_dotenv
from names_generator import generate_name
from util import get_data, get_params, get_test_data_path

from openapi_client import ApiClient, Configuration
from openapi_client.api.service_platform___jobs_api import ServicePlatformJobsApi
from openapi_client.model.create_job_request import CreateJobRequest
from openapi_client.model.job_dto import JobDto
from pyplanqk.helpers import wait_for_service_to_be_created
from pyplanqk.low_level_actions import (
    add_data_to_data_pool,
    create_application,
    create_managed_service,
    get_access_token,
    publish_service_internally,
    subscribe_application_to_service,
)

load_dotenv(".env")
PLANKQ_API_KEY = os.getenv("PLANKQ_API_KEY")
PLANKQ_TOKEN_URL = os.getenv("PLANKQ_API_KEY")
PLANQK_DATA_POOL_URL = os.getenv("PLANQK_DATA_POOL_URL")


@pytest.fixture(scope="function")
def api_key() -> Dict[str, str]:
    api_key = PLANKQ_API_KEY
    api_key = {"apiKey": api_key}
    return api_key


@pytest.fixture(scope="function")
def timeout() -> int:
    return 500


@pytest.fixture(scope="function")
def step() -> int:
    return 15


@pytest.fixture(scope="function")
def token_url() -> str:
    return PLANKQ_TOKEN_URL


@pytest.fixture(scope="function")
def consumer_key() -> str:
    return "wC1Dkq6ZPW7CRBUSB1oL5cURA_ga"


@pytest.fixture(scope="function")
def train_data() -> Dict[str, list]:
    return get_data()


@pytest.fixture(scope="function")
def predict_data() -> Dict[str, Any]:
    data = get_data()

    predict_data_ = {}
    predict_data_["model"] = None
    predict_data_["x"] = [data["X_test"][0]]

    return predict_data_


@pytest.fixture(scope="function")
def train_params() -> Dict[str, Any]:
    return get_params()


@pytest.fixture(scope="function")
def predict_params() -> Dict[str, Any]:
    params = get_params()
    params["mode"] = "predict"
    return params


@pytest.fixture(scope="function")
def config() -> Dict[str, Any]:
    config = {}
    config["name"] = f"service_{generate_name()}"
    config["user_code"] = open("tests/data/template.zip", "rb")
    config["api_definition"] = open("tests/data/openapi-spec.yml", "rb")
    config["description"] = "Service for unit testing."
    config["milli_cpus"] = 1000
    config["memory_in_megabytes"] = 4096
    config["runtime"] = "PYTHON_TEMPLATE"
    config["gpu_count"] = 0
    config["gpu_accelerator"] = "NONE"

    return config


@pytest.fixture(scope="function")
def data_pool(api_key: Dict[str, str]) -> Dict[str, Any]:
    data_pool_name = f"data_pool_{generate_name()}"
    url = PLANQK_DATA_POOL_URL

    headers = {"Content-Type": "application/json", "X-Auth-Token": api_key["apiKey"]}

    data = {"name": data_pool_name}

    response = requests.post(url, headers=headers, json=data)
    data_pool = response.json()
    return data_pool


@pytest.fixture(scope="function")
def data_pool_with_data(
    api_key: Dict[str, str], train_data: Dict[str, list], train_params: Dict[str, list]
) -> Dict[str, Any]:
    data_pool_name = f"data_pool_{generate_name()}"
    url = PLANQK_DATA_POOL_URL

    headers = {"Content-Type": "application/json", "X-Auth-Token": api_key["apiKey"]}

    data = {"name": data_pool_name}

    response = requests.post(url, headers=headers, json=data)
    data_pool = response.json()

    # save_data(train_data, train_params)

    file = open(f"{get_test_data_path()}data.json", "rb")
    result = add_data_to_data_pool(data_pool_name, file, api_key["apiKey"])
    assert result

    return data_pool


@pytest.fixture(scope="function")
def access_token() -> str:
    consumer_key = "wC1Dkq6ZPW7CRBUSB1oL5cURA_ga"
    consumer_secret = "o5oiJrJrNLbIuJPGk46vJyHfDj4a"
    token_url = PLANKQ_TOKEN_URL
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    assert access_token is not None
    assert len(access_token) == 1037
    return access_token


@pytest.fixture(scope="function")
def service_info(config: Dict[str, Any], api_key: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    service = create_managed_service(config, api_key)
    service_id = service["id"]
    version_id = service["service_definitions"][0]["id"]

    wait_for_service_to_be_created(service_id, version_id, api_key, timeout=500, step=5)

    return service, config


@pytest.fixture(scope="function")
def internally_published_service(
    service_info: Tuple[Dict[str, Any], Dict[str, Any]], api_key: Dict[str, str]
) -> Dict[str, Any]:
    simple_service, config = service_info

    service_name = simple_service["name"]

    publish_service_internally(service_name, api_key)

    return simple_service


@pytest.fixture(scope="function")
def simple_application(api_key: Dict[str, str]) -> Dict[str, Any]:
    application_name = f"application_{generate_name()}"
    application = create_application(application_name, api_key)
    return application


@pytest.fixture(scope="function")
def application_with_auth(api_key: Dict[str, str]) -> Tuple[Dict[str, Any], str, str]:
    application_name = f"application_{generate_name()}"
    application = create_application(application_name, api_key)
    assert application is not None
    print()
    print("Enter consumer_key:")
    consumer_key = input()
    print("Enter consumer_secret:")
    consumer_secret = input()
    return application, consumer_key, consumer_secret


@pytest.fixture(scope="function")
def full_application(config: Dict[str, Any], api_key: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, Any], str, str]:
    application_name = f"application_{generate_name()}"
    application = create_application(application_name, api_key)
    print()
    print("Enter consumer_key:")
    consumer_key = input()
    print("Enter consumer_secret:")
    consumer_secret = input()

    service = create_managed_service(config, api_key)

    service_name = service["name"]
    service_id = service["id"]
    version_id = service["service_definitions"][0]["id"]

    wait_for_service_to_be_created(service_id, version_id, api_key, timeout=500, step=5)

    publish_service_internally(service_name, api_key)

    subscribe_application_to_service(application_name, service_name, api_key)

    return application, service, consumer_key, consumer_secret


@pytest.fixture(scope="function")
def service_job(data: Dict[str, Any], params: Dict[str, Any], api_key: Dict[str, str]) -> JobDto:
    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration=configuration)
    service_jobs_api = ServicePlatformJobsApi(api_client=api_client)

    create_job_request = CreateJobRequest(
        service_definition_id="596ffd0c-2551-4564-83f6-851f64078497",
        input_data=json.dumps(data),
        parameters=json.dumps(params),
        serviceDefinition="596ffd0c-2551-4564-83f6-851f64078497",
        persist_result=True,
    )
    job = service_jobs_api.create_job(create_job_request=create_job_request)
    return job
