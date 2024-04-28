import os
import sys
import subprocess
import importlib
import inspect
import argparse


def get_path(obj):
    path = None
    while hasattr(obj, '__wrapped__'):
        obj = obj.__wrapped__
    try:
        path = inspect.getfile(obj)
    except Exception as e:
        # Handle the case of built-in modules
        message = "The error message suggests that you are trying to retrieve the file path for a built-in module, " \
                "in this case, the '{}' module. The inspect.getfile() function cannot provide the file path " \
                "for built-in modules because they are implemented in C or as part of the Python interpreter.".format(
            obj)
    if not path:
        module = inspect.getmodule(obj)
        try:
            path = inspect.getfile(module)
        except Exception as e:
            # Handle the case of built-in modules
            message = "The error message suggests that you are trying to retrieve the file path for a built-in module, " \
                    "in this case, the '{}' module. The inspect.getfile() function cannot provide the file path " \
                    "for built-in modules because they are implemented in C or as part of the Python interpreter.".format(
                obj)
            return None, None

    import_namespace = getattr(obj, '__qualname__', None)
    return path, import_namespace

def split_string(string, delimiter, n):
    parts = string.split(delimiter)
    return delimiter.join(parts[:n]), delimiter.join(parts[n:])

def find_file(input_string, number=1):
    module_name, obj_name = split_string(input_string, '.', number)
    # Form the full path to the module
    try:
        
        # Import the module
        module = importlib.import_module(module_name)
        # Check if the object is a class

        if '.' in obj_name:
            obj_parts = obj_name.split('.')
            parent_obj = module
            for part in obj_parts:
                parent_obj = getattr(parent_obj, part, None)
                if parent_obj is None:
                    # print(f"Object {part} not found in module {module_name}")
                    raise ImportError
            obj = parent_obj
            if obj is None:
                # print(f"Object {obj_name} not found in module {module_name}")
                raise ImportError
        else:
        # Object is not a nested call
            obj = getattr(module, obj_name, None)
            if obj is None:
                # print(f"Object {obj_name} not found in module {module_name}")
                raise ImportError

        # Use the get_path function to get the path and namespace
        
        path, namespace = get_path(obj)
        if path:
            path = path.replace(".py", "")

            if "site-packages" in path:
                path = path.split("site-packages")[1]
        return path, namespace

    except ImportError as e:
        # print(f"Failed to import module: {module_name}", obj_name, number)
        number += 1
        if '.' in obj_name:
            return find_file(input_string, number)
        else:
            # print("Error", input_string, obj_name, e)
            return None
    except Exception as e:
        print("Error", e)
        return None

def dynamic_import(input_string):
    while input_string:
        result = find_file(input_string)
        if result:
            if result[1]:
                print(result[0]+"$"+result[1])
        else:
            print(input_string)
        input_string_parts = input_string.split('.')
        if len(input_string_parts) <= 1:
            break
        input_string = '.'.join(input_string_parts[:-1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform dynamic import and find file path.")
    parser.add_argument("input_string", help="The input string to be processed.")
    args = parser.parse_args()

    result = dynamic_import(args.input_string)