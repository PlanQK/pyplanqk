from pyplanqk.low_level_actions import *
from pyplanqk.models import ServiceConfig

logger = logging.getLogger(__name__)


class PyPlanQK:

    def __init__(self, api_key):
        self.api_key = {"apiKey": api_key}
        self.token_url = "https://gateway.platform.planqk.de/token"

    def create_service(self, config: ServiceConfig) -> Optional[ServiceDto]:
        logger.info("Create service...")
        try:
            service = create_managed_service(config.model_dump(), self.api_key)
            assert service is not None

            service_id = service.id
            service_name = service.name
            version = get_version(service_name, self.api_key)
            version_id = version.id
            result = wait_for_service_to_be_created(service_id, version_id, self.api_key, timeout=500, step=5)
            service = get_service(service_name, self.api_key)
            logger.info("Service created.")
            assert service
        except Exception as e:
            service = None
            logger.info(e)
        return service

    def execute_service(self,
                        service_name: str,
                        data: Dict[str, Any],
                        params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        logger.info("Execute service...")
        try:
            service = get_service(service_name, self.api_key)

            service_name = service.name
            job = trigger_service_job(service_name=service_name,
                                      api_key=self.api_key,
                                      data=data,
                                      params=params)
            assert job is not None

            job_id = job["id"]
            result = get_service_job_result(job_id, self.api_key)
            assert result is not None
            logger.info("Service execution finished.")
        except Exception as e:
            result = None
            logger.info(e)
        return result

    def create_data_pool(self, data_pool_name: Optional[str], file) -> Optional[Dict[str, str]]:
        logger.info("Create data pool...")
        try:
            url = "https://platform.planqk.de/qc-catalog/data-pools"

            headers = {
                "Content-Type": "application/json",
                "X-Auth-Token": self.api_key["apiKey"]
            }

            data = {
                "name": data_pool_name
            }

            response = requests.post(url, headers=headers, json=data)
            data_pool = response.json()
            logger.info("Data pool created.")
            assert data_pool is not None

            result = add_data_to_data_pool(data_pool_name, file, self.api_key["apiKey"])
            assert result

        except Exception as e:
            data_pool = None
            logger.info(e)
        return data_pool
