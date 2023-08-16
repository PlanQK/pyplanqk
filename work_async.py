import aiohttp
import asyncio
import uuid


async def send_request():
    print("send_request")
    url = "http://127.0.0.1:8010/services/create_service"
    api_key = "bb7f15afefee47362632a3f04dfdd8ee2f0fd5403a6588191df9465ddcf3a7d1e5d2339b4f83538af2d9b8b98d7fdd7e"
    file_name_user_code = "data/template.zip"
    file_name_api_definition = "data/openapi-spec.yml"

    config = dict()
    config["name"] = f"service_{str(uuid.uuid4())}"
    config["description"] = "Service for unit testing."
    config["milli_cpus"] = 1000
    config["memory_in_megabytes"] = 4096
    config["runtime"] = "PYTHON_TEMPLATE"
    config["gpu_count"] = 0
    config["gpu_accelerator"] = "NONE"

    with open(file_name_user_code, "rb") as user_code_file:
        user_code_data = user_code_file.read()

    with open(file_name_api_definition, "rb") as api_definition_file:
        api_definition_data = api_definition_file.read()

    multipart_data = aiohttp.FormData()
    multipart_data.add_field("api_key", api_key)
    multipart_data.add_field("user_code", user_code_data, filename=file_name_user_code)
    multipart_data.add_field("api_definition", api_definition_data, filename=file_name_api_definition)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=config, data=multipart_data) as response:
            status = response.status
            content = await response.text()

            print("Response Status Code:", status)
            print("Response Content:", content)


loop = asyncio.get_event_loop()
loop.run_until_complete(send_request())
