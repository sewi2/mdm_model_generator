#!/usr/bin/env python
import json
from argparse import ArgumentParser
from os.path import join
from pathlib import Path

from .schema_to_models import ModelGenerator
from .schema_to_serializers import SerializerGenerator

parser = ArgumentParser(prog=f"{__package__}",
                        description='Generate models and serializers with OpenAPI flatten JSON-file (schema.esb.json)')
parser.add_argument('schema', help="OpenAPI flatten JSON-file (schema.esb.json)")
parser.add_argument('destination', default="../mdm_models/",
                    help="Models and serializers destination directory")

args = parser.parse_args()

with open(args.schema) as fp:
    schema = json.load(fp)

Path(args.destination).mkdir(parents=True, exist_ok=True)

data = [
    # (path, content)
    (join(args.destination, '__init__.py'), ''),
    (join(args.destination, 'base_models.py'), ModelGenerator(schema).generate()),
    (join(args.destination, 'base_serializers.py'), SerializerGenerator(schema).generate()),
]

for path, content in data:
    with open(path, 'w', encoding='utf-8') as file_obj:
        file_obj.write(content)
