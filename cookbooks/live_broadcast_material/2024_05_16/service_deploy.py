# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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

import os
import appbuilder
from appbuilder.utils.flask_deploy import FlaskRuntime

os.environ["APPBUILDER_TOKEN"] = "密钥"
component = appbuilder.Playground(
    prompt_template="{query}",
    model="ERNIE-Bot"
)

agent = FlaskRuntime(component=component)
agent.serve(port=8091)
