import json
import datetime
from pycg_producer.dep_producer import CallGraphGenerator
from multiprocessing import cpu_count, Pool
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Produce partial call graph of apps')
    parser.add_argument('-src', '--source', required=True, help='Directory hosting source files')
    parser.add_argument('-json', '--json', required=True, help='Path to JSON file hosting the dependencies')
    return parser.parse_args()

SUCCESS = "Success"
FAIL = "Fail"

def process(package, source):
    package = package.strip()
    product, version = package.split(":")
    cg_path = source+"/partial_callgraphs/"+package[0]+"/"+product+"/"+version
    if not os.path.exists(cg_path):
        print ("{}: Producing partial call graph of dependency {}".format(
            datetime.datetime.now(),
            package
        ))
        generator = CallGraphGenerator(source, package)
        output = generator.generate()

        path =  source+"/sources/"+ package[0]+"/"+package.replace(":", "/")+"/top_level.txt"
        if not os.path.exists(os.getcwd()+path):
            generator.copy_top_level_txt()

def main():
    args = parse_args()
    file = open(args.json, 'r')
    data = json.load(file)
    dependency_set = set()
    for project in data:
        for dep in list(project.values())[0]:
            dependency_set.add(dep)
    pool = Pool(cpu_count()-2)
    output = pool.starmap(process, [(dep, args.source) for dep in dependency_set])

if __name__ == "__main__":
    main()