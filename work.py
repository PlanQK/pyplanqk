import uuid
import requests

url = "http://127.0.0.1:8010/services/create_service"
api_key = "bb7f15afefee47362632a3f04dfdd8ee2f0fd5403a6588191df9465ddcf3a7d1e5d2339b4f83538af2d9b8b98d7fdd7e"
file_name_user_code = "data/template.zip"
file_name_api_definition = "data/openapi-spec.yml"

with open(file_name_user_code, "rb") as user_code_file:
    user_code = user_code_file.read()

with open(file_name_api_definition, "rb") as api_definition_file:
    api_definition = api_definition_file.read()

config = dict()
config["name"] = f"service_{str(uuid.uuid4())}"
config["description"] = "Service for unit testing."
config["milli_cpus"] = 1000
config["memory_in_megabytes"] = 4096
config["runtime"] = "PYTHON_TEMPLATE"
config["gpu_count"] = 0
config["gpu_accelerator"] = "NONE"

multipart_data = {
    "api_key": (None, api_key),
    "user_code": (file_name_user_code, user_code),
    "api_definition": (file_name_api_definition, api_definition)
}

response = requests.post(url, params=config, files=multipart_data)

print("Response Status Code:", response.status_code)
print("Response Content:", response.text)

