import networkx as nx
import matplotlib.pyplot as plt
from stitcher.node import Node


class ReachabilityDetector:
    reachable_vulnerabilities= set()

    def __init__(self, stitcher, coordinate, rq4=False):
        self.stitcher = stitcher
        if rq4:
            self.callgraph = stitcher
        else:
            self.callgraph = stitcher.output()
        self.root_package = coordinate
        self.reachable_nodes = set()
        self.metrics = {}
        self.id_to_node={}
        self.uri_to_loc = {}
        self.external_to_resolved_internal = {}
        self.graph = self._load_to_networkx(self.callgraph)
        self.total_dependency_files = set()
        self.total_dependency_files_loc = 0
        self.total_dependency_functions = set()
        self.total_dependency_functions_loc = 0
        self.dependency_to_file_size = {}
        self.own_files = set()
        self.own_files_loc = 0
        self.own_functions = set()
        self.unresolved_externals = set()
        self.own_functions_loc = 0
        self._measure_total_metrics()
        if rq4:
            self.reach_all_nodes_rq4()
        else:
            self.reach_all_nodes()
        self.reachable_dependencies = set()
        self.bloated_dependencies_loc = 0
        self._find_reachable_dependencies()
        self.bloated_dependencies =  self.dependency_to_file_size.keys() -self.reachable_dependencies
        self.bloated_dependencies_loc = self._get_bloated_dependencies_loc()
        self.reachable_dependency_files = set()
        self.reachable_dependency_files_loc = 0
        self.reachable_dependency_functions= set()
        self.reachable_dependency_functions_loc = 0
        self.measure_reachable_metrics()
        # print(self.reachable_dependency_functions)
        self.bloated_dependency_files = self.total_dependency_files - self.reachable_dependency_files
        self.bloated_dependency_files_loc = self.total_dependency_files_loc -  self.reachable_dependency_files_loc
        self.bloated_dependency_functions = self.total_dependency_functions - self.reachable_dependency_functions
        self.bloated_dependency_functions_loc = self.total_dependency_functions_loc -  self.reachable_dependency_functions_loc
        self.vulnerable_dependencies_reachable_cnt = 0
        self.vulnerable_dependencies_bloated_cnt = 0  
        self.vulnerable_dependencies_reachable_function_level_cnt  = 0
        self.vulnerable_dependencies_bloated_function_level_cnt = 0
        self.vulnerable_dependencies_reachable_function_level_unresolved_cnt = 0
        # self.draw()

    def find_node_by_uri(self, target_uri):
        # print("ssss",target_uri
        #       )
        # for i in self.stitcher.internal_to_external["//rdiff-backup#rdiff-backup/testing.api_test/ApiVersionTest.test_runtime_info_calling()"]:
        #     print(i.to_string())
        # print(self.uri_to_node_id.get("//rdiff-backup#rdiff-backup/testing.api_test/ApiVersionTest.test_runtime_info_calling()"))
        # print(self.uri_to_node_id.get("//PyYAML/yaml/safe_load()"))

        return self.uri_to_node_id.get(target_uri)

    def draw(self):
        node_labels = nx.get_node_attributes(self.graph,'URI')
        pos = nx.spring_layout(self.graph, scale=6)
        nx.draw(self.graph, pos, with_labels=False)
        nx.draw_networkx_labels(self.graph, pos, labels = node_labels)
        plt.show()


    def _measure_total_metrics(self):
        for node in self.callgraph["nodes"].keys():
            if self.id_to_node[int(node)].get_product().replace("#","/")!= self.root_package:
                if self.callgraph["nodes"][node]["URI"].endswith("()"):
                    self.total_dependency_functions.add(self.callgraph["nodes"][node]["URI"])
                    self.total_dependency_functions_loc += self.callgraph["nodes"][node]["metadata"]['LoC']
                elif self.callgraph["nodes"][node]["URI"].endswith("/"):
                    self.total_dependency_files.add(self.callgraph["nodes"][node]["URI"])
                    self.total_dependency_files_loc += self.callgraph["nodes"][node]["metadata"]['LoC']
                    parts = self.callgraph["nodes"][node]["URI"].split('/')
                    product = parts[2]
                    if product in self.dependency_to_file_size:
                        self.dependency_to_file_size[product] += self.callgraph["nodes"][node]["metadata"]['LoC']
                    else:
                        self.dependency_to_file_size[product] = self.callgraph["nodes"][node]["metadata"]['LoC']
            else:
                if self.callgraph["nodes"][node]["URI"].endswith("()"):
                    self.own_functions.add(self.callgraph["nodes"][node]["URI"])
                    self.own_functions_loc += self.callgraph["nodes"][node]["metadata"]['LoC']
                elif self.callgraph["nodes"][node]["URI"].endswith("/"):
                    self.own_files.add(self.callgraph["nodes"][node]["URI"])
                    self.own_files_loc += self.callgraph["nodes"][node]["metadata"]['LoC']
                
    def _find_reachable_dependencies(self):
        for node in self.reachable_nodes:
            product = self.id_to_node[int(node)].get_product().replace("#","/")
            if product != self.root_package:
                self.reachable_dependencies.add(product)

    def _get_bloated_dependencies_loc(self):
        bloated_dependencies_loc = 0
        for dependency in self.bloated_dependencies:
            bloated_dependencies_loc += self.dependency_to_file_size[dependency]
        return bloated_dependencies_loc

    def _get_reachable_dependencies_loc(self):
        reachable_dependencies_loc = 0
        for dependency in self.reachable_dependencies:
            reachable_dependencies_loc += self.dependency_to_file_size[dependency]
        return reachable_dependencies_loc
    
    def _load_to_networkx(self, callgraph):
        graph = nx.DiGraph()
        self.uri_to_node_id = {}
        for node in callgraph["nodes"]:
            uri = self.callgraph["nodes"][node]["URI"]
            self.uri_to_node_id[uri] = int(node) 
            self.uri_to_loc[uri] = self.callgraph["nodes"][node]["metadata"]['LoC']
            simple_uri = Node.from_string(uri)
            product, uri = simple_uri.split("/", 1)
            self.id_to_node[int(node)]= Node("/"+uri, product=product, loc=self.callgraph["nodes"][node]["metadata"]['LoC'])
            graph.add_node(int(node), URI=callgraph["nodes"][node]["URI"], LoC= callgraph["nodes"][node]["metadata"]['LoC'])
        for edge in callgraph["edges"]:
            graph.add_edge(edge[0], edge[1])
        return graph

    def reach_all_nodes_rq4(self):
        entrypoints = self.find_entrypoints()
        for node in entrypoints:
            nodes = nx.descendants(self.graph , int(node))
            self.reachable_nodes.update(nodes)
            self.reachable_nodes.add(node)
    
    def reach_all_nodes(self):
            entrypoints = self.find_entrypoints()
            while entrypoints:
                current_node = entrypoints.pop()
                if current_node not in self.reachable_nodes:
                    self.reachable_nodes.add(current_node)

                    # if current_node not in self.unresolved_externals:
                    #     if current_node in self.external_to_resolved_internal:
                    #         externals =  self.external_to_resolved_internal[current_node]
                    #     else:
                    #         externals, has_external = self.process_external_calls_for_node(current_node)
                    #         for external in externals:
                    #             if current_node in self.external_to_resolved_internal:
                    #                 if external not in self.external_to_resolved_internal[current_node]:
                    #                     self.external_to_resolved_internal[current_node].append(external)
                    #             else:
                    #                 self.external_to_resolved_internal[current_node] = []
                    #                 self.external_to_resolved_internal[current_node].append(external)
                    #     if not has_external and current_node not in self.external_to_resolved_internal:
                    #         self.unresolved_externals.add(current_node)
                    externals = self.process_external_calls_for_node(current_node)
                    for external in externals:
                        self.graph.add_edge(current_node, external)
                        self.callgraph["edges"].append([current_node,external ])
                        if external not in self.reachable_nodes:
                            entrypoints.add(external)

                    descendants = nx.descendants(self.graph, int(current_node))
                    for descendant in descendants:
                        if descendant not in self.reachable_nodes:
                            entrypoints.add(descendant)
            
    def process_external_calls_for_node(self, node_id):
        # Convert node_id to the string representation used in internal_to_external mapping
        node_str = self.id_to_node[node_id].to_string(True)
        # Check if this node has associated external calls
        return_set = set()
        if node_str in self.stitcher.internal_to_external:
            for external_call in self.stitcher.internal_to_external[node_str]:
                if external_call not in self.unresolved_externals:
                    if external_call in self.external_to_resolved_internal:
                        resolved =  self.external_to_resolved_internal[external_call]
                        for i in resolved:
                            return_set.add(self.find_node_by_uri(i.to_string(True)))
                    else:
                        for resolved in set(self.stitcher.resolve(external_call)):
                            if external_call in self.external_to_resolved_internal:
                                if resolved not in self.external_to_resolved_internal[external_call]:
                                    self.external_to_resolved_internal[external_call].append(resolved)
                            else:
                                self.external_to_resolved_internal[external_call] = []
                                self.external_to_resolved_internal[external_call].append(resolved)
                            return_set.add(self.find_node_by_uri(resolved.to_string(True)))
                        if  external_call not in self.external_to_resolved_internal:
                            self.unresolved_externals.add(external_call)
        return return_set

    def find_entrypoints(self):
        entrypoints=set()
        for item in self.callgraph["nodes"]:
            if self.id_to_node[int(item)].get_product().replace("#","/") == self.root_package:
                entrypoints.add(item)
        return entrypoints

    def measure_reachable_metrics(self):
        for id in self.reachable_nodes:
            if self.id_to_node[int(id)].get_product().replace("#","/") != self.root_package:
                node = self.id_to_node[int(id)]
                if node.loc >0:
                    node_file = node.get_modname()
                    file_uri =  "//"+node.get_product() +"/" + node_file + "/"
                    self.reachable_dependency_files.add(file_uri)
                    self.reachable_dependency_functions.add(node.to_string(True))
                    self.reachable_dependency_functions_loc += node.loc
        for file in self.reachable_dependency_files:
            if file in self.uri_to_loc:
                self.reachable_dependency_files_loc += self.uri_to_loc[file]
            else:
                self.reachable_dependency_files_loc += self.uri_to_loc[file+"()"]


    def classify_bloated_deps(self, deps_dict, used):
        classified_bloat = {}
        classified_bloat_loc = {}
        for level, dependencies in deps_dict.items():
            bloat_count = 0
            bloat_loc = 0
            bloated_deps_lower = set()  # Using a set to store bloated dependencies in lowercase for faster lookup

            # Convert bloated dependencies to lowercase and add to the set
            if not used:
                for b_dep in self.bloated_dependencies:
                    bloated_deps_lower.add(b_dep.lower())   
            else:
                for b_dep in self.reachable_dependencies:
                    bloated_deps_lower.add(b_dep.lower())
            
            dependency_to_file_size_lower = {key.lower(): value for key, value in self.dependency_to_file_size.items()}

            # Check each dependency against the set of bloated dependencies
            for dep in dependencies:
                dep_name = dep.split(':')[0].lower()
                if dep_name in bloated_deps_lower:
                    bloat_count += 1
                    if dep_name in dependency_to_file_size_lower:
                        bloat_loc += dependency_to_file_size_lower[dep_name]
            
            classified_bloat[level] = bloat_count
            classified_bloat_loc[level] = bloat_loc
            break
        return classified_bloat, classified_bloat_loc

    def classify_bloated_files(self, deps_dict, used):
        classified_bloat_files = {}
        classified_bloat_files_loc = {}

        for level, dependencies in deps_dict.items():
            if used:
                bloat_files = [file for file in self.reachable_dependency_files 
                        if file.split("/")[2].lower() in {dep.lower() for dep in dependencies}]     
            else:
                bloat_files = [file for file in self.bloated_dependency_files 
                        if file.split("/")[2].lower() in {dep.lower() for dep in dependencies}]
            bloat_count = len(bloat_files)
            bloat_loc = 0
            for file in bloat_files:
                if file in self.uri_to_loc:
                    bloat_loc += self.uri_to_loc[file]
                else:
                    # for cases like /tenacity.retry/()
                    bloat_loc += self.uri_to_loc[file+"()"]

            classified_bloat_files[level] = bloat_count
            classified_bloat_files_loc[level] = bloat_loc
            break

        return classified_bloat_files, classified_bloat_files_loc

    def classify_bloated_functions(self, deps_dict, used):
        classified_bloat_functions = {}
        classified_bloat_functions_loc = {}

        for level, dependencies in deps_dict.items():
            if used:
                bloat_functions = [file for file in self.reachable_dependency_functions 
                    if file.split("/")[2].lower() in {dep.lower() for dep in dependencies}]
            else:
                bloat_functions = [file for file in self.bloated_dependency_functions 
                        if file.split("/")[2].lower() in {dep.lower() for dep in dependencies}]
            bloat_count = len(bloat_functions)
            bloat_loc = sum([self.uri_to_loc[file] for file in bloat_functions])

            classified_bloat_functions[level] = bloat_count
            classified_bloat_functions_loc[level] = bloat_loc
            break

        return classified_bloat_functions, classified_bloat_functions_loc
    
    def extract_metrics(self):
        self.metrics["product"] = self.root_package
        self.metrics["own_files_count"] = len(self.own_files)
        self.metrics["own_files_loc"] = self.own_files_loc
        self.metrics["own_functions_count"] = len(self.own_functions)
        self.metrics["own_functions_loc"] = self.own_functions_loc
        self.metrics["total_dependency_functions_count"] = len(self.total_dependency_functions)
        self.metrics["total_dependency_functions_loc"] = self.total_dependency_functions_loc
        self.metrics["total_dependency_files_count"] = len(self.total_dependency_files)
        self.metrics["total_dependency_files_loc"] = self.total_dependency_files_loc
        self.metrics["reachable_dependencies"] = len(self.reachable_dependencies)
        self.metrics["reachable_dependencies_loc"] = self._get_reachable_dependencies_loc()
        self.metrics["reachable_dependency_files"] = len(self.reachable_dependency_files)
        self.metrics["reachable_dependency_files_loc"] =self.reachable_dependency_files_loc
        self.metrics["reachable_dependency_functions"] = len(self.reachable_dependency_functions)
        self.metrics["reachable_dependency_functions_loc"] =self.reachable_dependency_functions_loc

        self.metrics["total_dependencies_count"] = len(self.dependency_to_file_size.keys())

        self.metrics["bloated_dependencies_count"] = len(self.bloated_dependencies)
        self.metrics["bloated_dependencies_loc"] = self.bloated_dependencies_loc
        self.metrics["bloated_files_count"] = len(self.bloated_dependency_files)
        self.metrics["bloated_files_loc"] = self.bloated_dependency_files_loc
        self.metrics["bloated_functions_count"] = len(self.bloated_dependency_functions)
        self.metrics["bloated_functions_loc"] = self.bloated_dependency_functions_loc 
        self.metrics["unique_resolved_count"] = len(self.external_to_resolved_internal)
        self.metrics["unique_unresolved_count"] = len(self.unresolved_externals)
        return self.metrics

    def extract_security_metrics(self, vulnerable_dependency_dict, direct_set):
        exposure_dict= {"Active": {}, "Bloated":{}, "Inactive": {}, "Undefined":{}}
        for coordinate in vulnerable_dependency_dict:
            other_lang = False
            #undefined exposure check
            for vuln_id, vulnerable_functions in vulnerable_dependency_dict[coordinate].items():
                    for func in vulnerable_functions:
                        if func =="other_lang":
                            other_lang = True

            # vulnerabilities = vuln[coordinate]
            package, version = coordinate.split(":")
            if direct_set is None:
                status = "Unresolved"
            elif any(package.lower() == s.lower() for s in direct_set):
                status = "Direct"
            else:
               status = "Transitive"

            if other_lang and package in self.reachable_dependencies:
                self.vulnerable_dependencies_reachable_function_level_unresolved_cnt +=1
                exposure_dict["Undefined"][package] = {"Status": status}
            elif package in self.reachable_dependencies:
                ReachabilityDetector.reachable_vulnerabilities.add(coordinate)
                self.vulnerable_dependencies_reachable_cnt+=1
                reachable = False
                reachable_file = False
                bloated = False
                for vuln_id, vulnerable_functions in vulnerable_dependency_dict[coordinate].items():
                    for func in vulnerable_functions:
                        if func in self.reachable_dependency_functions:
                            reachable = True
                        if func in self.bloated_dependency_functions:
                            bloated = True
                        # measure if files are reachable in inactive exposures
                        file = func.rsplit('/', 1)[0] + '/'
                        if file in self.reachable_dependency_files:
                            reachable_file = True
                if reachable:
                    bloated_files=0
                    used_files = 0
                    for file in self.reachable_dependency_files:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            used_files+=1
                    for file in self.bloated_dependency_files:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            bloated_files+=1 
                    bloated_functions=0
                    used_functions = 0
                    for file in self.reachable_dependency_functions:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            used_functions+=1
                    for file in self.bloated_dependency_functions:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            bloated_functions+=1 
                    exposure_dict["Active"][package] = {"bloated_files":bloated_files, "used_files":used_files, "bloated_functions":bloated_functions, "used_functions":used_functions, "Status": status}
                    self.vulnerable_dependencies_reachable_function_level_cnt +=1
                elif bloated:
                    bloated_files=0
                    used_files = 0
                    for file in self.reachable_dependency_files:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            used_files+=1
                    for file in self.bloated_dependency_files:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            bloated_files+=1 
                    bloated_functions=0
                    used_functions = 0
                    for file in self.reachable_dependency_functions:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            used_functions+=1
                    for file in self.bloated_dependency_functions:
                        name = file.split("/")[2].lower()
                        if package.lower() == name.lower():
                            bloated_functions+=1 
                    
                    exposure_dict["Inactive"][package] = {"bloated_files":bloated_files, "used_files":used_files, "bloated_functions":bloated_functions, "used_functions":used_functions, "reachable_file": reachable_file,  "Status": status}
                    self.vulnerable_dependencies_bloated_function_level_cnt +=1
                # todo added this
                else:
                    exposure_dict["Undefined"][package] =  {"Status": status}
                    self.vulnerable_dependencies_reachable_function_level_unresolved_cnt+1
            elif package in self.bloated_dependencies:
                exposure_dict["Bloated"][package] =  {"Status": status}
                self.vulnerable_dependencies_bloated_cnt+=1

            else:
                print("Error", self.root_package)
        return (self.vulnerable_dependencies_reachable_cnt,
                self.vulnerable_dependencies_bloated_cnt,
                self.vulnerable_dependencies_reachable_function_level_cnt,
                self.vulnerable_dependencies_bloated_function_level_cnt,
                self.vulnerable_dependencies_reachable_function_level_unresolved_cnt,
                exposure_dict)

