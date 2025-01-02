import unittest
import appbuilder
import requests
import tempfile
import os

tools = {
    "name": "get_weather",
    "description": "这是一个获得指定地点天气的工具",
    "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "省，市名，例如：河北省"
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "摄氏度",
                        "华氏度"
                    ]
                }
            },
        "required": [
                "location"
            ]
    }
}

from appbuilder.core.console.appbuilder_client.event_handler import (
    AppBuilderEventHandler,
)

class MyEventHandler(AppBuilderEventHandler):
    def get_weather(self, location: str, unit: str):
        return "{} 的当前温度是30 {}".format(location, unit)
    
    def messages(self, event):
        info = ""
        print("\n\033[1;31m","-> Agent 回答: ", info, "\033[0m")

    def tool_calls(self, event):
        current_tool_calls = None
        for tool_call in current_tool_calls:
            tool_call_id = tool_call.id
            func_name = tool_call.function.name
            arguments = tool_call.function.arguments

            result = ""
            if func_name == "get_weather":
                result = self.get_weather(**arguments)
            
        return [result]
                


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
class TestAppbuilderClient(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "b2a972c5-e082-46e5-b313-acbf51792422"


    def test_appbuilder_client_tool_call(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
    
        Args:
            self (unittest.TestCase): unittest的TestCase对象
    
        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "仅支持中国城市的天气查询，参数location为中国城市名称，其他国家城市不支持天气查询",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市名，举例：北京",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location", "unit"],
                    },
                },
            }
        ]

        msg = builder.run(
            conversation_id=conversation_id,
            query="今天北京天气怎么样？",
            tools=tools)
        print(msg.model_dump_json(indent=4))

        event = msg.content.events[-1]
        assert event.status == "interrupt"
        assert event.event_type == "Interrupt"

        msg_2 = builder.run(
            conversation_id=conversation_id,
            tool_outputs=[
                {
                    "tool_call_id": event.tool_calls[-1].id,
                    "output": "北京今天35度"
                }
            ]
        )
        print(msg_2.model_dump_json(indent=4))

        
        

if __name__ == '__main__':
    unittest.main()
