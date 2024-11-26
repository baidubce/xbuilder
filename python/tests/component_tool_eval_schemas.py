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
from appbuilder.tests.component_schemas import text_schema, url_schema, image_schema, code_schema, file_schema, oral_text_schema, references_schema, chart_schema, audio_schema, plan_schema, function_call_schema

components_tool_eval_output_json_maps = {
    "AnimalRecognition": [text_schema],
    "ASR": [text_schema],
    "TreeMind": [text_schema, url_schema],
    "ImageUnderstand": [text_schema],
    "Text2Image": [url_schema]
}