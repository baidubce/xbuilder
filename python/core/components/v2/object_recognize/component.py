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

"""object recognize component."""

import base64
import json
import os

from appbuilder.core._client import HTTPClient
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.components.object_recognize.model import *
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace

class ObjectRecognition(Component):
    r"""
       提供通用物体及场景识别能力，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的多
       个物体及场景标签。

       Examples:

       .. code-block:: python

           import appbuilder
           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           object_recognition = appbuilder.ObjectRecognition()
           with open("./object_recognition_test.jepg", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
           print(out.content)

        """
    name = "object_recognition"
    version = "v1"

    manifests = [
        {
            "name": "object_recognition",
            "description": "提供通用物体及场景识别能力，即对于输入的一张图片，输出图片中的多个物体及场景标签。",
            "parameters": {
                "type": "object",
                "properties": {
                    "img_url": {
                        "type": "string",
                        "description": "待识别图片的url,根据该url能够获取图片"
                    },
                    "img_name": {
                        "type": "string",
                        "description": "待识别图片的文件名,用于生成图片url"
                    }
                },
                "anyOf": [
                    {
                        "required": [
                            "img_url"
                        ]
                    },
                    {
                        "required": [
                            "img_name"
                        ]
                    }
                ]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        """
        通用物体识别
        
        Args:
            message (Message): 输入图片或图片url下载地址用于执行识别操作。
                例如: Message(content={"raw_image": b"..."}) 或 Message(content={"url": "https://image/download/url"})。
            timeout (float, optional): HTTP超时时间，默认为None。
            retry (int, optional): HTTP重试次数，默认为0。
        
        Returns:
            Message: 模型识别结果。
                例如: Message(content={"result":[{"keyword":"苹果",
                    "score":0.94553,"root":"植物-蔷薇科"},{"keyword":"姬娜果","score":0.730442,"root":"植物-其它"},
                    {"keyword":"红富士","score":0.505194,"root":"植物-其它"}]})
        """
        inp = ObjectRecognitionInMsg(**message.content)
        req = ObjectRecognitionRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        result, _ = self._recognize(req, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = ObjectRecognitionOutMsg(**result_dict)
        return Message(content=out.model_dump())

    def _recognize(self, request: ObjectRecognitionRequest, timeout: float = None,
                  retry: int = 0, request_id: str = None) -> ObjectRecognitionResponse:
        r"""调用底层接口进行通用物体与场景识别
                   参数:
                       request (obj: `ObjectRecognitionRequest`) : 通用物体与场景识别输入参数
                   返回：
                       response (obj: `ObjectRecognitionResponse`): 通用物体与场景识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError("request format error, one of image or url must be set")

        data = ObjectRecognitionRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v2/advanced_general")
        response = self.http_client.session.post(url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id,data)
        object_response = ObjectRecognitionResponse.from_json(payload=json.dumps(data))
        object_response.request_id = request_id
        return object_response, data

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request (dict) : 通用物体与场景识别body返回
            返回：
                无
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )

    @components_run_stream_trace
    def tool_eval(self,
                  img_url: str = '',
                  img_name: str = '',
                  **kwargs):
        """
        对给定的图片进行物体识别，并返回识别结果。
        
        Args:
            img_url (str, optional): 图片的URL地址。默认为空字符串。
            img_name (str, optional): 图片的名称。默认为空字符串。
            **kwargs: 其他关键字参数。
        
        Returns:
            Generator[Output, NoneType, NoneType]: 生成器，包含识别结果的输出对象。
        
        Raises:
            InvalidRequestArgumentError: 如果请求格式错误，例如文件名未设置或文件URL不存在，则引发此异常。
        
        """
        traceid = kwargs.get("_sys_traceid")
        if not img_url:
            file_urls = kwargs.get("_sys_file_urls", {})
            img_path = img_name
            if not img_path:
                raise InvalidRequestArgumentError("request format error, file name is not set")
            img_name = os.path.basename(img_path)
            img_url = file_urls.get(img_name, None)
            if not img_url:
                raise InvalidRequestArgumentError(f"request format error, file {img_name} url does not exist")
        score_threshold = kwargs.get("score_threshold", 0.5)
        req = ObjectRecognitionRequest(url=img_url)
        result, raw_data = self._recognize(req, request_id=traceid)
        result = proto.Message.to_dict(result)
        results = []
        for item in result["result"]:
            if item["score"] < score_threshold and len(results) > 0:
                continue
            res = {
                "物体或场景名称": item["keyword"],
                "置信度": item["score"],
                "所属类别": item["root"],
            }
            results.append(res)
        res = json.dumps(results, ensure_ascii=False, indent=4)
        yield self.create_output(type="text", text=res, raw_data=raw_data, visible_scope='llm')
        yield self.create_output(type="text", text="", raw_data=raw_data, visible_scope='user')