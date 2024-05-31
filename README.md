# mdm_model_generator

This library allows us to generate django models, drf serializers, filters and viewsets using an OpenAPI schema.

# HowTo Use #
```shell
pip install mdm_model_generator

python -m mdm_model_generator {open_api_path.json} {destination}
```
    
    
As an example:
```shell
python -m mdm_model_generator schema.esb.json base_dir
```

or 

```shell
python -m mdm_model_generator /home/user/schema.esb.json /home/user/base_dir
```

This command creates base models, serializers, filters and viewsets based on its OpenAPI schema into the directory provided.

```shell
pip install mdm_models
```

Then you can use them to define models, serializers, filters and viewsets in your Django+DRF application.

models.py:

```python
from django.db import models
from mdm_models.apps.exploitation import base_models as base_module
from pik.utils.mdm_models import define_missing_classes

define_missing_classes(base_module, locals(), models.Model)
```

serializers.py:

```python
from mdm_models.apps.legal import base_serializers as base_module
from pik.utils.mdm_models import define_serializers

from .. import models as models_module

define_serializers(base_module, locals(), models_module)
```

viewsets.py:

```python
from mdm_models.apps.development import base_viewsets
from pik.utils.mdm_models import define_missing_viewsets

from . import filters
from . import serializers
define_missing_viewsets(locals(), base_viewsets, serializers, filters)
```

filters.py:

```python
from mdm_models.apps.exploitation import base_filters as base_module
from pik.utils.mdm_models import define_filters

from .. import models as models_module

define_filters(base_module, locals(), models_module)
```

After that you can use them:

```python
import pydoc
model_1 = pydoc.locate('{django_app}.models.Model1')
model_2 = pydoc.locate('{django_app}.models.Model2')
...
serializer_1 = pydoc.locate('{django_app}.api_v1.serializers.Model1Serializer')
serializer_2 = pydoc.locate('{django_app}.api_v1.serializers.Model2Serializer')
...
viewset_1 = pydoc.locate('{django_app}.api_v1.viewsets.Model1ViewSet')
viewset_2 = pydoc.locate('{django_app}.api_v1.viewsets.Model2ViewSet')
...
filter_1 = pydoc.locate('{django_app}.api_v1.filters.Model1Filter')
filter_2 = pydoc.locate('{django_app}.api_v1.filters.Model2Filter')
```

# Settings #

You can set one of these settings in your project that uses mdm-models:

```python
MDM_MODELS_CAMEL_CASE = True  # Leave table and its column names as camelCase ones.
MDM_MODELS_BIGINT_ON = True  # Use BigIntegerField instead of simple IntegerField in your models.
MDM_MODELS_HISTORY_ENABLED = False  # Disable historical tables only for mdm_models (removes them if exist).
```
