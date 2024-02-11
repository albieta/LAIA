# LAIA 

LAIA is a Python library that automates the generation of backend Python code and frontend Flutter code based on an OpenAPI description file. 

<span style="color: #808080; font-style: italic;">Please note that LAIA is currently under development, and only the backend functionality is available at the moment.</span>

## Installation

```
pip install laia-gen-lib
```

## Usage

```py
from pymongo import MongoClient
from laiagenlib.main import LaiaFastApi
from laiagenlib.crud.crud_mongo_impl import CRUDMongoImpl
import os

client = MongoClient('mongodb://localhost:27017')

db = client.test

openapi_file_path = os.path.join(os.getcwd(), "api.yaml")

app_instance = LaiaFastApi(openapi_file_path, db, CRUDMongoImpl)

app = app_instance.api
```