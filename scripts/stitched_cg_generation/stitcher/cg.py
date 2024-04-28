from stitcher.node import Node
from urllib.parse import unquote
import copy

class CallGraph:
    def __init__(self, cg):
        self.found= False
        self.cg = cg
        # a list having calls from one node object to another
        # example:
        #  [[<stitcher.node.Node object at 0x102f81450>,
        #   <stitcher.node.Node object at 0x102f81480>],
        #  [<stitcher.node.Node object at 0x102f81450>,
        #   <stitcher.node.Node object at 0x102f81450>]]
        self.internal_calls = []
        # exact same thing but for external calls
        self.external_calls = []
        # a superclass relation  can exist both to an internal or external superclass
        self.super_class_calls = []
        # a dict mapping modules with a dictionary mapping callable with node objects.
        # Given a module and a callable, using the self.nodes dict we can find the Node object representing the specific callable
        # the module and callable are represented in the node class
        # example:
        #  'pycparser': {'': <stitcher.node.Node object at 0x102085e40>,
        #                'parse_file': <stitcher.node.Node object at 0x102086800>,
        #                'preprocess_file': <stitcher.node.Node object at 0x1020867d0>},
        self.nodes = {}
        # dict mapping id to node object e.g 2188 to a certain node object, we need it in ordr to map the internal.external calls with the corresponding nodes
        self.id_to_node = {}
        self.node_list=[]
        self.product = self.cg["product"]
        self.version = self.cg["version"]
        self.root_dirs = set()
        self._parse_cg()

    def get_node(self, modname, name):
        if not self.nodes.get(modname, None):
            return None
        return self.nodes[modname].get(name, None)
    
    def get_root_dirs(self):
        return self.root_dirs
        
    def find_missing_externals(self, input_string):
        self.found = False
        initial_string = input_string
        while input_string:
            yield from self.find_missing_external(input_string)
            input_string_parts = input_string.split('.')
            if len(input_string_parts) <= 1:
                break
            input_string = '.'.join(input_string_parts[:-1])
        
        if not self.found:
            while initial_string:
                yield from self.find_missing_external(initial_string, True)
                input_string_parts = initial_string.split('.')
                if len(input_string_parts) <= 1:
                    break
                initial_string = '.'.join(input_string_parts[:-1])
        yield None, 0
    
    def find_missing_external(self, input_string, flag = False):
        # find the missing external call
        # input_string is the missing external call
        # we need to find the corresponding node object
        # we split the input_string into parts
        # print("Searching input string:", input_string)
        input_parts = input_string.split('.')
        matches = set()
        for k, v in self.nodes.items():
            for vs in v:
                uri = vs
                if flag:
                    uri = vs.split('.')[-1]

                # skip if vs is empty
                if uri == "":
                    continue
            
                if input_string.endswith("."+uri):
                        matches.add(v[vs])
                 # todo this is for protected members protected
                elif vs.startswith("_"):
                    if input_string.endswith("."+uri[1:]):
                        matches.add(v[vs])

        if len(matches)==0:
            yield None, 1
        elif len(matches)==1:
            x = matches.pop()
            self.found= True
            yield x, 1
        else:
            self.found = True
            for m in matches:           
                yield m, len(matches)

    def get_internal_calls(self):
        return self.internal_calls

    def get_external_calls(self):
        return self.external_calls

    def _parse_cg(self):


        def identify_nested_namespaces(uris):
            # For each uri we remove the last part of the namespace and try to see if a function/ class with the specific namespace exists.
            # If this is the case we add to the output dictionary a function/class as key (outer node) maped to a list of uris (inner functions) and we add the uri under test to this list
            nested_namespaces = {}
            uris = set(uris)
            for uri in uris:
                if '.' in uri:
                    parts = uri.split('.')
                    outer_namespace = '.'.join(parts[:-1])

                    if outer_namespace in uris:
                        if outer_namespace not in nested_namespaces:
                            nested_namespaces[outer_namespace] = []

                        nested_namespaces[outer_namespace].append(uri)
                    else:
                        outer_namespace = outer_namespace + "()"
                        if outer_namespace in uris:
                            if outer_namespace not in nested_namespaces:
                                nested_namespaces[outer_namespace] = []

                            nested_namespaces[outer_namespace].append(uri)
            return nested_namespaces
        
        def get_root_directory(source_file):
            root_dir = source_file.split("/")[0]
            if root_dir == "lib" or root_dir == "src" or root_dir == "lib3":
                root_dir = source_file.split("/")[1]
            if root_dir.endswith(".py"):
                root_dir = root_dir[:-3]
            return root_dir

        def iterate_mods(d, internal):
            for mod_id, data in d.items():
                if internal:
                    # todo we could just do modname = mod_id.split("/")[1] and avoid creating node object
                    # we do this just to get the modname (e.g. for external  the product and for internal the name of the module (e.g. m)
                    mod_node = Node(mod_id, product=self.product,
                                    version=self.version)
                    modname = unquote(mod_node.get_modname())
                    # modname = mod_node.get_modname()
                    # mod_id is  /dep1.dep1/ while modname is   dep1.dep1
                else:
                    modname = mod_id
                # we do this because an external modname might be the same with an internal modname causing the erasure of the previous nodes
                if modname not in self.nodes:
                    self.nodes[modname] = {}
                
                if internal:
                    src_file = get_root_directory(data["sourceFile"])
                    self.root_dirs.add(src_file)
                    # Handle nested function sizes
                    namespace_to_size = {}
                    # we first init a dictionary namespace_to_size which maps every namespace of a module to its size derived from the formulation: last-first+1
                    for namespace_id, namespace_data in data["namespaces"].items():
                            namespace = namespace_data["namespace"]
                            metadata = namespace_data["metadata"]
                            if metadata.get("first", None) != None:
                                size = metadata.get("last") - metadata.get("first") + 1
                            else:
                                # todo figure out which size  we assign to null
                                size = 0
                            namespace_to_size[namespace] = size

                    nested_namespaces = identify_nested_namespaces(list(namespace_to_size.keys()))

                    namespace_to_size_copy = copy.deepcopy(namespace_to_size)  # Perform deepcopy once
                    
                    for outer_node in nested_namespaces.keys():
                        size = namespace_to_size[outer_node]
                        # In order to find the nested size we aggregate the size (derived from the formulation: last-first+1) of the inner functions/classes
                        nested_size = sum(namespace_to_size_copy[inner_node] for inner_node in nested_namespaces[outer_node])
                        size -= nested_size
                        namespace_to_size[outer_node] = size

                for id, info in data["namespaces"].items():
                    super_cls = None
                    if info["metadata"].get("superClasses", None) != None:
                        super_cls = []
                        for cls in info["metadata"]["superClasses"]:
                            super_cls_node = Node(cls, product=self.product,
                                                        version=self.version)
                            super_cls.append(super_cls_node)
                            self.super_class_calls.append([
                                mod_node, super_cls_node
                            ])
                    # super_cls a list of node objects which are superclasses in the form of /ssh_exception/SSHException
                    if internal:
                        node = Node(info["namespace"], product=self.product,
                                super_cls=super_cls, version=self.version, loc=namespace_to_size.get(info["namespace"]))
                    else:
                        node = Node(info["namespace"], product=self.product,
                                super_cls=super_cls, version=self.version, loc=None)       
                    self.id_to_node[id] = node
                    if node.get_modname():
                        self.nodes[unquote(node.get_modname())][node.get_callable()] = node

        def iterate_calls(calls):
            res = []
            for src, dst, metadata in calls:
                if self.id_to_node.get(src, None) and self.id_to_node.get(dst, None):
                    res.append([
                        self.id_to_node.get(src),
                        self.id_to_node.get(dst)])
            return res
        
        def get_all_nodes(self):
            nodes = []
            for node in self.id_to_node:
                nodes.append(self.id_to_node[node])
            return nodes

        iterate_mods(self.cg["modules"]["internal"], True)
        self.node_list = get_all_nodes(self)
        iterate_mods(self.cg["modules"]["external"], False)

        self.internal_calls = iterate_calls(self.cg["graph"]["internalCalls"])
        self.external_calls = iterate_calls(self.cg["graph"]["externalCalls"])
