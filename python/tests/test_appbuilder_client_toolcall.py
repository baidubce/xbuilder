import unittest
import appbuilder
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
        client = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = client.create_conversation()
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
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                            },
                        },
                        "required": ["location", "unit"],
                    },
                },
            }
        ]

        msg = client.run(
            conversation_id=conversation_id, query="今天北京天气怎么样？", tools=tools
        )
        print(msg.model_dump_json(indent=4))

        event = msg.content.events[-1]
        assert event.status == "interrupt"
        assert event.event_type == "Interrupt"

        msg_2 = client.run(
            conversation_id=conversation_id,
            tool_outputs=[
                {"tool_call_id": event.tool_calls[-1].id, "output": "北京今天35度"}
            ],
        )
        print(msg_2.model_dump_json(indent=4))

    def test_appbuilder_client_tool_call_from_function(self):
        """测试functions2model功能"""
        # 定义本地函数
        def get_current_weather(location: str, unit: str) -> str:
            """获取指定中国城市的当前天气信息。

            仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。

            Args:
                location (str): 城市名，例如："北京"。
                unit (int): 温度单位，支持 "celsius" 或 "fahrenheit"。

            Returns:
                str: 天气情况描述
            """
            return "北京今天25度"

        # 定义函数列表
        functions = [get_current_weather]
        function_map = {f.__name__: f for f in functions}

        client = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = client.create_conversation()
        msg = client.run(
            conversation_id=conversation_id,
            query="今天北京的天气怎么样？",
            tools=[
                appbuilder.Manifest.from_function(f) for f in functions
            ],
        )
        print(msg.model_dump_json(indent=4))
        event = msg.content.events[-1]
        tool_call = event.tool_calls[-1]

        # 获取函数名称和参数
        name = tool_call.function.name
        args = tool_call.function.arguments

        # 将函数名称映射到具体的函数并执行
        raw_result = function_map[name](**args)

        # 传递工具的输出
        msg_2 = client.run(
            conversation_id=conversation_id,
            tool_outputs=[{"tool_call_id": tool_call.id, "output": str(raw_result)}],
        )
        print(msg_2.model_dump_json(indent=4))

    def test_appbuilder_client_tool_call_from_function_decorator(self):    
        @appbuilder.manifest(
            description="获取指定中国城市的当前天气信息。仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。"
        )
        @appbuilder.manifest_parameter(
            name="location", description="城市名，例如：北京。"
        )
        @appbuilder.manifest_parameter(
            name="unit", description="温度单位，支持 'celsius' 或 'fahrenheit'"
        )
        # 定义示例函数
        def get_current_weather(location: str, unit: str) -> str:
            return "北京今天25度"

        # 定义函数列表
        functions = [get_current_weather]
        function_map = {f.__name__: f for f in functions}
        # 调用大模型
        client = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = client.create_conversation()
        msg = client.run(
            conversation_id=conversation_id,
            query="今天北京的天气怎么样？",
            tools=[
                appbuilder.Manifest.from_function(f) for f in functions
            ],
        )
        print(msg.model_dump_json(indent=4))
        # 获取最后的事件和工具调用信息
        event = msg.content.events[-1]
        tool_call = event.tool_calls[-1]

        # 获取函数名称和参数
        name = tool_call.function.name
        args = tool_call.function.arguments

        # 将函数名称映射到具体的函数并执行
        raw_result = function_map[name](**args)

        # 传递工具的输出
        msg_2 = client.run(
            conversation_id=conversation_id,
            tool_outputs=[{"tool_call_id": tool_call.id, "output": str(raw_result)}],
        )
        print(msg_2.model_dump_json(indent=4))


if __name__ == "__main__":
    unittest.main()
