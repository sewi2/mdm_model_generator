import os

from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = [
        line.rstrip(f'{os.linesep}') for line in f.readlines()
        if line and not line.startswith(('#', '-e', 'git+'))
    ]

setup(
    name='mdm_model_generator',
    packages=find_packages(),
    version='__VERSION__',
    license='MIT',
    description=(
        'This library allows us to generate django '
        'models and drf serializers, filtersets and viewsets'
        ' using an OpenAPI schema'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dmitry Nikolaev',
    author_email='nikolaevdd@pik.ru',
    entry_points={
        'console_scripts': [
            'mdm_model_generator=mdm_model_generator.__main__:main'
        ],
    },
    keywords=['mdm', 'models', 'serializers',
              'filtersets', 'viewsets', 'generator', ],
    install_requires=requirements,
    include_package_data=True,
    python_requires='~=3.6',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
