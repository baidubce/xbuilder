# SDK 贡献代码规范

## 组件开发规范

### 组件整体介绍

在无特殊情况下，一个官方组件（class Component）的实现可以拆解为以下几个关键模块，分别是

* def run：组件的run函数，规范体现在该函数的输入和输出
    * 输入规范
    * 输出规范
* def tool_eval：组件功能的核心实现，规范体现在该函数的输入和输出
    * 输入规范
    * 输出规范
* dict manifest：组件参与FunctionCall时，帮助大模型理解组件功能的说明，规范体现在manifest的内容和格式
    * manifest规范

### `run` 函数

#### 消息(Message)
- 构建大模型应用的统一数据结构，基于Pydantic构建，在不同的Component之间流动。Message基类的默认字段是content，类型是Any。
```python
from appbuilder import Message
input_dict = Message({"query": "红烧肉怎么做"})
input_list = Message(["text1", "text2", "text3"])
input_str = Message("红烧肉怎么做")
```

#### `run` 函数输入输出规范

- 所有能力单元的标准结构，以Message结构作为输入输出，内部执行逻辑可在本地执行或调用云端服务，以下是官方组件的实现示例。`run` 函数需要添加 `@components_run_trace` 装饰器，实现对组件的trace。

```python
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

class SimilarQuestionMeta(ComponentArguments):
    """ SimilarQuestionMeta
    """
    message: Message = Field(..., 
                             variable_name="query", 
                             description="输入消息，用于模型的输入，一般为问题。")


class SimilarQuestion(CompletionBaseComponent):
    """ 基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。
    Examples:

        .. code-block:: python
            import os
            import appbuilder

            os.environ["APPBUILDER_TOKEN"] = "..."

            qa_mining = appbuilder.SimilarQuestion(model="Qianfan-Agent-Speed-8K")

            msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
            msg = appbuilder.Message(msg)
            answer = qa_mining(msg)

            print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    def __init__(self, model=None):
        """初始化SimilarQuestionMeta任务。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
        
        Returns:
            None
        
        """
        super().__init__(SimilarQuestionMeta, model=model)

    @components_run_trace
    def run(self, message, stream=False, temperature=1e-10):
        """
        给定输入（message）到模型运行，同时指定运行参数，并返回结果。

        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, stream=stream, temperature=temperature)
```

### `tool_eval` 函数

#### `ComponentOutput` 类

```python
class ComponentOutput(BaseModel):
    role: str = Field(default="tool",
                      description="role是区分当前消息来源的重要字段，对于绝大多数组件而言，都是填写tool，标明role所在的消息来源为组件。部分思考及问答组件，role需要填写为assistant")
    content: list[Content] = Field(default=[],
                                         description="content是当前组件返回内容的主要payload，List[Content]，每个Content Dict 包括了当前输出的一个元素")
```

#### `tool_eval` 函数输入输出规范

- 组件的核心实现，需要添加 `@components_run_stream_trace` 装饰器，实现对组件的trace。

##### `tool_eval` 函数 输入参数

* 组件tool_eval方法的输入，除了在manifest中约定的参数外，也可能会传入以下系统变量，辅助组件的运行。
* 系统入参列表中的字段是保留字段，组件定义的manifest不能与系统参数重名。系统参数中有可以被用户设置的参数例如uploaded_files，也有不能设置的字段例如traceid等。
* 在组件的开发中，以下系统输入字段体现为 def tool_eval(self, key1, key2, \*\*kwargs)中\*\*kwargs包含的内容，key1和key2是manifest中约定的参数，kwargs中的内容是系统入参。

##### `tool_eval` 函数 组件返回字段

* 组件返回参数统一采用json字段，固定key名称和对应的value，value默认是dict类型，value本身需要指定visible_scope。
* 非流式返回结果，按照所有流式内容的key-value进行合并，例如两个event都是references，那么需要两组references合并，所有组件需要支持非流式返回。
* 基于sse协议提供流式数据
* content 本身是个 List[Dict]，每个 Dict是当前 event 的一个元素，一般有多个元素的返回例如 urls/files 才需要多个 Dict

###### 组件返回字段总览

