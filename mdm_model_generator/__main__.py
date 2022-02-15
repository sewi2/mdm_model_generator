#!/usr/bin/env python

from argparse import ArgumentParser

from .schema_to_models import ModelGenerator
from .schema_to_serializers import SerializerGenerator

parser = ArgumentParser(prog=f"{__package__}",
                        description='Generate models and serializers with OpenAPI flatten JSON-file (schema.esb.json)')
parser.add_argument('schema', help="OpenAPI flatten JSON-file (schema.esb.json)")
parser.add_argument('destination', default="../mdm_models/",
                    help="Models and serializers destination directory")

args = parser.parse_args()

ModelGenerator(args.schema, args.destination).generate()
SerializerGenerator(args.schema, args.destination).generate()
