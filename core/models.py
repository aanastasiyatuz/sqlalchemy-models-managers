from .managers import Manager

class ModelBase(type):
    """Meta class for models"""
    def __new__(cls, name, bases, attrs, **kwargs):

        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super().__new__(cls, name, bases, attrs)

        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        manager = Manager()
        manager.model = new_class
        new_class.objects = manager

        return new_class

class Model(metaclass=ModelBase):
    ...