|字段|类型|是否必须|默认值 及 取值范围|作用说明|备注|
|---|---|---|---|---|---|
|role|str|否|- tool 默认<br>- user<br>- assistant<br>|ole是区分当前消息来源的重要字段，对于绝大多数组件而言，都是填写tool，标明role所在的消息来源为组件。部分思考及问答组件，role需要填写为assistant|{"role": "tool"}|
|content|list[dict]|是|[]Event|当前组件返回内容的主要payload，List[Dict]，每个 Dict 包括了当前 event 的一个元素||
|+ name|str|否|part1，part2或者3d_pics，title|介绍当前yield内容的step name使用name的必要条件，是有不同content需要是属于结构上的不同字段，但又是streaming的||
|+ type|str|是|* text 默认<br>* code<br>* files<br>* urls<br>* oral_text<br>* references<br>* image<br>* chart<br>* audio<br>* json|代表event 类型，包括 text、code、files、urls、oral_text、references、image、chart、audio、tought、json<br>该字段的取值决定了下面text字段的内容结构||
|+ text|dict<br>object|是|{}|代表当前 event 元素的内容，每一种 event 对应的 text 结构固定|保留字段<br>"text": {'filename': 'chart_url.png', 'url': 'https://chart_url.png'},|
|+ visible_scope|str|否|all 默认<br>llm<br>user<br>空|为了界面展示明确的说明字段<br>* llm为思考模型可见，类似function calling结果中submit的执行结果<br>* user为终端用户可见|workflow中存在消息通知节点，类型为notice<br>目前实测，llm、user、all用户都可见，只是气泡不一样。llm在下拉框中，user直接输出到气泡中。|
|+ raw_data|dict<br>object|否|{}|内部信息，由开发者请求透传，内部系统返回的信息，例如API节点收到的resp，大模型节点的MB resp|{<br>    "origin_response": "xxxxx"<br>}|
|+ usage|list of dict<br>object|否|{}|大模型的token用量|{<br>    "prompt_tokens": 1547,<br>    "completion_tokens": 2,<br>    "total_tokens": 1549,<br>    "name": "ERNIE Speed-AppBuilder"<br>}|
|+ metrics|dict<br>object|否|{}|耗时、性能、内存等trace及debug所需信息|{<br>    "begin_timestamp": xxxxx<br>    "end_timestamp": xxxxx<br>}|

##### 包含 `manifests` 定义的 `tool_eval` 函数返回示例

```python
class SimilarQuestion(CompletionBaseComponent):
    r""" 
    基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。
    
    Examples:

    .. code-block:: python
        
        import os
        import appbuilder

        os.environ["APPBUILDER_TOKEN"] = "..."

        qa_mining = appbuilder.SimilarQuestion(model="Qianfan-Agent-Speed-8K")

        msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        msg = appbuilder.Message(msg)
        answer = qa_mining(msg)

        print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    manifests = [
        {
            "name": "similar_question",
            "description": "基于输入的问题，挖掘出与该问题相关的类似问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "输入的问题，用于大模型根据该问题输出相关的类似问题。"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ]

    def __init__(
            self,
            model: str="Qianfan-Agent-Speed-8K",
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = True,
    ):
        """初始化StyleRewrite模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
            SimilarQuestionMeta, model=model, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification)

    @components_run_stream_trace
    def tool_eval(self, 
                  query: str,
                  **kwargs):
        """
        根据给定的query和可选参数生成并返回文本输出。
        
        Args:
            query (str): 需要生成文本的输入查询字符串。
            **kwargs: 其他可选参数。
        
        Returns:
            Generator[Output]: 返回一个生成器，生成类型为Output的对象。
        
        """
        traceid = kwargs.get("_sys_traceid")
        msg = Message(query)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, stream=False, temperature=temperature, top_p=top_p, request_id=traceid)
        
        yield self.create_output(type="text", text=str(message.content), name="text", usage=message.token_usage)
```

### `manifest` 规范

* 若组件有tool_eval方法，则必须要求存在manifest
  * 现状：算法手动撰写；未来：提供工具，自动从python函数的入参及注释转manifest
* mainfests是一个list[dict]，是对组件多个能力的规范化描述，如无特殊情况，一般list中只有一个元素，对应tool_eval的能力
* manifest dict要满足json schema协议要求
* 要求manifest dict中parameters-properties定义的参数，与def tool_eval的入参一致
* 组件中的version字段，会影响的组件URL，参考组件API：组件调用形如:
  * /v2/components/${component}/version/{$version}?action=${action}
* 遵循新规范的组件，因输入输出与原组件不兼容，在实现上有显著的标志区分

