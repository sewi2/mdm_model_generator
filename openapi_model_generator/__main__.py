#!/usr/bin/env python
import json
from argparse import ArgumentParser
from os.path import join
from pathlib import Path

from openapi_model_generator.generators.models.generator import ModelGenerator
from openapi_model_generator.generators.serializers.generator import SerializerGenerator

parser = ArgumentParser(prog=f"{__package__}",
                        description='Generate models and serializers with OpenAPI flatten JSON-file (schema.esb.json)')
parser.add_argument('schema', help="OpenAPI flatten JSON-file (schema.esb.json)")
parser.add_argument('destination', default="../utils/",
                    help="Models and serializers destination directory")

args = parser.parse_args()

with open(args.schema) as fp:
    schema = json.load(fp)

Path(args.destination).mkdir(parents=True, exist_ok=True)

data = [
    # (path, content)
    (join(args.destination, '__init__.py'), ''),
    (join(args.destination, 'base_models.py'), ModelGenerator().generate(schema)),
    (join(args.destination, 'base_serializers.py'), SerializerGenerator().generate(schema)),
]

for path, content in data:
    with open(path, 'w', encoding='utf-8') as file_obj:
        file_obj.write(content)
