from rest_framework import serializers

def no_empty_validator(value: str):
    if not isinstance(value, str):
        raise serializers.ValidationError({"comment": ["This field must be an string"]})
    return str(value)