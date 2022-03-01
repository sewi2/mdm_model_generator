from os.path import join, dirname

from .generator import Generator


class SerializerGenerator:
    TEMPLATES = join(dirname(__file__), 'templates')

    def __init__(self, schema: dict):
        self._schema = schema
        self._generator = Generator(self.TEMPLATES, schema)

    def generate(self):  # noqa: pylint=arguments-differ
        return self._generator.generate('base_serializers')
