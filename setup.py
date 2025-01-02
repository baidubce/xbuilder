# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Setup script.

Authors: dongdaxiang(dongdaxiang@baidu.com)
Date:    2023/12/01 11:19:24
"""

import os
import shutil
import datetime
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


now = datetime.datetime.now()
timestamp_str = now.strftime("%Y%m%d_%H%M%S")
package_dir = f"appbuilder_sdk_{timestamp_str}"
if not os.path.exists(package_dir):
    os.makedirs(package_dir)

shutil.copytree("python", os.path.join(package_dir, "appbuilder"))
shutil.copy("requirements.txt", package_dir)

packages = find_packages(where=package_dir)
package_data = {}
print(packages)
for package in packages:
    if package.startswith('appbuilder.utils'):
        package_data[package] = ["*.md"]

serve_require = ["chainlit~=1.0.200", "flask~=2.3.2", "flask-restful==0.3.9", "arize-phoenix==4.5.0"]
trace_require = ["SQLAlchemy==2.0.31"]
test_require = ["python-dotenv"]
langchain_require = ["langchain==0.3.0", "datamodel-code-generator==0.25.8"]
all_require = serve_require + trace_require + test_require + langchain_require

setup(
    name="appbuilder-sdk",
    # NOTE(chengmo): 修改此版本号时，请注意同时修改 __init__.py 中的 __version__
    version='0.9.8.3', 
    author="dongdaxiang",
    author_email="dongdaxiang@baidu.com",
    packages=packages,
    package_data=package_data,
    package_dir={'': package_dir}, 
    install_requires=requirements,
    python_requires=">=3.9",
    extras_require={
        "serve": serve_require,
        "trace": trace_require,
        "test": test_require,
        "langchain": langchain_require,
        "all": all_require
    },
    entry_points={
        "console_scripts": [
            "appbuilder_bce_deploy=appbuilder.utils.bce_deploy:deploy",
            "appbuilder_trace_server=appbuilder.utils.trace.phoenix_wrapper:runtime_main"
        ]
    },
    description="百度智能云千帆AppBuilder-SDK",
    long_description="百度智能云千帆AppBuilder, 开箱即用的组件与框架, 高效开发你的AI原生应用, 更多信息请登录: https://appbuilder.cloud.baidu.com/",
    url="https://github.com/baidubce/app-builder",
)

shutil.rmtree(package_dir)
