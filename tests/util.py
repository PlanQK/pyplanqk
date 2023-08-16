import numpy as np

from pyplanqk.low_level_actions import *

from typing import List, Any

logger = logging.getLogger(__name__)


def cleanup_services_and_applications(applications: List[ApplicationDto],
                                      services: List[ServiceDto],
                                      api_key: Dict[str, str]):
    logger.debug("")
    logger.debug("")
    logger.debug("cleanup_services_and_applications")
    for application in applications:
        application_name = application.name
        subscriptions = get_all_subscriptions(application_name, api_key)

        for _ in subscriptions:
            remove_subscription(application_name, api_key)

        remove_application(application_name, api_key)
        logger.debug(f"remove_application: {application_name}")

    for service in services:
        service_name = service.name
        unpublish_service(service_name, api_key)
        logger.debug(f"unpublish_service: {service_name}")
        remove_service(service_name, api_key)
        logger.debug(f"remove_service: {service_name}")


def label_data(x):
    num_samples = x.shape[0]
    y01 = 1 * (np.sum(x, axis=1) >= 0)
    y_one_hot = np.zeros((num_samples, 2))
    for i in range(num_samples):
        y_one_hot[i, y01[i]] = 1
    return y_one_hot


def save_data(train_data: Dict[str, Any],
              train_params: Dict[str, Any]):
    f = open("data/data.json", "w")
    json.dump(train_data, f)
    f.close()

    f = open("data/params.json", "w")
    json.dump(train_params, f)
    f.close()

    data = dict()
    data["data"] = train_data
    data["params"] = train_params

    f = open("data/train_data.json", "w")
    json.dump(data, f)
    f.close()


def get_params(maxiter=30, reps=1):
    params = dict()

    params["mode"] = "train"
    params["maxiter"] = maxiter
    params["reps"] = reps

    return params


def get_data(num_samples_train=80, num_samples_test=20) -> Dict[str, Any]:
    data = dict()

    x_train = np.random.uniform(-1.0, 1.0, size=(num_samples_train, 2))
    data["X_train"] = x_train.tolist()
    data["y_train"] = label_data(x_train).tolist()

    x_test = np.random.uniform(-1.0, 1.0, size=(num_samples_test, 2))
    data["X_test"] = x_test.tolist()
    data["y_test"] = label_data(x_test).tolist()

    return data
