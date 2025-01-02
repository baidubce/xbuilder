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

        cities = ["北京", "上海", "广州", "深圳", "杭州"]
        query = "下面这些城市的天气怎么样：{}".format(",".join(cities))
        msg = builder.run(
            conversation_id=conversation_id,
            query=query,
            tools=tools)
        print("------ Response: --------\n")
        print(msg.model_dump_json(indent=4))
        print("------ End of response--------\n")
        event = msg.content.events[-1]

        idx = 0
        while True:
            if event.status == "success":
                break

            msg_2 = builder.run(
                conversation_id=conversation_id,
                tool_outputs=[
                    {
                        "tool_call_id": event.tool_calls[-1].id,
                        "output": "{}今天的温度是35度".format(cities[idx])
                    }
                ]
            )
            idx += 1
            print("------ Response: --------\n")
            print(msg_2.model_dump_json(indent=4))
            print("------ End of response--------\n")
            event = msg_2.content.events[-1]
        
        print(msg.content.answer)

        
        

if __name__ == '__main__':
    unittest.main()
