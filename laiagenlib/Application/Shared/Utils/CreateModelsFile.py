from typing import TypeVar, List
from pydantic import BaseModel
import subprocess
import re
from .ExtractClassInfo import extract_class_info
from .UpdateFile import update_file
from ....Domain.Shared.Utils.logger import _logger

T = TypeVar('T', bound='BaseModel')

def create_models_file(input_file="openapi.yaml", output_file="model.py", models: List[any] = []):
    # This function uses the datamodel-code-generator for generating the pydantic models given a openapi.yaml file. 
    # The generated file is modified so that the pydantic models extend the LaiaBaseModel, this is necessary for 
    # using the Laia library

    subprocess.run(["datamodel-codegen", "--input", input_file, "--output", output_file], check=True)

    import_statement = """
# modified by laia-gen-lib:

from pydantic import ConfigDict
from laiagenlib.models.Model import LaiaBaseModel
from laiagenlib.models.User import LaiaUser"""

    with open(output_file, 'r') as f:
        model_content = f.read()

    lines = model_content.split('\n')
    import_index = next((i for i, line in enumerate(lines) if "from __future__ import annotations" in line), None)

    if import_index is not None:
        lines.insert(import_index + 1, import_statement)

    modified_content = '\n'.join(lines)
    modified_content = re.sub(r'class\s+(\w+)\(BaseModel\):', r'class \1(LaiaBaseModel):', modified_content)

    for model in models:
        if model.get_field_extensions():
            model_config_line = f"model_config = ConfigDict(json_schema_extra={model.get_field_extensions()})"
            modified_content = modified_content.replace(f'class {model.model_name}(LaiaBaseModel):',
                                                        f'class {model.model_name}(LaiaBaseModel):\n    {model_config_line}')
        if model.get_field_extensions() and model.get_field_extensions().get('x-auth'):
            modified_content = modified_content.replace(f'class {model.model_name}(LaiaBaseModel):', f'class {model.model_name}(LaiaUser):', 1)

    with open(output_file, 'w') as f:
        f.write(modified_content)

    with open(output_file, 'r') as f:
        model_content = f.read()

    classes_info = extract_class_info(model_content, models)
    update_file(output_file, classes_info)

    _logger.info(f"File '{output_file}' created and modified.")