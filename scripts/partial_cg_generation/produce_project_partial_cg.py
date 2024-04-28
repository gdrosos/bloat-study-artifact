import json
import datetime
from pycg_producer.app_producer import CallGraphGenerator
from multiprocessing import cpu_count, Pool
import os
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Produce partial call graph of apps')
    parser.add_argument('-src', '--source', required=True, help='Directory hosting source files')
    parser.add_argument('-json', '--json', required=True, help='Path to JSON file hosting the projects')
    return parser.parse_args()


def process(package, source):
    package = package.strip()
    if not os.path.exists(source+"/partial_callgraphs/apps/"+package):
        print ("{}: Producing partial call graph of project {}".format(
        datetime.datetime.now(),
        package
        ))

        generator = CallGraphGenerator(source, package)
        output = generator.generate()

        return output

def main():
    args = parse_args()
    file = open(args.json, 'r')
    data = json.load(file)
    project_list = []
    for project in data:
        project_list.append(list(project.keys())[0])
    pool = Pool(cpu_count()-2)
    output = pool.starmap(process, [(app, args.source) for app in project_list])


if __name__ == "__main__":
    main()