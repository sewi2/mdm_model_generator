from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mdm_model_generator',
    packages=find_packages(),
    version='0.1.9',
    license='MIT',
    description='This library allows us to generate django models and drf serializers using an OpenAPI schema',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dmitry Nikolaev',
    author_email='sewi0018@gmail.com',
    url='https://github.com/sewi2/mdm_model_generator',
    download_url='https://github.com/sewi2/mdm_model_generator/archive/refs/tags/0.1.9.tar.gz',
    keywords=['mdm', 'models', 'serializers', 'generator', ],
    install_requires=[
        'jinja2',
        'django',
        'prance',
        'openapi_spec_validator',
        'djangorestframework',
        'djangorestframework-camel-case',
    ],
    dependency_links=['https://github.com/pik-software/pik-django-utils.git@rabbit-test#egg=pik_django_utils'],
    include_package_data=True,
    python_requires='~=3.6',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        '5 - Production/Stable',

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
