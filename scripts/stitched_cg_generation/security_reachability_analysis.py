import json
import os
from stitcher.reachability import ReachabilityDetector
import multiprocessing as mp
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Extract security bloat metrics for RQ2 through the reachability analysis')
    parser.add_argument('-host', '--host', required=True, help='Path to the directory hosting the stitched call graphs')
    parser.add_argument('-project_vulns', '--project_vulns', required=True, help='Json file hosting project vulnerabilities')
    parser.add_argument('-vuln2func', '--vuln2func', required=True, help='Json file hosting the manual mapping of vulnerabilities to vulnerable functions')
    return parser.parse_args()

def load_cg(project, path):
    path = path+ "/"+project+"/cg.json"
    if os.path.exists(path):
        with (open(path, "r")) as f:
            return json.load(f)

def load_project_vulnerabilities(project_vulns):
    file = open(project_vulns)
    return json.load(file) 

def load_vulnerable_functions(vuln2func):
    file = open(vuln2func)
    return json.load(file) 


# def parse_dependency_graph(dep_graph_path):
#     with open(dep_graph_path, 'r') as file:
#         dep_graph = json.load(file)
#     return dep_graph

# def max_depth(graph, node, visited=None):
#     if visited is None:
#         visited = set()
    
#     if node in visited:
#         return 0  # Avoid infinite loops by not revisiting nodes
    
#     visited.add(node)

#     # If the node has no dependencies, its depth is 0
#     if not graph.get(node):
#         return 0
    
#     # Get the depth of each dependency and take the maximum
#     return 1 + max(max_depth(graph, dep, visited) for dep in graph[node])

# def collect_dependencies_by_depth(graph, node, visited=None, current_depth=1, depth_dict=None, deps=None):
#     if deps is None:
#         deps = set() 
#     if visited is None:
#         visited = set()

#     if depth_dict is None:
#         depth_dict = {}

#     if node in visited:
#         return depth_dict  # Avoid infinite loops by not revisiting nodes

#     visited.add(node)

#     # If the node has no dependencies, return the current depth_dict
#     if not graph.get(node):
#         return depth_dict


#     for dep in graph[node]:
#         product = dep.split(":")[0]
#         if product not in  deps:
#             if current_depth not in depth_dict:
#                 depth_dict[current_depth] = set()
#             deps.add(product)
#             depth_dict[current_depth].add(product)
#         collect_dependencies_by_depth(graph, dep, visited, current_depth + 1, depth_dict, deps)

    # return depth_dict
# def get_depth(app_name):
#     owner, repo = app_name.split("/")
#     dep_graph_path = "../../callgraph_generation/pypi/produce_missing/data/sources/apps/"+owner+"/"+repo+"/dep_graph.json"
#     if os.path.exists(dep_graph_path):
#         # print("Processing", app_name)
#         dep_graph = parse_dependency_graph(dep_graph_path)
#         depth = max_depth(dep_graph,app_name)
#         dep_dict = collect_dependencies_by_depth(dep_graph, app_name)
#         return depth, dep_dict
    

def update_dict_with_relevant_vulnerable_functions(vulnerabilities, vuln2func):
    merged_dict = {}
    for vuln_dict in vulnerabilities:
        for package, vuln_ids in vuln_dict.items():
            functions_list = []
            for vuln_id in vuln_ids:
                if vuln_id in vuln2func:
                    functions_list.extend(vuln2func[vuln_id])
            if functions_list:
                merged_dict[package] = {vuln_id: functions_list for vuln_id in vuln_ids}
    
    return merged_dict

def process(vulnerabilities, path, vuln2func):
        app_name = vulnerabilities[0]
        owner, repo = app_name.split("/")
        if not os.path.exists(path+"/"+owner+"/"+repo):
            return
        # if os.path.exists("data/projects_new/"+owner+"/"+repo+"/metrics_rq4_new.json"):
        #     return
        print("Processing", app_name)
        # depth, deps_dict = get_depth(app_name)
        # direct_set = deps_dict.get(1)
        cg = load_cg(app_name, path)
        reachability = ReachabilityDetector(cg, app_name, True)
        metrics = reachability.extract_metrics()
        func = update_dict_with_relevant_vulnerable_functions(vulnerabilities[1], vuln2func)
        reachable_cnt, bloated_cnt, reachable_function_lvl_cnt, bloated_function_lvl_cnt, unresolved_function_lvl_cnt, exposure_dict  = reachability.extract_security_metrics(func, [])
        metrics["vulnerable_dependencies_reachable"] = reachable_cnt
        metrics["vulnerable_dependencies_bloated"] = bloated_cnt
        metrics["vulnerable_dependencies_reachable_through_functions"] = reachable_function_lvl_cnt
        metrics["vulnerable_dependencies_bloated_through_functions"] = bloated_function_lvl_cnt
        metrics["vulnerable_dependencies_unresolved_through_functions"] = unresolved_function_lvl_cnt
        metrics["exposure_dict"] = exposure_dict
        print(metrics)
        with open(path+"/"+owner+"/"+repo+"/security_metrics.json", "w+") as f:
            f.write(json.dumps(metrics, indent=2))

def main():
    args = parse_args()
    vulnerabilities = load_project_vulnerabilities(args.project_vulns)
    vuln2func = load_vulnerable_functions(args.vuln2func)
    pool = mp.Pool(mp.cpu_count())
    pool.starmap(process, [(item, args.host, vuln2func) for item in vulnerabilities.items()])

        

if __name__ == "__main__":
    main()