#### Json Schema协议

- [Json Schema协议](https://json-schema.org/overview/what-is-jsonschema)，以下是示例

```python
class BaiduSearchWithModel(Component):
    r"""
        百度搜索总结工具
    """
    name = "baidu_search_with_model"
    version = "v1" # 修改此处，会影响组件的调用URL
    manifests = [
        {
            "name": "baidu_search_with_model",  # 组件名称
            "description": "对百度搜索结果进行大模型总结",  # 组件描述，该字段重要，影响 function calling 效果
            "parameters": {  # parameters 描述组件入参列表
                "type": "object",
                "properties": { # 多个参数可以指定多个 properties
                    "query": {
                        "type": "string", # 参数query 的类型
                        "description": "搜索关键词" # 参数query 的描述，该字段重要，影响 function calling 效果
                    }
                },
                "required": [
                    "query" # query参数为必填字段
                ]
            }
        }
    ]
```

## 代码合入单元测试规范

* 现状: 当前开源Appbuilder-SDK已经部署了单元测试流水线，并要求90%的单元测试覆盖率合入要求，要求开发者实现完整已开发的代码的端到端的测试，并且要求代码增量行覆盖率为90%

### 单元测试规范

#### 单元测试要求

- 覆盖if-else分支
    - 对于包含if-else逻辑的代码，需要编写测试用例来确保每个分支都被执行到
- 输入的边界条件检查
    - 边界条件通常指的是数据范围的极值（如最小值和最大值），或者特定情况下的特殊值（如空值、空字符串、负值等）  
-  Error raise的覆盖
    - 确保测试覆盖了所有可能抛出异常的代码路径，包括代码自身的预期错误，以及访问远程服务失败后的错误处理

#### Test文件目录

* test文件需要为『test_』开头
* 测试类需要形如『class TestFlaskRuntime(unittest.TestCase)::』的定义方式
* test文件需要置于appbuilder-sdk-ext/appbuilder_sdk_ext/tests路径下

#### UnitTest提供三种标签实现两种运行模式

* 添加下列标签，单元测试脚本实现cpu并行
  * @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
* 不添加标签，单元测试脚本默认使用cpu串行
* 添加下列标签，暂时跳过当前单元测试脚本
  * @unittest.skip(reason="单测暂时跳过")

##### SKIP标签代码示例
```python
@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCreateChatPrompt(unittest.TestCase):
    pass
    
    
class TestCreateChatPrompt(unittest.TestCase):
    pass
    
    
@unittest.skip(reason="单测暂时跳过")
class TestCreateChatPrompt(unittest.TestCase):
    pass
```

#### SDK测试代码示例

下面给出一个通过parameterized库进行多种参数组合的示例，可以大幅简化单测代码，但需注意，多种参数的测试case会并行运行，对服务的QPS有要求

```python
import unittest
from parameterized import parameterized, param
import appbuilder

class TestHandwritingOcr(unittest.TestCase):
    @parameterized.expand([
        param(image_url, None, None),
        param(image_url, None, 0),
        param(image_url, float(120), None),
        param(image_url, None, 1),
        param(image_url, 120.5, 1),
        param(image_url, float(12000), None),
    ])
    def test_normal_case(self, image, timeout, retry):
        """
        正常用例
        """
        # 创建表格识别组件实例
        handwrite_ocr = appbuilder.HandwriteOCR()
        # 执行识别操作并获取结果
        if timeout is None and retry is None:
            out = handwrite_ocr.run(appbuilder.Message(content={"url": image}))
        elif timeout is None:
            out = handwrite_ocr.run(appbuilder.Message(content={"url": image}), retry=retry)
        elif retry is None:
            out = handwrite_ocr.run(appbuilder.Message(content={"url": image}), timeout=timeout)
        else:
            out = handwrite_ocr.run(appbuilder.Message(content={"url": image}), timeout=timeout, retry=retry)
        res = out.content
        self.assertIsNotNone(res["contents"], "识别结果为空")
        self.assertEqual(len(res["contents"]), 6)
    
    @parameterized.expand([
        # timeout为0
        param(image_url, 0, 0, "ValueError", "timeout", 'but the timeout cannot be set to a value '
                                                                'less than or equal to 0.'),
        # timeout为字符串
        param(image_url, "a", 0, "appbuilder.core._exception.InvalidRequestArgumentError", "timeout",
                        'timeout must be float or tuple of float'),
        # timeout为0.1，太短了
        param(image_url, float(0.1), 0, "requests.exceptions.ReadTimeout", "timeout",
                        "Read timed out. (read timeout=0.1)"),
        # retry为字符串
        param(image_url, float(10), "a", "TypeError", "str", "'<' not supported between instances of"
                                                                    " 'str' and 'int'"),
        # image_url错误
        param("https://bj.bcebos.com/v1/appbuilder/xxx", 12.5, 1,
                        "appbuilder.core._exception.AppBuilderServerException", "url",
                        "service_err_message=url format illegal"),
    ])
    def test_abnormal_case(self, image, timeout, retry, err_type, err_param, err_msg):
        """
        异常用例
        """
        try:
            # 创建表格识别组件实例
            handwrite_ocr = appbuilder.HandwriteOCR()
            # 执行识别操作并获取结果
            out = handwrite_ocr.run(appbuilder.Message(content={"url": image}), timeout=timeout, retry=retry)
            res = out.content
            log.info(res)
            assert False, "未捕获到错误信息"
        except Exception as e:
            self.assertIsInstance(e, eval(err_type), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type))
            self.assertIn(err_param, str(e), "捕获的异常参数类型不正确, 预期 参数:{}, 实际:{}".format(err_param, str(e)))
            self.assertIn(err_msg, str(e), "捕获的异常消息不正确， 预期:{}, 实际:{}".format(err_msg, str(e)))
```

## 注释规范

- SDK使用注释自动生成API文档，因此非私有函数的注释需要严格按照Google代码注释规范编写

### object类注释

```python
class AppBuilderClient(Component):
    r"""
    AppBuilderClient 组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)平台上
    构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。
    
    Examples:

    .. code-block:: python

        import appbuilder
        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["APPBUILDER_TOKEN"] = '...'
        # 可在Console 应用页面获取
        app_id = "app_id"
        client = appbuilder.AppBuilderClient("app_id")
        conversation_id = client.create_conversation()
        file_id = client.upload_local_file(conversation_id, "/path/to/file")
        message = client.run(conversation_id, "今天你好吗？")
        # 打印对话结果
        print(message.content)
        
    """
```
- 注意
    - 注释必须使用 Examples:之后必须存在一行空行，.. code-block:: python之后也必须要有一行空行
    - code-block前为两点（..）之后为两个冒号(::)
    - 方法的示例注释与此规范相同

### 函数注释

- 私有函数如_recognize_w_post_process等无需按照规范注释函数

```python
@components_run_stream_trace
def tool_eval(
    self,
    name: str,
    streaming: bool,
    origin_query: str,
    **kwargs,
) -> Union[Generator[str, None, None], str]:
    """
    执行工具函数，通过调用底层接口进行动物识别。
    
    Args:
        name (str): 工具名
        streaming (bool): 是否流式返回结果，True 表示流式返回，False 表示一次性返回
        origin_query (str): 用户原始查询字符串
        **kwargs: 工具调用的额外关键字参数
    
    Returns:
        Union[Generator[str, None, None], str]: 动物识别结果。如果 streaming 为 True，则返回一个生成器，可以逐个返回识别结果；
                                                如果 streaming 为 False，则返回一个字符串，包含识别出的动物类别和相应的置信度信息。
    
    """
```

### google风格指南与规范示例

- Google详情见 [Google注释风格指南](https://google.github.io/styleguide/pyguide.html)
   

```python
class GoogleStyle:
    '''Google注释风格
    用 ``缩进`` 分隔，
    适用于倾向水平，短而简单的文档
    Attributes:
        dividend (int or float): 被除数
        name (:obj:`str`, optional): 该类的命名
    '''
 
    def __init__(self, dividend, name='GoogleStyle'):
        '''初始化'''
        self.dividend = dividend
        self.name = name
 
    def divide(self, divisor):
        '''除法
        Google注释风格的函数，
        类型主要有Args、Returns、Raises、Examples
        Args:
            divisor (int):除数
        Returns:
            除法结果
        Raises:
            ZeroDivisionError: division by zero
        Examples:
        
        .. code-block:: python
        
            # 实例代码
            
        References:
            除法_百度百科  https://baike.baidu.com/item/%E9%99%A4%E6%B3%95/6280598
        '''
        try:
            return self.dividend / divisor
        except ZeroDivisionError as e:
            return e
```
