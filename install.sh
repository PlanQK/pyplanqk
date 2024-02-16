#!/bin/bash

# Read .env
source .env

# Install openapi-generator-cli globally
npm install -g @openapitools/openapi-generator-cli

# Create and navigate to the generator-output directory
mkdir generator-output && cd generator-output || exit

# Set openapi-generator-cli version to 5.4.0
openapi-generator-cli version-manager set 5.4.0

# Generate Python client using the specified OpenAPI URL
openapi-generator-cli generate -g python -i $PLANQK_OPEN_API_SPEC_URL

# Copy the generated client to the parent directory
cp -R openapi_client ../src

# Navigate back to the parent directory
cd ..

# Remove the generator-output directory
rm -rf generator-output

# Replace faulty openapi generation
echo ""
echo "Replace faulty openapi generation"

# Specify the file path
file_path=("src/openapi_client/api/service_platform___services_api.py")
search_list=("(UNKNOWN_BASE_TYPE,)," "'unknown_base_type':" "from openapi_client.model.unknownbasetype import UNKNOWNBASETYPE")

for search in "${search_list[@]}"; do

    replace="# ${search}"

    echo $search
    echo $replace

    # Find and replace the line
    sed -i "s/${search}/${replace}/" "$file_path"
    echo ""
done
