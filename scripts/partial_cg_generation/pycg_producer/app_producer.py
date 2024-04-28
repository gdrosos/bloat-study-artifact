import os
import json
import datetime
import subprocess as sp
import os
import signal

from pathlib import Path




class CallGraphGenerator:
    def __init__(self, source_dir, release):
        self.release = release
        self.output = { "Status":"",
                        "Output":""}
        self.release_msg = release 
        self.product= release
        self.source_dir = Path(source_dir)
        self.plugin_name = "PyCG"
        self.plugin_version = "0.0.1"
        # template for error messages
        self.error_msg = {
            'product': self.product,
            'phase': '',
            'message': ''
        }
        # elapsed time for generating call graph
        self.elapsed = None
        # lines of code of package
        self.loc = None
        # maximum resident set size
        self.max_rss = None
        # number of files in the package
        self.num_files = None

        # Root directory for tmp data
        x = "tmp1/"+release.split("/")[0]+release.split("/")[1]
        self.out_root = Path(x)
        self.out_file = self.out_root/'cg.json'
        self._create_dir(self.out_root)

        # Where the source code will be stored
        self.source_path = self.source_dir/("sources/apps/{}".format(
                    release))
        # Where the call graphs will be stored
        self.cg_path = self.source_dir/("callgraphs/apps/{}".format(
                    release))

    def generate(self):
        try:
            cg_path = self._generate_callgraph(self.source_path)
            self._produce_callgraph(cg_path)
            self._unlink_callgraph(cg_path)
        except CallGraphGeneratorError:
            self._produce_error()
        finally:
            return self.output

    def _get_now_ts(self):
        return int(datetime.datetime.now().timestamp())


   

    def _generate_callgraph(self, package_path):
        # call pycg using `package`

        files_list = self._get_python_files(package_path)


        # x = []
        # for i in files_list:
        #     if "/docs/" not in i:
        #         x.append(i)
        # files_list = x
        # get metrics from the files list
        self.num_files = len(files_list)
        self.loc = self._get_lines_of_code(files_list)
        # if the package path contains an init file
        # then the package is its parent


        cmd = [
            'pycg',
            '--fasten',
            '--package', package_path.as_posix(),
            '--product', self.product,
            '--version', '1',
            '--forge', 'PyPI',
            '--timestamp', '0',
            '--output', self.out_file.as_posix()
        ] + files_list
        timing = [
            "/usr/bin/time",
            "-f", "secs=%e\nmem=%M"
        ]

        try:
            process1 = sp.Popen(timing + cmd, stdout=sp.PIPE, stderr=sp.PIPE)
            pid = process1.pid 
            out, err = process1.communicate(None)
        except Exception as e:
            os.kill(pid, signal.SIGTERM)
            self._format_error('generation', str(e))
            raise CallGraphGeneratorError()

        if not self.out_file.exists():
            self._format_error('generation', err.decode('utf-8'))
            raise CallGraphGeneratorError()

        for l in err.decode('utf-8').splitlines():
            if l.strip().startswith("secs"):
                self.elapsed = float(l.split("=")[-1].strip())
            if l.strip().startswith("mem"):
                self.max_rss = int(l.split("=")[-1].strip())

        return self.out_file

    def _should_include(self, file_path, excluded_dirs):
        return not any(excluded_dir in file_path.parts[:-1] for excluded_dir in excluded_dirs)

    def _get_python_files(self, package):
        excluded_dirs = ["tests", "test", "docs", "examples"]
        return [x.resolve().as_posix().strip() for x in package.glob("**/*.py") if self._should_include(x, excluded_dirs)]
    # def _get_python_files(self, package):
    #     return [x.resolve().as_posix().strip() for x in package.glob("**/*.py")]

    def _get_lines_of_code(self, files_list):
        res = 0
        for fname in files_list:
            with open(fname) as f:
                try:
                    res += sum(1 for l in f if l.rstrip())
                except UnicodeDecodeError as e:
                    continue

        return res


    def _produce_callgraph(self, cg_path):
        # produce call graph to kafka topic
        if not cg_path.exists():
            self._format_error('producer',\
                'Call graph path does not exist {}'.format(cg_path.as_posix()))
            raise CallGraphGeneratorError()

        with open(cg_path.as_posix(), "r") as f:
            try:
                cg = json.load(f)
            except Exception:
                self._format_error('producer',\
                    'Call graph path does is not JSON formatted {}. Contents {}'.format(cg_path.as_posix(), f.read()))
                raise CallGraphGeneratorError()


        if not cg.get("metadata"):
            cg["metadata"] = {}

        cg["metadata"]["loc"] = self.loc or -1
        cg["metadata"]["time_elapsed"] = self.elapsed or -1
        cg["metadata"]["max_rss"] = self.max_rss or -1
        cg["metadata"]["num_files"] = self.num_files or -1
        cg["sourcePath"] = self.source_path.as_posix()

        # store it
        self._store_cg(cg)

        output = dict(
                payload=cg,
                plugin_name=self.plugin_name,
                plugin_version=self.plugin_version,
                input=self.release,
                created_at=self._get_now_ts()
        )

        self.output["Status"] = "Success"
        self.output["Output"] = output

    def _store_cg(self, out_cg):
        if not self.cg_path.exists():
            self.cg_path.mkdir(parents=True)

        with open((self.cg_path/"cg.json").as_posix(), "w+") as f:
            f.write(json.dumps(out_cg))

    def _unlink_callgraph(self, cg_path):
        if not cg_path.exists():
            self._format_error('deleter',
                'Call graph path does not exist {}'.format(cg_path.as_posix()))
            raise CallGraphGeneratorError()
        cg_path.unlink()

    def _produce_error(self):
        # produce error
        output = dict(
            plugin_name=self.plugin_name,
            plugin_version=self.plugin_version,
            input=self.release,
            created_at=self._get_now_ts(),
            err=self.error_msg
        )
        self.output["Status"] = "Fail"
        self.output["Output"] = output

    def _format_error(self, phase, message):
        self.error_msg['phase'] = phase
        self.error_msg['message'] = message

    def _create_dir(self, path):
        if not path.exists():
            path.mkdir(parents=True)


class CallGraphGeneratorError(Exception):
    pass