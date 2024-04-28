import json
import os
from stitcher.stitcher import Stitcher
from stitcher.reachability import ReachabilityDetector
import multiprocessing as mp
import requests as re
import time
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Produce stitched call graph of Python projects')
    parser.add_argument('-src', '--source', required=True, help='Directory hosting call graphs')
    parser.add_argument('-json', '--json', required=True, help='Path to JSON file hosting the dependencies')
    return parser.parse_args()


def load_final_apps(path):
    file = open(path)
    return json.load(file)


def find_callgraph(coordinate,source_path):
   
    path1 = source_path+"/"+ coordinate[0]+"/"+coordinate.replace(":", "/")+"/cg.json"
    path2 = source_path+"/apps/"+ coordinate+"/cg.json"
    if os.path.exists(path1):
        with open(path1, "r") as f:
            return (json.load(f))  
    elif os.path.exists(path2):
        with open(path2, "r") as f:
            return (json.load(f)) 
    else: 
        return None

def find_callgraphs(app_dict, source_path):
    cooridnate = list(app_dict.keys())[0]
    parent_cg = find_callgraph(cooridnate,source_path)
    dep_cgs = []
    for dep_coordinate  in list(app_dict.values())[0]:

        cg = find_callgraph(dep_coordinate,source_path)
        if cg:    
            dep_cgs.append(cg)
    dep_cgs.append(parent_cg)
    return dep_cgs

def stitch_cgs(app, source_path):
    app_name = list(app.keys())[0]
    owner, repo = app_name.split("/")
    print("Producing stitched call graph of:", app_name)
    cg_list = find_callgraphs(app,source_path)
    stitcher = Stitcher(cg_list, True, app_name)
    stitcher.stitch_for_rq1()
    reachability = ReachabilityDetector(stitcher, app_name)
    outfile = json.dumps(reachability.callgraph, indent=2)
    file_path = source_path+"/../stitched_callgraphs/"+owner+"/"+repo+"/cg.json"
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w+") as f:
        f.write(outfile)
    metrics = reachability.extract_metrics()
    # # stitcher.save_cache("data/projects_new/"+owner+"/"+repo)
    metrics["transitive_dependencies_count"] = len(cg_list) -1
    with open(source_path+"/../stitched_callgraphs/"+owner+"/"+repo+"/bloat_metrics.json", "w+") as f:
        f.write(json.dumps(metrics, indent=2))
    # return metrics 

def main():
    args = parse_args()
    apps = load_final_apps(args.json)
    # print(apps)
    sorted_data = sorted(apps, key=lambda x: len(list(x.values())[0]))
    pool = mp.Pool(mp.cpu_count()-2)
    output = pool.starmap(stitch_cgs, [(app, args.source) for app in apps])



if __name__ == "__main__":
    main()

