# Install
````shell
.\install.sh
pip install .
````
In *install.sh* the python client library is generated from the openapi-spec at https://platform.planqk.de/qc-catalog/docs.
Addintionally there are some problems with generating the correct types which are also handled by replacing the lines with the script.

# Test
````shell
pytest -s -m MARK .
````

Values for **MARK** are defined in the pyproject.toml
- **interactive**: only run tests with user interaction
- **slow_service**: only run tests wich are slow because of the service creation
- **auto**: only run tests that run fully automatic

By setting **log_cli_level** to **DEBUG** you get a finer logging output.