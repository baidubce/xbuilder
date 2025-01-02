import os
import sys
import json
import subprocess
import unittest
import pydantic
import appbuilder
from appbuilder.core.component import Component
from appbuilder.utils.sse_util import SSEClient
from appbuilder import (
    Message,
    Playground,
    AppBuilderClient
)
from appbuilder.utils.flask_deploy import FlaskRuntime
from appbuilder.utils.chainlit_deploy import ChainlitRuntime

class TestRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "aa8af334-df27-4855-b3d1-0d249c61fc08"

    def test_no_token_http(self):
        """ 测试http """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K",
            lazy_certification=True,
        )
        agent = FlaskRuntime(component=component)
        app = agent.create_flask_app(url_rule="/chat")
        app.config['TESTING'] = True
        client = app.test_client()
        
        payload = {
            "message": {"query": "你好"},
            "stream": False
        }
        headers = {}
        response = client.post('/chat', json=payload, headers=headers)
        self.assertNotEqual(response.json.get('code'), 0)
  
    def test_err_http(self):
        """ 测试http """
        print(os.getenv("APPBUILDER_TOKEN", ""))
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K",
            lazy_certification=True,
        )
        agent = FlaskRuntime(component=component)
        app = agent.create_flask_app(url_rule="/chat")
        app.config['TESTING'] = True
        client = app.test_client()
        
        payload = {
            "message": {"query": "你好"},
            "stream": False
        }
        headers = {
            "X-Appbuilder-Authorization": "...",
            "X-Appbuilder-Token": "..."
        }
        response = client.post('/chat', json=payload, headers=headers)
        self.assertNotEqual(response.json.get('code'), 0)
        
    def test_stream_http(self):
        """ 测试http """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K",
            lazy_certification=True,
        )
        agent = FlaskRuntime(component=component)
        app = agent.create_flask_app(url_rule="/chat")
        app.config['TESTING'] = True
        client = app.test_client()
        
        payload = {
            "message": {"query": "你好"},
            "stream": True
        }
        headers = {
            "X-Appbuilder-Authorization": os.environ.get("APPBUILDER_TOKEN", ""),
            "X-Appbuilder-Token": os.environ.get("APPBUILDER_TOKEN", "")
        }
        response = client.post('/chat', json=payload, headers=headers)
        for e in response.text.split("\n\n"):
            data_str = e.strip()
            if data_str:
                data_str = data_str[len("data: "):]
                data = json.loads(data_str)
                self.assertEqual(data.get('code'), 0)
        
    def test_http(self):
        """ 测试http """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K",
            lazy_certification=True,
        )
        agent = FlaskRuntime(component=component)
        app = agent.create_flask_app(url_rule="/chat")
        app.config['TESTING'] = True
        client = app.test_client()
        
        payload = {
            "message": {"query": "你好"},
            "stream": False
        }
        headers = {
            "X-Appbuilder-Authorization": os.environ.get("APPBUILDER_TOKEN", ""),
            "X-Appbuilder-Token": os.environ.get("APPBUILDER_TOKEN", "")
        }
        response = client.post('/chat', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('code'), 0)
        
    def test_init_with_valid_component(self):
        """ 测试在component有效时运行 """
        component = Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K"
        )
        agent = FlaskRuntime(component=component)
        agent = ChainlitRuntime(component=component)

    def test_chat_with_valid_message_and_blocking(self):
        """ 测试在消息有效时处理 """
        component = Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K"
        )
        agent = FlaskRuntime(component=component)
        message = appbuilder.Message({"query": "你好"})
        answer = agent.chat(message, stream=False)
        agent2 = ChainlitRuntime(component=component)
        message = appbuilder.Message({"query": "你好"})
        answer2 = agent2.chat(message, stream=False)
        self.assertIs(type(answer.content), str)
        self.assertIs(type(answer2.content), str)
        
    def test_chat_with_valid_message_and_streaming(self):
        """ 测试在消息有效时处理 """
        component = Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K"
        )
        agent = FlaskRuntime(component=component)
        message = Message({"query": "你好"})
        answer = agent.chat(message, stream=True)
        for it in answer.content:
            self.assertIs(type(it), str)

        agent2 = ChainlitRuntime(component=component)
        message = Message({"query": "你好"})
        answer2 = agent2.chat(message, stream=True)
        for it in answer2.content:
            self.assertIs(type(it), str)
        

    def test_chainlit_agent_component_error(self):
        """ 测试chainlit agent组件错误 """
        component = Component()
        agent = ChainlitRuntime(component=component)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", "-y", "chainlit"]
        )
        with self.assertRaises(ImportError):
            agent.chainlit_agent()
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "chainlit==1.0.200"]
        )
        with self.assertRaises(ValueError):
            agent.chainlit_agent()
        os.environ["APPBUILDER_RUN_CHAINLIT"] = "1"
        agent_builder = AppBuilderClient(self.app_id)
        agent = ChainlitRuntime(component=agent_builder)
        agent.chainlit_agent()


if __name__ == '__main__':
    unittest.main()
