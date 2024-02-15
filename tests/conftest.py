import uuid
from typing import Tuple

import pytest
from util import *


@pytest.fixture(scope="function")
def api_key() -> Dict[str, str]:
    api_key = "plqk_QNNS83d5b9geIIlYmqnb2yYNv8nmBizJv1oZye5kCS"
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
    return "https://gateway.platform.planqk.de/token"


@pytest.fixture(scope="function")
def consumer_key() -> str:
    return "wC1Dkq6ZPW7CRBUSB1oL5cURA_ga"


@pytest.fixture(scope="function")
def train_data() -> Dict[str, list]:
    return get_data()


@pytest.fixture(scope="function")
def predict_data() -> Dict[str, Any]:
    data = get_data()

    predict_data_ = dict()
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
    config = dict()
    config["name"] = f"service_{str(uuid.uuid4())}"
    config["user_code"] = open(f"{generalTestParameters.testdataPath}template.zip", "rb")
    config["api_definition"] = open(f"{generalTestParameters.testdataPath}openapi-spec.yml", "rb")
    config["description"] = "Service for unit testing."
    config["milli_cpus"] = 1000
    config["memory_in_megabytes"] = 4096
    config["runtime"] = "PYTHON_TEMPLATE"
    config["gpu_count"] = 0
    config["gpu_accelerator"] = "NONE"

    return config


@pytest.fixture(scope="function")
def data_pool(api_key: Dict[str, str]) -> Dict[str, Any]:
    data_pool_name = f"data_pool_{str(uuid.uuid4())}"
    url = "https://platform.planqk.de/qc-catalog/data-pools"

    headers = {"Content-Type": "application/json", "X-Auth-Token": api_key["apiKey"]}

    data = {"name": data_pool_name}

    response = requests.post(url, headers=headers, json=data)
    data_pool = response.json()
    return data_pool


@pytest.fixture(scope="function")
def data_pool_with_data(
    api_key: Dict[str, str], train_data: Dict[str, list], train_params: Dict[str, list]
) -> Dict[str, Any]:
    data_pool_name = f"data_pool_{str(uuid.uuid4())}"
    url = "https://platform.planqk.de/qc-catalog/data-pools"

    headers = {"Content-Type": "application/json", "X-Auth-Token": api_key["apiKey"]}

    data = {"name": data_pool_name}

    response = requests.post(url, headers=headers, json=data)
    data_pool = response.json()

    # save_data(train_data, train_params)

    file = open(f"{generalTestParameters.testdataPath}data.json", "rb")
    result = add_data_to_data_pool(data_pool_name, file, api_key["apiKey"])
    assert result

    return data_pool


@pytest.fixture(scope="function")
def access_token() -> str:
    consumer_key = "wC1Dkq6ZPW7CRBUSB1oL5cURA_ga"
    consumer_secret = "o5oiJrJrNLbIuJPGk46vJyHfDj4a"
    token_url = "https://gateway.platform.planqk.de/token"
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    assert access_token is not None
    assert len(access_token) == 1037
    return access_token


@pytest.fixture(scope="function")
def service_info(
    config: Dict[str, Any], api_key: Dict[str, str]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
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
    application_name = f"application_{str(uuid.uuid4())}"
    application = create_application(application_name, api_key)
    return application


@pytest.fixture(scope="function")
def application_with_auth(api_key: Dict[str, str]) -> Tuple[Dict[str, Any], str, str]:
    application_name = f"application_{str(uuid.uuid4())}"
    application = create_application(application_name, api_key)
    assert application is not None
    print()
    print("Enter consumer_key:")
    consumer_key = input()
    print("Enter consumer_secret:")
    consumer_secret = input()
    return application, consumer_key, consumer_secret


@pytest.fixture(scope="function")
def full_application(
    config: Dict[str, Any], api_key: Dict[str, str]
) -> Tuple[Dict[str, Any], Dict[str, Any], str, str]:
    application_name = f"application_{str(uuid.uuid4())}"
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
def service_job(
    data: Dict[str, Any], params: Dict[str, Any], api_key: Dict[str, str]
) -> JobDto:
    logger.debug("Trigger service job")
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




