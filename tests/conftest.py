import pytest
import uuid

from pyplanqk.low_level_actions import *
from pyplanqk.helpers import *

logger = logging.getLogger("pyplanqk")


@pytest.fixture(autouse=True)
def configure_logger():
    logger_ = logging.getLogger("pyplanqk")

    # Configure your custom logger as desired, e.g., setting log level, formatter, handlers, etc.
    logger_.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(name)s - %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger_.addHandler(stream_handler)

    # Yielding None here means the fixture will only run once before the tests start.
    yield None

    # Clean up the logger after all tests have finished (optional).
    logger_.handlers = []


@pytest.fixture(scope="function")
def api_key():
    api_key = "bb7f15afefee47362632a3f04dfdd8ee2f0fd5403a6588191df9465ddcf3a7d1e5d2339b4f83538af2d9b8b98d7fdd7e"
    api_key = {"apiKey": api_key}
    return api_key


@pytest.fixture(scope="function")
def token_url():
    return "https://gateway.platform.planqk.de/token"


@pytest.fixture(scope="function")
def consumer_key():
    return "wC1Dkq6ZPW7CRBUSB1oL5cURA_ga"


@pytest.fixture(scope="function")
def train_data():
    data = dict()

    data["X_train"] = list()
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))
    data["X_train"].append((0.0, 1.0))

    data["y_train"] = list()
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))
    data["y_train"].append((0.0, 1.0))

    data["X_test"] = list()
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))
    data["X_test"].append((0.0, 1.0))

    data["y_test"] = list()
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))
    data["y_test"].append((0.0, 1.0))


    return data


@pytest.fixture(scope="function")
def train_params():

    params = dict()

    params["mode"] = "train"
    params["encoding"] = "latin-1"
    params["maxiter"] = 3
    params["reps"] = 1

    return params


@pytest.fixture(scope="function")
def config():
    config = dict()
    config["name"] = f"service_{str(uuid.uuid4())}"
    config["description"] = "Service"
    # config["quantum_backend"] = "NONE"
    # config["use_platform_token"] = "FALSE"
    config["milli_cpus"] = 1000
    config["memory_in_megabytes"] = 4096
    config["runtime"] = "PYTHON_TEMPLATE"
    config["gpu_count"] = 0
    config["gpu_accelerator"] = "NONE"
    config["user_code"] = open("data/template.zip", "rb")
    config["api_definition"] = open("data/openapi-spec.yml", "rb")
    return config


@pytest.fixture(scope="function")
def access_token():
    consumer_key = "wC1Dkq6ZPW7CRBUSB1oL5cURA_ga"
    consumer_secret = "o5oiJrJrNLbIuJPGk46vJyHfDj4a"
    token_url = "https://gateway.platform.planqk.de/token"
    access_token = get_access_token(consumer_key, consumer_secret, token_url)
    assert access_token is not None
    assert len(access_token) == 1037
    return access_token


@pytest.fixture(scope="function")
def simple_service(config, api_key: Dict[str, str]):
    service = create_managed_service(config, api_key)
    service_id = service["id"]
    version_id = service["service_definitions"][0]["id"]

    wait_for_service_to_be_created(service_id, version_id, api_key, timeout=500, step=5)

    return service


@pytest.fixture(scope="function")
def internally_published_service(config, api_key: Dict[str, str]):
    service = create_managed_service(config, api_key)
    service_id = service["id"]
    version_id = service["service_definitions"][0]["id"]

    wait_for_service_to_be_created(service_id, version_id, api_key, timeout=500, step=5)

    publish_service_internally(service_id, version_id, api_key)

    return service


@pytest.fixture(scope="function")
def simple_application(api_key: Dict[str, str]):
    application_name = f"application_{str(uuid.uuid4())}"
    application = create_application(application_name, api_key)
    return application


@pytest.fixture(scope="function")
def application_with_auth(api_key: Dict[str, str]):
    application_name = f"application_{str(uuid.uuid4())}"
    application = create_application(application_name, api_key)
    assert application is not None
    print("Enter consumer_key:")
    consumer_key = input()
    print("Enter consumer_secret:")
    consumer_secret = input()
    return application, consumer_key, consumer_secret


@pytest.fixture(scope="function")
def full_application(config, api_key: Dict[str, str]):

    application_name = f"application_{str(uuid.uuid4())}"
    application = create_application(application_name, api_key)
    application_id = application["id"]

    print("Enter consumer_key:")
    consumer_key = input()
    print("Enter consumer_secret:")
    consumer_secret = input()

    service = create_managed_service(config, api_key)

    service_id = service["id"]
    version_id = service["service_definitions"][0]["id"]

    wait_for_service_to_be_created(service_id, version_id, api_key, timeout=500, step=5)

    publish_service_internally(service_id, version_id, api_key)

    subscribe_application_to_service(application_id, service_id, api_key)

    return application, service, consumer_key, consumer_secret


def cleanup_services_and_applications(applications, services, api_key: Dict[str, str]):
    logger.debug("")
    logger.debug("")
    logger.debug("cleanup_services_and_applications")
    for application in applications:
        application_id = application["id"]
        subscriptions = get_all_subscriptions(application_id, api_key)

        for subscription in subscriptions:
            subscription_id = subscription["id"]
            remove_subscription(application_id, subscription_id, api_key)
            logger.debug(f"remove_subscription: {application_id}, {subscription_id}")

        remove_application(application_id, api_key)
        logger.debug(f"remove_application: {application_id}")

    for service in services:
        service_id = service["id"]
        version = get_version(service_id, api_key)
        version_id = version["id"]
        unpublish_service(service_id, version_id, api_key)
        logger.debug(f"unpublish_service: {service_id}, {version_id}")
        remove_service(service_id, api_key)
        logger.debug(f"remove_service: {service_id}")
