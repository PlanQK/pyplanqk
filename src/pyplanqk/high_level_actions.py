from pyplanqk.low_level_actions import *
from pyplanqk.models import ServiceConfig

logger = logging.getLogger(__name__)


class PyPlanQK:

    def __init__(self, api_key):
        self.api_key = {"apiKey": api_key}
        self.token_url = "https://gateway.platform.planqk.de/token"

    def create_service(self, config: Dict[str, Any]) -> Optional[ServiceDto]:
        logger.info("Create service...")
        try:
            service_name = config["name"]
            service = get_service(service_name, self.api_key)

            if service is not None:
                logger.info("Service already created.")
                return service

            service = create_managed_service(config, self.api_key)
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
                        params: Dict[str, Any],
                        data: Dict[str, Any] = None,
                        data_ref: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        logger.info("Execute service...")
        try:
            service = get_service(service_name, self.api_key)

            service_name = service.name
            if data_ref is not None:
                job = trigger_service_job(service_name=service_name,
                                          api_key=self.api_key,
                                          mode="DATA_POOL",
                                          data_ref=data_ref,
                                          params=params)
            else:
                job = trigger_service_job(service_name=service_name,
                                          api_key=self.api_key,
                                          mode="DATA_UPLOAD",
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

    def create_data_pool(self, data_pool_name: Optional[str], file) -> Optional[Dict[str, Any]]:
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

            file_infos = get_data_pool_file_information(data_pool_name, self.api_key["apiKey"])
            assert file_infos is not None
            file_name = file.name.split("/")[-1]
            file_info = file_infos[file_name]
            return file_info

        except Exception as e:
            file_info = None
            logger.info(e)
        return file_info
