import dataclasses


def dataclass_from_dict(klass, d):
    class_d = {field.name: field.default if field.default !=
               field.default_factory else None for field in dataclasses.fields(klass)}
    return klass(**{**class_d, **d})
