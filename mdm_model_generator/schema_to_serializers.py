from os.path import join, dirname
from pathlib import Path

from .generator import Generator


class SerializerGenerator:
    TEMPLATES = join(dirname(__file__), 'templates')

    def __init__(self, schema: str, destination: str):
        self._schema = schema
        self._destination = destination
        self._generator = Generator(self.TEMPLATES, schema)

    def generate(self):  # noqa: pylint=arguments-differ
        Path(self._destination).mkdir(parents=True, exist_ok=True)
        data = [
            (join(self._destination, '__init__.py'), ''),
            (join(self._destination, 'base_serializers.py'), self._generator.generate('base_serializers')),
        ]
        for path, content in data:
            with open(path, 'w', encoding="utf-8") as file_obj:
                file_obj.write(content)
