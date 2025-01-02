import unittest
import appbuilder
import requests
import tempfile
import os

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
class TestAppBuilderClient(unittest.TestCase):
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
            tools=tools,
            stream=True)
        for res in msg.content:
            print(res.model_dump_json(indent=4))
            if len(res.events) > 0:
                event = res.events[-1]

        assert event.status == "interrupt"
        assert event.event_type == "Interrupt"

        msg_2 = builder.run(
            conversation_id=conversation_id,
            tool_outputs=[
                {
                    "tool_call_id": event.tool_calls[-1].id,
                    "output": "北京今天35度"
                }
            ],
            stream=True
        )

        for res in msg_2.content:
            print(res.model_dump_json(indent=4))


if __name__ == '__main__':
    unittest.main()
