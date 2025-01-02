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
                    "description": "支持多个中国城市的天气查询，参数location为一个list，包含多个中国城市名称",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {'items': {'type': 'string'}, 'title': 'Location', 'type': 'array'},
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location", "unit"],
                    },
                },
            }
        ]

        msg = builder.run(
            conversation_id=conversation_id,
            query="今天北京和上海天气怎么样？",
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
                    "output": "北京和上海今天都是35度"
                }
            ]
        )
        print(msg_2.model_dump_json(indent=4))

        
if __name__ == '__main__':
    unittest.main()
