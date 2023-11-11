#!/usr/bin/python3
"""This defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """This Represent an amenity.
    Attributes:
        name (str): The name of the amenity.
    """

    name = ""
