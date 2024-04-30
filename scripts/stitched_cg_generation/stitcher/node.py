class Node:
    def __init__(self, uri_str, product=None, super_cls=None, version=None, loc=None):
        # uri in str of the ndoe
        if "/" in product:
            product = product.replace("/", "#")
        self.uri_str = uri_str
        self.product = product
        self.version = version
        # super_cls a list of node objects which are superclasses in the form /ssh_exception/SSHException
        self.super_cls = super_cls or []
        self.loc = loc
        # externals are in the form of //product//callable eg. //django//django.error.__class__
        # internals are in the form of /modname/callable eg. /test.api/A.hello()
        if uri_str.endswith("/"):
            self.is_mod = True
        else:
            self.is_mod = False
        if len(uri_str.split("/")) == 5:
            self.internal = False
            self.external = True
        else:
            self.internal = True
            self.external = False

        self.modname = self.callable = ""

        splitted = self.uri_str.split("/")
        if self.internal:
            self.modname = splitted[1]
            self.callable = splitted[2]
        else:
            # product only for external nodes since it is included in the uri e.g. //django//django.error.__class__
            self.product = splitted[2]
            self.callable = splitted[4]

        self.is_class = super_cls != None
        self.is_func = False
        if self.callable.endswith("()"):
            self.is_func = True
            # remove parentheses
            self.callable = self.callable[:-2]
    def get_product(self):
        return self.product

    def get_version(self):
        return self.version

    def get_modname(self):
        return self.modname

    def get_callable(self):
        return self.callable

    def get_class_hier(self):
        return self.super_cls

    def get_class(self):
        if self.is_mod or self.is_func:
            return False
        else:
            return True
    
    def to_string(self, simple=False):
        uri = ""
        if not simple:
            uri += "fasten://PyPI!"
        else:
            uri += "//"
        uri += self.product
        if self.version and not simple:
            uri += "$" + self.version
        uri += "/" + self.modname + "/" + self.callable

        if self.is_func:
            uri += "()"
        return uri

    def from_string(input_string):
        # Remove the fasten://PyPI! prefix if present
        if input_string.startswith("fasten://PyPI!"):
            input_string = input_string.replace("fasten://PyPI!", "")

        # Remove the leading "//" for simple URIs
        if input_string.startswith("//"):
            input_string = input_string[2:]

        return input_string

    def get_modname_callable(input_string):
        # Remove the fasten://PyPI! prefix if present
        if input_string.startswith("fasten://PyPI!"):
            input_string = input_string.replace("fasten://PyPI!", "")

        input_string = input_string.replace("()", "")
        parts = input_string.split("/")
        product, version = parts[0].split("$")
        return product, parts[1], parts[2]
        