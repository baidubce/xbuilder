import unittest
import appbuilder
import requests
import tempfile
import os
from appbuilder.core.console.appbuilder_client.event_handler import AppBuilderEventHandler

class MyEventHandler(AppBuilderEventHandler):
    def get_current_weather(self, location=None, unit="摄氏度"):
        return "{} 的温度是 {} {}".format(location, 20, unit)
    
    def interrupt(self, run_context, run_response):
        thought = run_context.current_thought
        # 绿色打印
        print("\033[1;32m", "-> Agent 中间思考: ", thought, "\033[0m")

        tool_output = []
        for tool_call in run_context.current_tool_calls:
            tool_call_id = tool_call.id
            tool_res = self.get_current_weather(
                **tool_call.function.arguments)
            # 蓝色打印
            print("\033[1;34m", "-> 本地ToolCall结果: ", tool_res, "\033[0m\n")
            tool_output.append(
                {
                    "tool_call_id": tool_call_id,
                    "output": tool_res
                }
            )
        return tool_output
    
    def running(self, run_context, run_response):
        print("\n\033[1;31m","-> Agent 流式回答: \n", run_response.answer, "\033[0m")
        
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
                            "unit": {"type": "string", "enum": ["摄氏度", "华氏度"]},
                        },
                        "required": ["location", "unit"],
                    },
                },
            }
        ]

        cities = ["北京", "上海", "广州"]
        query = "下面这些城市的天气怎么样：{}".format(",".join(cities))

        with builder.run_with_handler(
            conversation_id = conversation_id,
            query = query,
            tools = tools,
            stream = True,
            event_handler = MyEventHandler(),
        ) as run:
            run.until_done()

        
if __name__ == '__main__':
    unittest.main()
