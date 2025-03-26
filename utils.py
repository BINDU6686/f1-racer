from pydantic import BaseModel

from f1_racer.constants import Operator


def get_query_builder_options(attr_type):
    operators = Operator
    attribute_type = attr_type
    return {'attributes': attribute_type, 'operators': operators}
    


def cast_attribute_value(attribute: str, attr_value: str, model_class: BaseModel):
    """
    Casts the attr_value to the type defined for the attribute in the given model class.

    Parameters:
    - attribute (str): The name of the attribute to cast.
    - attr_value (str): The value to be cast.
    - model_class (BaseModel): The Pydantic model class to reference for field types.

    Returns:
    - Any: The casted value.
    
    Raises:
    - ValueError: If the attribute type is unsupported or casting fails.
    """
    # Get the expected type of the attribute from the model
    expected_type = model_class.__annotations__.get(attribute)
    if expected_type is None:
        raise ValueError(f"Attribute '{attribute}' is not valid for the model '{model_class.__name__}'.")

    try:
        # Perform type casting
        if expected_type is int:
            return int(attr_value)
        elif expected_type is float:
            return float(attr_value)
        elif expected_type is str:
            return str(attr_value)
        else:
            raise ValueError(f"Unsupported type for attribute '{attribute}': {expected_type}")
    except ValueError as e:
        raise ValueError(f"Error casting value '{attr_value}' to type '{expected_type.__name__}': {e}")
