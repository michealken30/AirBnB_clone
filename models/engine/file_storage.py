#!/usr/bin/python3
"""This defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """This Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """This Set in __objects obj with key <obj_class_name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """It serializes __objects to the JSON file __file_path."""
        with open(self.__file_path, "w", encoding="utf-8") as j:
            od = {y: z.to_dict() for y, z in self.__objects.items()}
            json.dump(od, j)

    def reload(self):
        """It Deserialize the JSON file __file_path to __objects,
        if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as j:
                dict_obj = json.load(j)
                for k in dict_obj.values():
                    class_name = k["__class__"]
                    del k["__class__"]
                    self.new(eval(f"{class_name}")(**k))
        except FileNotFoundError:
            return
