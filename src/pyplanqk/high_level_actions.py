from pyplanqk.low_level_actions import *
from pyplanqk.helpers import *

logger = logging.getLogger("pyplanqk")


class PyPlanQK:

    def __init__(self, api_key):
        self.api_key = {"apiKey": api_key}
        self.token_url = "https://gateway.platform.planqk.de/token"

    def create_application_service(self, config, application_name: str):
        try:
            # create service
            service = create_managed_service(config, self.api_key)
            assert service is not None

            service_id = service["id"]
            version_id = service["service_definitions"][0]["id"]
            result = wait_for_service_to_be_created(service_id, version_id, self.api_key, timeout=500, step=5)
            assert result is not None

            # publish service
            service_id = service["id"]
            version_id = service["service_definitions"][0]["id"]
            result = publish_service_internally(service_id, version_id, self.api_key)
            assert result is not None

            # get application
            application = get_application(application_name, self.api_key)
            if application is None:
                # OPTIONAL: create application
                application = create_application(application_name, self.api_key)
                assert application is not None

            # subscribe application to service
            application_id = application["id"]
            result = subscribe_application_to_service(application_id, service_id, self.api_key)
            assert result is not None

            result = dict()
            result["service"] = service
            result["application"] = application

            return result
        except Exception as e:
            logger.debug(e)
            return None

    def execute_application_service(self,
                                    service_name: str,
                                    consumer_key: str,
                                    consumer_secret: str,
                                    data,
                                    params):
        service = get_service(service_name, self.api_key, lifecycle="ACCESSIBLE")
        access_token = get_access_token(consumer_key, consumer_secret, self.token_url)

        service_id = service["id"]
        job = trigger_application_execution(service_id, data, params, access_token, self.api_key)
        assert job is not None

        job_id = job["id"]
        version = get_version(service_id, self.api_key)
        service_endpoint = version.gateway_endpoint
        service_endpoint = f"{service_endpoint}/{job_id}"
        result = wait_for_execution_to_be_finished(service_endpoint, access_token)
        assert result

        result = get_application_job_result(service_id, job_id, access_token, self.api_key)
        assert result is not None

        return result
