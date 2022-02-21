# mdm_model_generator

This library allows us to generate django models and drf serializers using an OpenAPI schema.

# HowTo Use #
```shell
pip install mdm_model_generator

python -m mdm_model_generator {open_api_path.json} {destination}
python -m mdm_model_generator {open_api_path.yaml} {destination}
```
    
    
As an example:
```shell
python -m mdm_model_generator schema.esb.json base_dir
```

or 

```shell
python -m mdm_model_generator /home/user/schema.esb.json /home/user/base_dir
```

This command creates base models and serializers based on its models into the directory provided.

Then you can use them to define models and serializers in your Django+DRF application.

models.py:

```python
from mdm_models import define_models

from base_dir import base_models


define_models(['Model1', 'Model2', ...], base_models, locals())
```

serializers.py:

```python
from mdm_models import define_serializers

from base_dir import base_serializers
from . import models


define_serializers(['Model1', 'Model2', ...], base_serializers, locals(), models)
```

After that you can use them:

```python
import pydoc
model_1 = pydoc.locate('{django_app}.models.Model1')
model_2 = pydoc.locate('{django_app}.models.Model2')
...
serializer_1 = pydoc.locate('{django_app}.serializers.Model1Serializer')
serializer_2 = pydoc.locate('{django_app}.serializers.Model2Serializer')
```
