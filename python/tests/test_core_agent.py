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
import json
import os
import unittest
import random

from appbuilder.core.components.llms.style_writing import StyleWriting
from appbuilder.utils.flask_deploy import FlaskRuntime
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.utils.sse_util import SSEClient


def generate_event(case):
    # 模拟正常事件
    if case == "normal":
        yield "event1"
        yield "event2"
        yield "event3"
    # 模拟首包一定概率出错
    elif case == "head_may_failed":
        num = random.randint(1, 100)
        if num < 20:
            raise Exception("事件生成报错")
        else:
            yield "event1"
    # 模型中包出错
    elif case == "middle_failed":
        yield "event1"
        raise Exception("事件生成报错")
    # 模拟首包总是报错
    elif case == "head_always_failed":
        raise Exception("事件生成报错")


# 模拟流式事件生成报错
class FakeComponent1(Component):
    def run(self, message, stream, **kwargs):
        # 模拟流式调用
        if stream:
            case = kwargs["case"]
            return Message(content=generate_event(case))
        else:
            return Message(content="result")


# 模拟组件内部执行报错
class FakeComponent2(Component):
    def run(self, message, stream, **kwargs):
        # 内部执行报错
        raise Exception("内部执行报错")


class TestCoreAgent(unittest.TestCase):
    def setUp(self):
        pass

    def test_core_agent_create_flask1(self):
        component = FakeComponent1()
        # agent = FlaskRuntime(component=StyleWriting(model="eb"))
        agent = FlaskRuntime(component=component)

        app = agent.create_flask_app()
        client = app.test_client()
        payload = {
            "stream": False,
            "message": "message",
        }
        # 非流式请求
        rsp = client.post("http://127.0.0.1:8080/chat", json=payload)
        assert (rsp.json["code"] == 0)

        # 流式请求
        for case in ["normal", "head_may_failed", "middle_failed", "head_always_failed"]:
            payload = {
                "stream": True,
                "message": "message",
                "case": case
            }
            if case == "normal":
                rsp = client.post("http://127.0.0.1:8080/chat", json=payload)
                data_chunks = rsp.data.splitlines(keepends=True)
                for event in SSEClient(data_chunks).events():
                    d = json.loads(event.data)
                    self.assertEqual(d["code"], 0)
            if case == "head_may_failed":
                for i in range(5):
                    rsp = client.post("http://127.0.0.1:8080/chat", json=payload)
                    data_chunks = rsp.data.splitlines(keepends=True)
                    for event in SSEClient(data_chunks).events():
                        d = json.loads(event.data)
                        self.assertEqual(d["code"], 0)
            if case == "middle_failed":
                rsp = client.post("http://127.0.0.1:8080/chat", json=payload)
                data_chunks = rsp.data.splitlines(keepends=True)
                i = 0
                for event in SSEClient(data_chunks).events():
                    d = json.loads(event.data)
                    if i == 0:
                        self.assertEqual(d["code"], 0)
                    if i == 1:
                        self.assertNotEqual(d["code"], 0)
                    i += 1

            if case == "head_always_failed":
                rsp = client.post("http://127.0.0.1:8080/chat", json=payload)
                data_chunks = rsp.data.splitlines(keepends=True)
                for event in SSEClient(data_chunks).events():
                    self.assertNotEqual(d["code"], 0)

    def test_core_agent_create_flask2(self):
        component = FakeComponent2()
        agent = FlaskRuntime(component=component)
        app = agent.create_flask_app()
        client = app.test_client()
        payload = {
            "stream": False,
            "message": "message",
        }
        # 非流式请求
        rsp = client.post("http://127.0.0.1:8080/chat", json=payload)
        assert (rsp.json["code"] != 0)

        payload = {
            "stream": True,
            "message": "message",
        }
        # 流式请求
        rsp = client.post("http://127.0.0.1:8080/chat", json=payload)
        data_chunks = rsp.data.splitlines(keepends=True)
        for event in SSEClient(data_chunks).events():
            d = json.loads(event.data)
            self.assertNotEqual(d["code"], 0)


if __name__ == '__main__':
    unittest.main()
