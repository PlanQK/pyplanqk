from pyplanqk.low_level_actions import *

from pyplanqk.models import ConfigModel

logger = logging.getLogger("pyplanqk")


class PyPlanQK:

    def __init__(self, api_key):
        """
            Initializes an instance of the ServiceManager class.

            Args:
                api_key (str): The API key to authenticate requests.

            Attributes:
                api_key (dict): A dictionary containing the API key in the format: {"apiKey": api_key}.
                token_url (str): The URL to obtain authentication tokens.
            """
        self.api_key = {"apiKey": api_key}
        self.token_url = "https://gateway.platform.planqk.de/token"

    def create_service(self, config: ConfigModel) -> Optional[ServiceDto]:
        logger.debug("Create service")
        try:
            service = create_managed_service(config.model_dump(), self.api_key)
            assert service is not None

            service_id = service.id
            service_name = service.name
            version = get_version(service_name, self.api_key)
            version_id = version.id
            result = wait_for_service_to_be_created(service_id, version_id, self.api_key, timeout=500, step=5)
            assert result
        except Exception as e:
            service = None
            logger.debug(e)
        return service

    def execute_service(self,
                        service_name: str,
                        data: Dict[str, list],
                        params: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
            Executes a service job with the specified parameters and data.

            Args:
                service_name (str): The name of the service to execute.
                data (Dict[str, list]): A dictionary containing input data for the service job.
                params (Dict[str, str]): A dictionary containing additional parameters for the service job.

            Returns:
                Optional[Dict[str, str]]: A dictionary containing the result of the executed service job,
                or None if execution failed.
            """
        logger.debug("Execute service")
        try:
            service = get_service(service_name, self.api_key)

            service_name = service.name
            job = trigger_service_job(service_name, data, params, self.api_key)
            assert job is not None

            job_id = job["id"]
            result = get_service_job_result(job_id, self.api_key)
            assert result is not None
        except Exception as e:
            result = None
            logger.debug(e)
        return result
