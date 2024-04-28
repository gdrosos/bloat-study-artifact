import sys
import json
from stitcher.load_environment import dynamic_import

from stitcher.cg import CallGraph
from stitcher.node import Node


class Stitcher:
    _unresolved = set()
    # external_to_resolved_internal_global = {}
    def __init__(self, call_graphs, simple, root):
        self.root = root.split(":")[0]
        self.simple = simple
        self.cgs = {}
        self.id_cnt = 0
        self.node_to_id = {}
        self.stitched = {
            "edges": [],
            "nodes": {}
        }
        self.total_dep_size = 0
        self.nodes_cnt = 0
        self.edges_cnt = 0
        self.resolved_cnt = 0
        self.unresolved_cnt = 0
        self.edges_cnt_no_builtin = 0
        self.predicted_cnt = 0
        self.node_to_metadata = {}
        self.root_dir_to_product= {}
        self._parse_cgs(call_graphs)
        self.external_to_resolved_internal = {}
        self.unresolved_externals = set()
        self.unique_levenstein_externals = set()
        self.internal_to_external= {}

    def stitch_for_rq1(self):
        for product, cg in self.cgs.items():
            internal_calls = cg.get_internal_calls()
            external_calls = cg.get_external_calls()
            self.edges_cnt += len(internal_calls) + len(external_calls)
            self.edges_cnt_no_builtin += len(internal_calls) + len(external_calls)

            for node in cg.node_list:
                # first check for root node, second, third check generally if we need locs
                self.node_to_metadata[node.to_string(self.simple)] = node.loc
                self._assign_id(node.to_string(self.simple))    
            for src, dst in internal_calls:
                self._handle_internals_for_rq1(src, dst)

            count = 0
            for src, dst in external_calls:
                count += 1
                if dst.to_string(False) not in Stitcher._unresolved:
                    # print(count, len(external_calls))
                    self._handle_externals(src, dst, product)
                else:
                    self.unresolved_cnt += 1
        self.nodes_cnt = self.id_cnt
        for node, id in self.node_to_id.items():
            self.stitched["nodes"][id] = {"URI": node, "metadata": {"LoC": self.node_to_metadata[node]}}

    def get_stitching_metadata(self):
        # for i in self.unresolved_externals:
        #     print("Error, could not resolve ", i)
        # print(self.resolved_cnt, self.unresolved_cnt, len(self.external_to_resolved_internal), len(self.unresolved_externals))
        return [self.resolved_cnt, self.unresolved_cnt, len(self.external_to_resolved_internal), len(self.unresolved_externals), len(self.unique_levenstein_externals)]

    def _handle_internals_for_rq1(self, src, dst):
        if self.node_to_id.get(src.to_string(self.simple), None) is None:
            # print("src", src.to_string(self.simple), src.is_func,  src.is_class)
            self._assign_id(src.to_string(self.simple))
        if self.node_to_id.get(dst.to_string(self.simple), None) is None:
            # print("dst", dst.to_string(self.simple), dst.is_func, dst.is_class)
            self._assign_id(dst.to_string(self.simple))
        self.node_to_metadata[src.to_string(self.simple)] = src.loc
        self.node_to_metadata[dst.to_string(self.simple)] = dst.loc
        self.stitched["edges"].append([
            self.node_to_id[src.to_string(self.simple)],
            self.node_to_id[dst.to_string(self.simple)],
        ])

    def _handle_internals(self, src, dst):
        self._assign_id(src.to_string(self.simple))
        self.node_to_metadata[src.to_string(self.simple)] = src.loc
        self._assign_id(dst.to_string(self.simple))
        self.node_to_metadata[dst.to_string(self.simple)] = dst.loc
        self.stitched["edges"].append([
            self.node_to_id[src.to_string(self.simple)],
            self.node_to_id[dst.to_string(self.simple)],
        ])

    def _handle_externals(self, src, dst, src_product):
        # if we haven't processed the internal (meaning that it is a module or class) we need to further investigate it
        if self.node_to_id.get(src.to_string(self.simple), None) is None:
            self._assign_id(src.to_string(self.simple))
            self.node_to_metadata[src.to_string(self.simple)] = src.loc
            # print("src2ext", src.to_string(self.simple), src.is_func, src.is_class)
        if "builtin" in dst.to_string():
            self.edges_cnt_no_builtin -= 1
            return
        product = dst.get_product()
        if self.cgs.get(product.replace("_", "-")):
            product = product.replace("_", "-")

        if self.cgs.get(product) or product in self.root_dir_to_product:
            src_str = src.to_string(self.simple)
            if src_str not in self.internal_to_external:
                    self.internal_to_external[src_str] = []
            self.internal_to_external[src_str].append(dst)

        #     found = False
        #     # we store resolved externals in external_to_resolved_internal so that we avoid resolving
        #     # the same external multiple times
        #     if dst.to_string(False) in self.external_to_resolved_internal:
        #         # resolved =  Stitcher.external_to_resolved_internal_global[dst.to_string(False)]
        #         resolved = self.external_to_resolved_internal[dst.to_string(False)]
        #     else:
        #         resolved = False
        #         for resolved in set(self.resolve(dst)):
        #             # if this already exists it means we want to jsut go add a new resolved element
        #             if dst.to_string(False)in self.external_to_resolved_internal:
        #                 # but we only add new elements if they do not already exist
        #                 if resolved.to_string(False) not in self.external_to_resolved_internal[dst.to_string(False)]:
        #                     # Stitcher.external_to_resolved_internal_global[dst.to_string(False)].append(resolved.to_string(False))
        #                     self.external_to_resolved_internal[dst.to_string(False)].append(resolved.to_string(False))
        #             else:
        #                 self.external_to_resolved_internal[dst.to_string(False)] = []
        #                 self.external_to_resolved_internal[dst.to_string(False)].append(resolved.to_string(False))
        #                 # Stitcher.external_to_resolved_internal_global[dst.to_string(False)] = []
        #                 # Stitcher.external_to_resolved_internal_global[dst.to_string(False)].append(resolved.to_string(False))
        #     if dst.to_string(False) in self.external_to_resolved_internal:
        #         self.resolved_cnt += 1
        #         self.node_to_metadata[src.to_string(self.simple)] = src.loc
        #         self._assign_id(src.to_string(self.simple))
        #         for external_uri in self.external_to_resolved_internal[dst.to_string(False)]:
        #             external_product, modname, callable = Node.get_modname_callable(external_uri)
        #             external = self.cgs[external_product].get_node(modname, callable)
        #             self.node_to_metadata[external.to_string(self.simple)] = external.loc
        #             self._assign_id(external.to_string(self.simple))
        #             self.stitched["edges"].append([
        #                 self.node_to_id[src.to_string(self.simple)],
        #                 self.node_to_id[external.to_string(self.simple)],
        #             ])

        #     else:
        #         if product!= src_product and self.cgs.get(product):
        #             self.unresolved_externals.add(dst.to_string(False))
        #             Stitcher._unresolved.add(dst.to_string(False))
        #             self.unresolved_cnt = self.unresolved_cnt + 1

    def output(self):
        return self.stitched

    def get_predicted_count(self):
        return self.predicted_cnt

    def _parse_cgs(self, paths):
        for p in paths:
            if not p:
                print("Error",  self.root)
                continue
            if self.cgs.get(p["product"], None):
                print("Error on parsing call graph", p)
                continue
            
            cg =CallGraph(p)
            self.cgs[p["product"]] = cg
            if p["product"]!= self.root:
                root_dirs = cg.get_root_dirs()
                for root_dir in root_dirs:
                    # if root_dir in self.root_dir_to_product:
                    #     print("Error", root_dir, p["product"], self.root) 
                    self.root_dir_to_product[root_dir] = p["product"]

    def parse_cg(self, cg_json):
        if not self.cgs.get(cg_json["product"], None):
            self.cgs[cg_json["product"]] = CallGraph(cg_json)

    def resolve(self, init_node, search_parents=True):
        product = init_node.get_product()
        callbl = init_node.get_callable().split(".")
        callable = init_node.get_callable()
        # we cannot resolve any calls
        if self.cgs.get(product.replace("_", "-")):
            product = product.replace("_", "-")
        if not self.cgs.get(product):
            product = self.root_dir_to_product.get(product, None)
            if not product:
                return None
        # all the combinations of modname filename with different modules
        # e.g.
            # ['cryptography', 'hazmat', 'primitives', 'asymmetric', 'rsa', 'RSAPublicNumbers']
            # cryptography hazmat.primitives.asymmetric.rsa.RSAPublicNumbers
            # cryptography.hazmat primitives.asymmetric.rsa.RSAPublicNumbers
            # cryptography.hazmat.primitives asymmetric.rsa.RSAPublicNumbers
            # cryptography.hazmat.primitives.asymmetric rsa.RSAPublicNumbers
            # cryptography.hazmat.primitives.asymmetric.rsa RSAPublicNumbers
        found = False
        for i in range(1, len(callbl)):
            modname = ".".join(callbl[:i])
            fnname = ".".join(callbl[i:])

            # check if the specific node having as modname and filename the combination exists
            actual = self.cgs[product].get_node(modname, fnname)
            if not actual:
                if search_parents:
                    # if it does not exist, and if it has superclasses,
                    parent_fnname = ".".join(callbl[i:-1])
                    if self.cgs[product].get_node(modname, parent_fnname):
                        fn = self._resolve_mro(product, modname, parent_fnname, callbl[-1])
                        if fn:
                            found = True
                            yield fn

            elif actual.is_func:
                found = True
                yield actual
            elif actual.is_class:
                # We assign the constructor if it exists
                init = self.cgs[product].get_node(actual.modname, actual.callable+".__init__")
                if init:
                    actual = init
                found = True
                yield actual
        if not found:
            if callable.endswith("__init__"):
                    callable = callable.replace("__init__", "")
            if callable.endswith("."):
                # example: numpy.poly1d.
                callable = callable[:-1]

            # todo do this for many things
            is_found = False
            identified_with_levenshtein = False
            for edge in dynamic_import(callable, self.cgs[product].product, self.cgs[product].version):
                if "$" in edge:
                    filename_path, declaration_path = edge.split("$")
                    node =  self.cgs[product].get_node(filename_path.replace("/", ".")[1:], declaration_path)
                    if node:
                        if node.is_class:
                            temp = self.cgs[product].get_node(node.modname, node.callable+".__init__")
                            if temp:
                                node = temp
                        is_found = True
                        yield node

                    if not is_found:
                        node =  self.cgs[product].get_node(filename_path.replace("/", ".")[1:].replace(".__init__", ""), declaration_path)
                        if not node:
                            node =  self.cgs[product].get_node(filename_path.replace("/", ".")[1:].replace(".__init__", ""), declaration_path+".__init__")
                        if node:
                            is_found = True
                            yield node            
                if not is_found:
                    for found, levenstein_candidates in self.cgs[product].find_missing_externals(edge):
                        if found:
                            if found.is_class:
                                # We assign the constructor if it exists
                                init = self.cgs[product].get_node(found.modname, found.callable+".__init__")
                                if init:
                                    found = init
                            is_found = True
                            self.unique_levenstein_externals.add(init_node.to_string())
                            yield found
            
            # elif not is_found:
            #     for found, levenstein_candidates in self.cgs[product].find_missing_externals(callable):
            #         if found:
            #             print("Maped", found.to_string(True), "for", callable)
            #             candidates = True
            #             if found.is_class:
            #                 # We assign the constructor if it exists
            #                 init = self.cgs[product].get_node(found.modname, found.callable+".__init__")
            #                 if init:
            #                     found = init
            #             identified_with_levenshtein = True
            #             yield found 
            #     if identified_with_levenshtein:
            #         self.unique_levenstein_externals.add(found)
    def _resolve_mro(self, product, modname, cls, name):
        if not self.cgs.get(product, None):
            return None

        node = self.cgs[product].get_node(modname, cls)

        resolved = None
        for parent in node.get_class_hier():
            if parent.get_product() == product:
                resolved = self.cgs[product].get_node(
                    parent.get_modname(),
                    parent.get_callable() + "." + name)
            else:
                for parent_resolved in self.resolve(parent, search_parents=False):
                    if parent_resolved:
                        resolved = self.cgs[parent_resolved.get_product()].get_node(
                            parent_resolved.get_modname(),
                            parent_resolved.get_callable() + "." + name)

            if resolved:
                return resolved

        return None

    def _err_and_exit(self, msg):
        print(msg)
        sys.exit(1)

    def save_cache(self, path):
        with open(path+"/external_2_internal.json", 'w') as json_file:
            json.dump(self.external_to_resolved_internal, json_file, indent=2)
        with open(path+"/unresolved.txt", 'w') as txt_file:
            for item in Stitcher._unresolved:
                txt_file.write(str(item) + '\n')
        
    def _assign_id(self, node_str):
        if self.node_to_id.get(node_str, None) is None:
            self.node_to_id[node_str] = self.id_cnt
            self.id_cnt += 1
