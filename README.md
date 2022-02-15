# mdm_model_generator

This library allows us to generate django models and drf serializers using an OpenAPI schema.

# HowTo Use #
    pip install mdm_model_generator

    python -m mdm_model_generator {open_api_path.json} {destination}
    python -m mdm_model_generator {open_api_path.yaml} {destination}
    
As an example:

    python -m mdm_model_generator schema.esb.json mdm_models

or 
    
    python -m mdm_model_generator /home/user/schema.esb.json /home/user/mdm_models

