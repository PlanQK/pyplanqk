import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from pyplanqk.helpers import get_path_delimiter, wait_for_service_to_be_created
from pyplanqk.low_level_actions import (
    add_data_to_data_pool,
    create_data_pool,
    create_managed_service,
    get_data_pool,
    get_data_pool_file_information,
    get_service,
    get_service_job_result,
    get_version,
    trigger_service_job,
)

logger = logging.getLogger(__name__)

load_dotenv(".env")
PLANKQ_TOKEN_URL = os.getenv("PLANKQ_TOKEN_URL")


class PyPlanQK:
    def __init__(self, api_key):
        self.api_key = {"apiKey": api_key}
        self.token_url = PLANKQ_TOKEN_URL

    def create_service(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        The create_service function creates a service on PlanQK.
            Args:
                config (dict): A dictionary containing the configuration for creating a service.

        Args:
            self: Refer to the instance of the class
            config: Dict[str: Pass the configuration of the service to be created
            Any]: Specify the type of the parameter

        Returns:
            A dictionary with the following keys:

        Doc Author:
            Trelent
        """
        service_name = None
        try:
            service_name = config["name"]
            logger.info("Create service: %s.", service_name)
            service = get_service(service_name, self.api_key)

            if service is not None:
                logger.info("Service: %s already created.", service_name)

                return service

            service = create_managed_service(config, self.api_key)

            version = get_version(service_name, self.api_key)
            service_id = service["id"]
            version_id = version["id"]
            wait_for_service_to_be_created(service_id, version_id, self.api_key, timeout=500, step=5)

            service = get_service(service_name, self.api_key)
            logger.info("Service: %s created.", service_name)
            return service
        except Exception as e:
            if service_name is not None:
                logger.error("Creation of service: %s failed.", service_name)
            else:
                logger.error("Creation of service failed.")
            logger.error(e)
            raise e

    def execute_service(
        self,
        service_name: str,
        params: Dict[str, Any],
        data: Dict[str, Any] = None,
        data_ref: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        The execute_service function is used to execute a service.

        Args:
            self: Bind the function to a class
            service_name: str: Specify the name of the service to be executed
            params: Dict[str: Pass the parameters to the service
            Any]: Define the type of data that is passed to the function
            data: Dict[str: Pass the data to be processed by the service
            Any]: Specify the type of data that is returned by the function
            data_ref: Dict[str: Pass the data pool reference
            Any]: Define the type of the data that is passed to the function
            : Pass the service name to the function

        Returns:
            The result of the service execution

        Doc Author:
            Trelent
        """
        logger.info("Execute service: %s.", service_name)

        try:
            if data_ref is not None:
                logger.debug("triggering service job with data pool: %s.", data_ref)
                job = trigger_service_job(
                    service_name=service_name,
                    api_key=self.api_key,
                    mode="DATA_POOL",
                    data_ref=data_ref,
                    params=params,
                )
            else:
                logger.debug("triggering service job with data upload: %s.", data)
                job = trigger_service_job(
                    service_name=service_name,
                    api_key=self.api_key,
                    mode="DATA_UPLOAD",
                    data=data,
                    params=params,
                )

            job_id = job["id"]
            result = get_service_job_result(job_id, self.api_key)
            logger.info("Service execution: %s finished.", service_name)
            return result
        except Exception as e:
            logger.error("Service execution: %s failed.", service_name)
            logger.error(e)
            raise e

    def create_data_pool(self, data_pool_name: Optional[str], file) -> Dict[str, Any]:
        """
        The create_data_pool function creates a data pool with the given name and adds the file to it.
            If a data pool with that name already exists, then it will not be created again.

        Args:
            self: Bind the method to an object
            data_pool_name: Optional[str]: Specify the name of the data pool
            file: Create a data pool

        Returns:
            A dictionary with the following keys:

        Doc Author:
            Trelent
        """
        logger.info("Create data pool: %s...", data_pool_name)

        try:
            data_pool = get_data_pool(data_pool_name, self.api_key["apiKey"])

            if data_pool is not None:
                logger.info("Data pool: %s already created.", data_pool_name)

                return data_pool
            logger.debug("data pool: %s not found. Creating...", data_pool_name)

            create_data_pool(data_pool_name, self.api_key["apiKey"])
            logger.debug("data pool: %s created. Adding data...", data_pool_name)
            add_data_to_data_pool(data_pool_name, file, self.api_key["apiKey"])
            logger.debug("data added to data pool")
            file_infos = get_data_pool_file_information(data_pool_name, self.api_key["apiKey"])
            file_name = file.name.split(get_path_delimiter())[-1]
            file_info = file_infos[file_name]
            return file_info
        except Exception as e:
            logger.error("Creation of data pool: %s failed.", data_pool_name)
            logger.error("file: %s could not be added to data pool.", file.name)
            logger.error(e)
            raise e
