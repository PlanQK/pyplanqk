from pyplanqk.low_level_actions import *

logger = logging.getLogger(__name__)



class PyPlanQK:
    def __init__(self, api_key):
        self.api_key = {"apiKey": api_key}
        self.token_url = "https://gateway.platform.planqk.de/token"

    def create_service(self, config: Dict[str, Any]) -> Dict[str, Any]:
        service_name = None
        try:
            service_name = config["name"]
            logger.info(f"Create service: {service_name}.")
            service = get_service(service_name, self.api_key)

            if service is not None:
                logger.info(f"Service: {service_name} already created.")
                return service

            service = create_managed_service(config, self.api_key)

            version = get_version(service_name, self.api_key)
            service_id = service["id"]
            version_id = version["id"]
            wait_for_service_to_be_created(
                service_id, version_id, self.api_key, timeout=500, step=5
            )

            service = get_service(service_name, self.api_key)
            logger.info(f"Service: {service_name} created.")
            return service
        except Exception as e:
            if service_name is not None:
                logger.error(f"Creation of service: {service_name} failed.")
            else:
                logger.error(f"Creation of service failed.")
            logger.error(e)
            raise e

    def execute_service(
        self,
        service_name: str,
        params: Dict[str, Any],
        data: Dict[str, Any] = None,
        data_ref: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        logger.info(f"Execute service: {service_name}.")

        try:
            if data_ref is not None:
                logger.debug(f"triggering serice job with data pool: {data_ref}.")
                job = trigger_service_job(
                    service_name=service_name,
                    api_key=self.api_key,
                    mode="DATA_POOL",
                    data_ref=data_ref,
                    params=params,
                )
            else:
                logger.debug(f"triggering serice job with data upload: {data}.")
                job = trigger_service_job(
                    service_name=service_name,
                    api_key=self.api_key,
                    mode="DATA_UPLOAD",
                    data=data,
                    params=params,
                )

            job_id = job["id"]
            result = get_service_job_result(job_id, self.api_key)
            logger.info(f"Service execution: {service_name} finished.")
            return result
        except Exception as e:
            logger.error(f"Service execution: {service_name} failed.")
            logger.error(e)
            raise e

    def create_data_pool(self, data_pool_name: Optional[str], file) -> Dict[str, Any]:
        logger.info(f"Create data pool: {data_pool_name}...")

       

        try:
            data_pool = get_data_pool(data_pool_name, self.api_key["apiKey"])

            if data_pool is not None:
                logger.info(f"Data pool: {data_pool_name} already created.")
                return data_pool
            logger.debug(f"data pool: {data_pool_name} not found. Creating...")
            print(f"data pool: {data_pool_name} not found. Creating...")

            create_data_pool(data_pool_name, self.api_key["apiKey"])
            logger.debug(f"data pool: {data_pool_name} created. Adding data...")
            add_data_to_data_pool(data_pool_name, file, self.api_key["apiKey"])
            logger.debug(f"data added to data pool")
            file_infos = get_data_pool_file_information(
                data_pool_name, self.api_key["apiKey"]
            )
            file_name = file.name.split(get_path_delimiter)[-1]
            file_info = file_infos[file_name]
            return file_info
        except Exception as e:
            logger.error(f"Creation of data pool: {data_pool_name} failed.")
            logger.error(f"file: {file.name} could not be added to data pool.")
            logger.error(e)
            raise e
