#!/usr/bin/python3
"""This defines the BaseModel class."""
from datetime import datetime
import uuid
import models


class BaseModel:
    """Representation of  the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """This Initialize a new BaseModel.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "updated_at" or key == "created_at":
                    self.__dict__[key] = datetime.fromisoformat(value)
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """This update the updated_at with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """This returns the dictionary of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        dict_new = self.__dict__.copy()
        dict_new["__class__"] = self.__class__.__name__
        dict_new["created_at"] = self.created_at.isoformat()
        dict_new["updated_at"] = self.updated_at.isoformat()
        return dict_new
