from pydantic import BaseModel


class ServiceConfig(BaseModel):
    name: str
    user_code: str
    api_definition: str
    description: str = "Default description."
    milli_cpus: int = 1000
    memory_in_megabytes: int = 4096
    runtime: str = "PYTHON_TEMPLATE"
    gpu_count: int = 0
    gpu_accelerator: str = "NONE"
