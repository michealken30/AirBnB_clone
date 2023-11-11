#!/usr/bin/python3
"""This Defines the HBnB console."""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """This Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = ["BaseModel",
                 "User",
                 "State",
                 "City",
                 "Amenity",
                 "Place",
                 "Review"]

    def do_quit(self, line):
        """This Quit command helps to exit the program."""
        return True

    def do_EOF(self, line):
        """This is an EOF signal to exit the program."""
        return True

    def emptyline(self):
        """This does nothing upon receiving an empty line."""
        pass

    def do_create(self, line):
        """Usage: create <class>
        It create a new class instance and print its id.
        """

        lines = line.split()

        if len(lines) == 0:
            print("** class name missing **")
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            new_obj_instance = eval(f"{lines[0]}")()
            print(new_obj_instance.id)
        storage.save()

    def do_show(self, line):
        """Usage: show <class> <id> or <class>.show(<id>)
        This Display the string representation of a class instance
        of a given id.
        """

        lines = line.split()

        if len(lines) == 0:
            print("** class name missing **")
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(lines) == 1:
            print("** instance id missing **")
        elif f"{lines[0]}.{lines[1]}" not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[f"{lines[0]}.{lines[1]}"])

    def do_destroy(self, line):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        This Delete a class instance of a given id."""

        lines = line.split()

        if len(lines) == 0:
            print("** class name missing **")
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(lines) == 1:
            print("** instance id missing **")
        elif f"{lines[0]}.{lines[1]}" not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[f"{lines[0]}.{lines[1]}"]
        storage.save()

    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        This Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        lines = line.split()

        if len(lines) == 0:
            print([str(value) for value in storage.all().values()])
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in storage.all().items()
                  if k.startswith(lines[0])])

    def do_update(self, line):
        """Usage: update <class> <id> <attribute_name>
        <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        This update a class instance of a given id by
        adding or updating
        a given attribute key/value pair or dictionary."""

        lines = line.split()

        if len(lines) == 0:
            print("** class name missing **")
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(lines) == 1:
            print("** instance id missing **")
        elif f"{lines[0]}.{lines[1]}" not in storage.all():
            print("** no instance found **")
        elif len(lines) == 2:
            print("** attribute name missing **")
        elif len(lines) == 3:
            print("** value missing **")
        else:
            inst_class = lines[0]
            inst_id = lines[1]
            inst_key = inst_class + "." + inst_id
            inst = storage.all()[inst_key]

            att_name = lines[2]
            att_value = lines[3]

            if att_value[0] == '"':
                att_value = att_value[1:-1]

            if hasattr(inst, att_name):
                type_of = type(getattr(inst, att_name))
                if type_of in [str, float, int]:
                    att_value = type_of(att_value)
                    setattr(inst, att_name, att_value)
            else:
                setattr(inst, att_name, att_value)
            storage.save()

    def default(self, line):
        """This is the default behavior for cmd module when input is invalid"""
        lines = line.split('.')
        if lines[0] in self.__classes:
            if lines[1] == "all()":
                self.do_all(lines[0])
            elif lines[1] == "count()":
                list_items = [v for k, v in storage.all().items()
                              if k.startswith(lines[0])]
                print(len(list_items))
            elif lines[1].startswith("show"):
                the_id = lines[1].split('"')[1]
                self.do_show(f"{lines[0]} {the_id}")
            elif lines[1].startswith("destroy"):
                the_id = lines[1].split('"')[1]
                self.do_destroy(f"{lines[0]} {the_id}")
            elif lines[1].startswith("update"):
                split_of = lines[1].split('(')
                split_of = split_of[1].split(')')
                if '{' in split_of[0]:
                    split_of = split_of[0].split(", {")
                    new_id = split_of[0].strip('"')
                    new_dict = '{' + split_of[1]
                    new_dict = eval(new_dict)
                    for k, v in new_dict.items():
                        self.do_update(f"{lines[0]} {new_id} {k} {v}")

                else:
                    split_of = split_of[0].split(', ')
                    n_id = split_of[0].strip('"')
                    n_name = split_of[1].strip('"')
                    n_value = split_of[2].strip('"')

                    self.do_update(f"{lines[0]} {n_id} {n_name} {n_value}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
