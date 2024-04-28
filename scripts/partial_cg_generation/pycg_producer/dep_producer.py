#
# Copyright (c) 2018-2020 FASTEN.
#
# This file is part of FASTEN
# (see https://www.fasten-project.eu/).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import os
import json
import shutil
import datetime
import subprocess as sp

from pathlib import Path
from distutils import dir_util


class CallGraphGenerator:
    def __init__(self, source_dir, release):
        self.release = release
        self.output = { "Status":"",
                        "Output":""}
        self.release_msg = release
        coordinate = release.split(":")
        if len(coordinate)<2:
            self._format_error("Data Reading", 'Error, cannot unpack{}'.format(str(release)))
            raise CallGraphGeneratorError()
        self.product, self.version = release.split(":")
        self.source_dir = Path(source_dir)
        self.plugin_name = "PyCG"
        self.plugin_version = "0.0.1"
        # template for error messages
        self.error_msg = {
            'product': self.product,
            'version': self.version,
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
        self.out_root = Path("tmp1/"+release)
        self.out_dir = self.out_root/self.product/self.version
        self.out_file = self.out_dir/'cg.json'
        self.downloads_dir = self.out_root/"downloads"
        self.untar_dir = self.out_root/"untar"

        # Where the source code will be stored
        self.source_path = self.source_dir/("sources/{}/{}/{}".format(
                    self.product[0], self.product, self.version))
        # Where the call graphs will be storedn
        self.cg_path = self.source_dir/("callgraphs/{}/{}/{}".format(
                    self.product[0], self.product, self.version))
        self._create_dir(self.source_dir)
        self._create_dir(self.out_dir)


    def generate(self):
        try:
            comp = self._download()
            self._copy_source(comp)
            cg_path = self._generate_callgraph(comp)
            self._produce_callgraph(cg_path)
            self._unlink_callgraph(cg_path)
        except CallGraphGeneratorError:
            self._produce_error()
        finally:
            self._clean_dirs()
        return self.output

    def _get_now_ts(self):
        return int(datetime.datetime.now().timestamp())

    def _download(self):
        # Download tar into self.downloads_dir directory
        # return compressed file location
        err_phase = 'download'

        self._create_dir(self.downloads_dir)
        cmd = [
            'pip3',
            'install',
            '--no-deps',
            '-t', self.downloads_dir.as_posix(),
            "{}=={}".format(self.product, self.version)
        ]
        try:
            out, err = self._execute(cmd, None)
        except Exception as e:
            self._format_error(err_phase, str(e))
            raise CallGraphGeneratorError()

        items = list(self.downloads_dir.iterdir())
        if len(items) != 1:
            for i in items:
                lename = i.name.lower()
                product = self.product.lower()
                if not lename.endswith("dist-info") and not lename.endswith("egg-info") and  not lename.endswith("bin"):
                    if ((lename ==product) or  (lename == product.replace("-", "_")) or  (lename in product)):
                        return i
            for i in items:
                lename = i.name
                if lename.endswith(".py"):
                    return i
            # self._format_error(err_phase, 'Expecting a single downloaded item {}'.format(str(items)))
            # raise CallGraphGeneratorError()
        return items[0]

    def _copy_source(self, pkg):
        try:
            if not self.source_path.exists():
                self.source_path.mkdir(parents=True)
            if os.path.isdir(pkg):
                pkg_path = pkg.as_posix()
                # if the package path contains an init file
                # then the PyCG will generate a call graph for its parent
                if (pkg/"__init__.py").exists():
                    pkg_path = pkg.parent.as_posix()

                dir_util.copy_tree(pkg_path, self.source_path.as_posix())
            else:
                fname = os.path.basename(pkg)
                # target_path = self.source_path / fname
                #  if not target_path.parent.exists():
                # print(pkg, (self.source_path/fname).as_posix())
                shutil.copyfile(pkg, (self.source_path/fname).as_posix())
        except Exception as e:
            self._format_error('pkg-copy', str(e))
            raise CallGraphGeneratorError()

    def _generate_callgraph(self, package_path):
        # call pycg using `package'
        x = str(package_path)
        files_list = []
        if not x.endswith(".py"):
            init_files_list = self._get_python_files(package_path)
            exclude_substring = 'test'
            files_list = [s for s in init_files_list if exclude_substring not in s]
            if not files_list:
                files_list = init_files_list
        else:
            files_list.append(package_path)
        # get metrics from the files list
        self.num_files = len(files_list)
        self.loc = self._get_lines_of_code(files_list)
        # if the package path contains an init file
        # then the package is its parent
        if (package_path/"__init__.py").exists():
            package_path = package_path.parent
        cmd = [
            'pycg',
            '--fasten',
            '--package', package_path.as_posix(),
            '--product', self.product,
            '--version', self.version,
            '--forge', 'PyPI',
            '--max-iter', '2',
            '--timestamp', '0',
            '--output', self.out_file.as_posix()
        ] + files_list
        timing = [
            "/usr/bin/time",
            "-f", "secs=%e\nmem=%M"
        ]
        try:
            out, err = self._execute(timing + cmd, None)
        except Exception as e:
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
        excluded_dirs = ["tests", "test", "docs", "examples", "_vendor", "_distutils"]
        return [x.resolve().as_posix().strip() for x in package.glob("**/*.py") if self._should_include(x, excluded_dirs)]

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
        if not cg_path or not cg_path.exists():
            self._format_error('producer',\
                'Call graph path does not exist {}'.format(cg_path))
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

    def _execute(self, opts, timeout):
        cmd = sp.Popen(opts, stdout=sp.PIPE, stderr=sp.PIPE)
        return cmd.communicate(timeout=None)


    def _format_error(self, phase, message):
        self.error_msg['phase'] = phase
        self.error_msg['message'] = message

    def _clean_dirs(self):
        # clean up directories created
        if self.downloads_dir.exists():
            shutil.rmtree(self.downloads_dir.as_posix())
        if self.untar_dir.exists():
            shutil.rmtree(self.untar_dir.as_posix())
        if self.out_root.exists():
            shutil.rmtree(self.out_root.as_posix())

    def _create_dir(self, path):
        if not path.exists():
            path.mkdir(parents=True)

    def copy_top_level_txt(self):
        """
        Re-installs the given package into a temporary directory,
        locates the top_level.txt file, and copies it to the sources directory.
        If top_level.txt is not found, generate a custom one using top directory names.
        """
        temp_install_dir = self.out_root 

        # Step 1: Re-install the package into temp_install_dir
        cmd = [
            'pip3',
            'install',
            '--no-deps',
            '-t', temp_install_dir.as_posix(),
            "{}=={}".format(self.product, self.version)
        ]
        try:
            out, err = self._execute(cmd, None)
        except Exception as e:
            self._format_error('reinstall', str(e))
            print('Exception in install ', self.product, self.version)
        # Step 2: Locate the top_level.txt file
        top_level_file = None
        try:
            for root, dirs, files in os.walk(temp_install_dir):
                if 'top_level.txt' in files:
                    top_level_file = os.path.join(root, 'top_level.txt')
                    break
            if not top_level_file:
                # Generate custom top_level.txt
                top_directories = []
                for item in os.listdir(temp_install_dir):
                    full_path = os.path.join(temp_install_dir, item)
                    if os.path.isdir(full_path) and not item.endswith(('-info', '-INFO')):  # Ignoring common metadata directories
                        top_directories.append(item)
                
                # If we found top directories, write them into a custom top_level.txt
                if top_directories:
                    custom_top_level_path = os.path.join(temp_install_dir, 'top_level.txt')
                    with open(custom_top_level_path, 'w') as f:
                        for dir_name in top_directories:
                            f.write(dir_name + '\n')
                    shutil.copy(custom_top_level_path, self.source_path)
            else:
                shutil.copy(top_level_file, self.source_path)

            # Cleanup: remove the temporary installation directory
            shutil.rmtree(temp_install_dir)
        except Exception as e:
            pass

class CallGraphGeneratorError(Exception):
    pass