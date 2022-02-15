from os.path import join, dirname

from .generator import Generator
from .utils import create_directory, write_if_not_exists


class SerializerGenerator:
    TEMPLATES = join(dirname(__file__), 'templates')

    def __init__(self, schema: str, destination: str):
        self._schema = schema
        self._destination = destination
        self._generator = Generator(self.TEMPLATES, schema)

    def generate(self):  # noqa: pylint=arguments-differ
        create_directory(self._destination)
        data = [
            # tuple((path, content, force,))
            (join(self._destination, '__init__.py'), '', False,),
            (join(self._destination, 'base_serializers.py'), self._generator.generate('base_serializers'), True,),
            (join(self._destination, 'serializers.py'), self._generator.generate('serializers'), True,),
        ]
        for write_data in data:
            write_if_not_exists(*write_data)
