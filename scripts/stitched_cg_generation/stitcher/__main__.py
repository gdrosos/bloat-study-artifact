import json
import argparse

from stitcher.stitcher import Stitcher
from stitcher.reachability import ReachabilityDetector

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("call_graph",
        nargs="*",
        help="Paths to call graphs to be stitched together in JSON format")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Output in simple format",
        default=False
    )
    parser.add_argument(
        "-r",
        "--root",
        help="The root coordinate, including the product and the version, separated by a colon(:)",
        default=None
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output path",
        default=None
    )

    args = parser.parse_args()

    stitcher = Stitcher(args.call_graph, args.simple, args.root)
    stitcher.stitch_for_rq1()
    output = json.dumps(stitcher.output(), indent=2)
    ReachabilityDetector(stitcher.output(), args.root)
    if args.output:
        with open(args.output, "w+") as f:
            f.write(output)
    else:
        print (output)

if __name__ == "__main__":
    main()
