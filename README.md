# Install
Generate openapi client and install dependencies.
````shell
.\install.sh
pip install .
````
In *install.sh* the python client library is generated from the openapi-spec at https://platform.planqk.de/qc-catalog/docs.
Addintionally there are some problems with generating the correct types which are also handled by replacing the lines with the script.

# Test
Install dev dependencies.
````shell
pip install .[dev]
````

Execute tests.
````shell
pytest -s -m MARK --log-cli-level=LOG_LEVEL .
````

Some tests are marked depending on their behavior. Values for **MARK** are defined in the pyproject.toml
- **interactive**: only run tests with user interaction
- **slow_service**: only run tests wich are slow because of the service creation
- **auto**: only run tests that run fully automatic

# Example
## Upload data in the request(payload below 1 Mb)
````python
from pyplanqk import PyPlanQK

# Enter a valid PlanQK API-Key(look at www.planqk.de/settings/access-tokens)
apiKey = "YOUR_PLANQK_API_KEY"
plnqk = pyplanqk.PyPlanQK(api_key)

# Define a fancy service name
service_name = "YOUR_SERVICE_NAME"

# Full config object to define a service
config = {}
config["name"] = service_name
config["user_code"] = open("PATH_TO_TEMPLATE.zip", "rb")
config["api_definition"] = open("PATH_TO_OPENAPI_SPEC.yml", "rb")
config["description"] = "YOUR SERVICE DESCRIPTION"
config["milli_cpus"] = 1000
config["memory_in_megabytes"] = 4096
config["runtime"] = "PYTHON_TEMPLATE"
config["gpu_count"] = 0
config["gpu_accelerator"] = "NONE"

# Trigger the creation of a service with status polling until the service is ready set up
service = plnqk.create_service(config)

# Trigger an execution on your service with your data and params dictionaries
result = plnqk.execute_service(service_name, 
                               data={"k": "v", ...}, 
                               params={"k": "v", ...})
````

## Use data from data pool
````python
from pyplanqk import PyPlanQK

# Enter a valid PlanQK API-Key(look at www.planqk.de/settings/access-tokens)
apiKey = "YOUR_PLANQK_API_KEY"
plnqk = pyplanqk.PyPlanQK(api_key)

# Define a fancy service name
service_name = "YOUR_SERVICE_NAME"

# Define a fancy data pool name
data_pool_name = "YOUR_DATA_POOL_NAME"

# Create a data pool
data_ref = plnqk.create_data_pool(data_pool_name, 
                                  file=open("PATH_TO_YOUR_FILE.json", "rb"))

# Full config object to define a service
config = {}
config["name"] = service_name
config["user_code"] = open("PATH_TO_TEMPLATE.zip", "rb")
config["api_definition"] = open("PATH_TO_OPENAPI_SPEC.yml", "rb")
config["description"] = "YOUR SERVICE DESCRIPTION"
config["milli_cpus"] = 1000
config["memory_in_megabytes"] = 4096
config["runtime"] = "PYTHON_TEMPLATE"
config["gpu_count"] = 0
config["gpu_accelerator"] = "NONE"

# Trigger the creation of a service with status polling until the service is ready set up
service = plnqk.create_service(config)

# Trigger an execution on your service with your data and params dictionaries
result = plnqk.execute_service(service_name, 
                               data_ref=data_ref, 
                               params={"k": "v", ...})
````