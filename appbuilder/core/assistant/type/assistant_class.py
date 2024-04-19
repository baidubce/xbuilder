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

from pydantic import BaseModel
from pydantic import Field
from typing import Union
from typing import Optional
from enum import Enum


class AssitantFileInfo(BaseModel):
    url: str = ""
    url_type: str = ""
    file_name: str = ""
    file_id: str = ""


class AssistantAnnotation(BaseModel):
    type: str = "file_info"
    text: str = ""
    start_index: int = 0
    end_index: int = 0
    file_info: Union[AssitantFileInfo, None] = None


class AssistantText(BaseModel):
    value: str = ""
    annotations: Union[list[str], None] = None


class AssistantContent(BaseModel):
    type: str = "text"
    text: Union[AssistantText, None] = None


class AssistantMessage(BaseModel):
    content: str
    role: str = "user"
    file_ids: list[str] = []


class AssistantMessageCreateRequest(BaseModel):
    thread_id: str
    role: str = 'user'
    content: str
    file_ids: Union[list[str], None] = []


class AssistantMessageCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    name: str = ""
    role: str = ""
    content: Union[list[AssistantContent], None] = []
    metadata: Union[dict, None] = None
    created_at: int = 0
    thread_id: str = ""
    content_type: str = 'text'
    assistant_id: Union[str, None] = ""
    run_id: Union[str, None] = ""
    file_ids: Union[list[str], None] = []


class AssistantFilesCreateResponse(BaseModel):
    id: str = ""
    bytes: int = 0
    object: str = ""
    purpose: str = ""
    create_at: int = 0
    filename: str = ""
    classification_id: str = ""


class AssistantFunctionCall(BaseModel):
    name: str
    arguments: str


class AssistantExample(BaseModel):
    role: str = "user"
    content: str
    function_call: AssistantFunctionCall


class AssistantFunctionJsonSchema(BaseModel):
    type: str = 'object'
    properties: Union[dict, None] = None
    required: Union[list[str], None] = None


class AssistantFunction(BaseModel):
    name: str
    description: str
    parameters: Union[AssistantFunctionJsonSchema, None] = None
    responses:  Union[AssistantFunctionJsonSchema, None] = None
    examples: Union[list[list[AssistantExample]], None] = None


class AssistantTool(BaseModel):
    type: str = 'function'
    function: AssistantFunction = None


class ResponseFormat(str, Enum):
    TEXT = 'text'
    JSON_OBJECT = 'json_object'


class AssistantModel(str, Enum):
    ERNIE_408K = 'ERNIE-4.0-8K'

class AssistantCreateRequest(BaseModel):
    model: AssistantModel = Field(default="ERNIE-4.0-8K")
    name: str = Field(default="", min_length=1,
                      max_length=64, pattern="^[0-9a-zA-Z_-]+$")
    description: str = Field(default="", max_length=512)
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)
    instructions: str = Field(default="", max_length=4096)
    thought_instructions: str = Field(default="", max_length=4096)
    chat_instructions: str = Field(default="", max_length=4096)
    tools: list[AssistantTool] = Field(default=[], max_length=10)
    file_ids: list[str] = Field(default=[], max_length=10)
    metadata: dict = Field(default={}, max_length=16)
    assistant_id: str = ""


class AssistantCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    name: str = ""
    description: str = ""
    instructions: str
    tools: Optional[list[AssistantTool]] = Field(default=[])
    created_at: int = 0
    thought_instructions: str = ""
    chat_instructions: str = ""
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)
    file_ids: Optional[list[str]] = Field(default=[])
