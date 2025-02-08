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


r"""Text2Image model.py.
"""
from typing import MutableSequence, List

from typing import Optional, Union
import proto
from pydantic import BaseModel, Field


class Text2ImageSubmitRequest(BaseModel):
    prompt: str = Field(default='')
    width: int = Field(default=1024)
    height: int = Field(default=1024)
    image_num: int = Field(default=1, ge=1, le=8)
    image: Optional[str] = Field(default="")
    url: Optional[str] = Field(default="")
    pdf_file: Optional[str] = Field(default="")
    pdf_file_num: Optional[str] = Field(default="")
    change_degree: Optional[int] = None
    text_content: Optional[str] = None
    task_time_out: Optional[int] = None
    text_check: Optional[int] = None


class Text2ImageSubmitErrorDetail(BaseModel):
    msg: Optional[str] = Field(default=None)
    word: Optional[object] = Field(default=None)
    words: Optional[list] = Field(default=None)


class Text2ImageSubmitResponseData(BaseModel):
    primary_task_id: Optional[int] = None
    task_id: Optional[str] = None


class Text2ImageSubmitResponse(BaseModel):
    log_id: Optional[int] = None
    data: Optional[Text2ImageSubmitResponseData] = Text2ImageSubmitResponseData()
    error_msg: Optional[str] = None
    error_detail: Union[list[Text2ImageSubmitErrorDetail], Text2ImageSubmitErrorDetail, None] = None
    error_code: Optional[int] = None


class Text2ImageQueryRequest(BaseModel):
    task_id: Optional[str]


class FinalImage(BaseModel):
    img_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    img_approve_conclusion: Optional[str] = None


class SubTaskResult(BaseModel):
    sub_task_status: Optional[str] = None
    sub_task_progress_detail: Union[int, float, None] = None
    sub_task_progress: Union[float, int, None] = None
    sub_task_error_code: Optional[int] = None
    final_image_list: Optional[list[FinalImage]] = None


class Text2ImageQueryResponseData(BaseModel):
    task_id: Optional[int] = None
    task_status: Optional[str] = None
    task_progress_detail: Union[float, int, None] = None
    task_progress: Union[float, int, None] = None
    sub_task_result_list: Optional[list[SubTaskResult]] = None


class Text2ImageQueryResponse(BaseModel):
    log_id: Union[str, int, None] = None
    data: Optional[Text2ImageQueryResponseData] = Text2ImageQueryResponseData()


class Text2ImageInMessage(BaseModel):
    """ 文生图组件输入message.
        参数:
            prompt(str):
                生图的文本描述。仅支持中文、日常标点符号。不支持英文，特殊符号，限制 200 字。
    """
    prompt: str


class Text2ImageOutMessage(BaseModel):
    """ 文生图组件输出message.
        参数:
            img_urls(str):
                图片所在 BOS http 地址，默认 1 小时失效。
    """
    img_urls: List[str]

if __name__ == '__main__':
    msg = {
        'log_id': 1882788580231261430,
        'error_msg': '文本敏感信息拦截', 
        'error_detail': [
            {'msg': '存在自定义文本黑名单不合规', 'words': ['特朗普', '特朗普']}, {'msg': '存在政治敏感不合规', 'words': []}], 'error_code': 282004}
    resp = Text2ImageSubmitResponse(**msg)
    print(resp)