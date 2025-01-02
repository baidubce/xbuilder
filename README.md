<div align="center">
<img src='docs/image/logo.png' alt='logo' width='700' >
<br>

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.9+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)
</div>

简体中文 | [English](./docs/README_en.md) | [日本語](./docs/README_ja.md)

<br>


## 什么是AppBuilder-SDK

百度智能云千帆AppBuilder-SDK是[百度智能云千帆AppBuilder](https://appbuilder.cloud.baidu.com/)面向AI原生应用开发者提供的一站式开发平台的客户端SDK。

### AppBuilder-SDK 有哪些功能？

百度智能云千帆AppBuilder-SDK提供了以下AI应用开发者的必备功能：

- **调用**
    - 调用大模型，可自由调用您在[百度智能云千帆大模型平台](https://qianfan.cloud.baidu.com/)的模型，开发并调优prompt
    - 调用能力组件，提供40+个源于百度生态的[优质组件](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz#3%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1)，赋能Agent应用
    - 调用AI原生应用，通过[AppBuilderClient](/docs/BasisModule/Platform/Application/appbuilder_client.md)可访问并管理在百度智能云千帆AppBuilder[网页端](https://console.bce.baidu.com/ai_apaas/app)发布的AI原生应用，并可注册本地函数联动端云组件
- **编排**
    - 配置知识库，通过[KnowledgeBase](/docs/BasisModule/Platform/KnowledgeBase/knowledgebase.md)管理知识库，进行文档及知识切片的增删改查，配合[网页端](https://console.bce.baidu.com/ai_apaas/app)开发产业级的`RAG`应用
    - 编排工作流，提供了`Message`、`Component`、`FlaskRuntime`、`ChainlitRuntime`多级工作流抽象，实现工作流编排，并可与LangChain、OpenAI等业界生态能力打通
- **监控**
    - 提供了可视化Tracing、详细DebugLog等监控工具，助力开发者在生产环境应用
- **部署**
    - `FlaskRuntime`支持部署为基于`Flask`与`gunicorn`的API服务
    - `ChainlitRuntime`支持部署为基于`Chainlit`的对话框交互前端
    - 提供了`appbuilder_bce_deploy`工具，可快速部署程序到百度云，提供公网API服务，联动AppBuilder工作流

### 使用 AppBuilder-SDK 可以构建什么应用？

#### **产业级RAG应用**

AppBuilder-SDK提供多类型组件，覆盖以下构建产业级`RAG`应用的完整步骤：
- 文档解析（Parser）
- 文档切片（Chunker）
- 切片向量化（Embedding）
- 索引构建（Indexing）
- 切片召回（Retrieval）
- 答案生成（Answer Generation）

AppBuilder-SDK不仅提供了百度智能云提供的基础能力组件，同时提供经过深度优化的大模型高级能力组件，可以组合下表提供的原子能力组件，构建个性化的RAG应用[RAG 原子能力 CookBook](./cookbooks/end2end_application/rag/rag.ipynb)：


| 阶段 |组件名称 | 组件类型 |组件链接 |
|--------|--------|--------|---|
| 文档解析 | 文档矫正增强 (DocCropEnhance) | 基础能力组件 | [链接](./python/core/components/doc_crop_enhance/README.md) |
| 文档解析 | 文档格式转换 (DocFormatConverter) | 基础能力组件 | [链接](./python/core/components/doc_format_converter/README.md)|
| 文档解析 | 文档解析（DocParser）| 基础能力组件 | [链接](./python/core/components/doc_parser/README.md) |
| 文档解析 | 表格抽取组件（ExtractTableFromDoc）| 基础能力组件 | [链接](./python/core/components/extract_table/README.md) |
| 文档解析 | 通用文字识别-高精度版（GeneralOCR）| 基础能力组件 | [链接](./python/core/components/general_ocr/README.md) |
| 文档切片 | 文档切分（DocSplitter）| 基础能力组件 | [链接](./python/core/components/doc_splitter/README.md) |
| 切片向量化 | 向量计算（Embedding） | 基础能力组件 | [链接](./python/core/components/embeddings/README.md) |
| 索引构建及切片召回 | 向量检索-VectorDB（BaiduVectorDBRetriever） | 基础能力组件 | [链接](./python/core/components/retriever/baidu_vdb/README.md) |
| 索引构建及切片召回 | 向量检索-BES（BaiduElasticSearchRetriever） | 基础能力组件 | [链接](./python/core/components/retriever/bes/README.md) |
| 文档切片及答案生成 | 问答对挖掘（QAPairMining）| 高级能力组件 | [链接](./python/core/components/llms/qa_pair_mining/README.md) |
| 文档切片及答案生成 | 相似问生成（SimilarQuestion）| 高级能力组件 | [链接](./python/core/components/llms/similar_question/README.md) |
| 答案生成| 标签抽取（TagExtraction）| 高级能力组件 | [链接](./python/core/components/llms/tag_extraction/README.md) |
| 答案生成 | 复杂Query判定（IsComplexQuery）| 高级能力组件 | [链接](./python/core/components/llms/is_complex_query/README.md) |
| 答案生成 | 复杂Query分解（QueryDecomposition）| 高级能力组件 | [链接](./python/core/components/llms/query_decomposition/README.md) |
| 答案生成 | 多轮改写 (QueryRewrite)| 高级能力组件 | [链接](./python/core/components/llms/query_rewrite/README.md) |
| 答案生成 | 阅读理解问答（MRC）| 高级能力组件 | [链接](./python/core/components/llms/mrc/README.md) |
| 答案生成 | 幻觉检测（Hallucination Detection）| 高级能力组件 | [链接](./python/core/components/llms/hallucination_detection/README.md) |


> 功能预告：在AppBuiler-SDK 1.0.0版本中，AppBuilder-SDK可联动AppBuilder平台，自定义离线与在线处理的能力及Pipeline，构建更加灵活、可沉淀、可复用的产业级`RAG`应用，敬请期待



##  如何安装AppBuilder-SDK

#### 百度智能云千帆AppBuilder-SDK 最新版本 0.9.8 (2024-12-10)

百度智能云千帆AppBuilder-SDK 更新记录&最新特性请查阅我们的[版本说明](/docs/DevelopGuide/ChangeLog/changelog.md)

- `Python`版本安装，要求Python版本 >= `3.9`

```bash
python3 -m pip install --upgrade appbuilder-sdk
```
- `Java` 及 `Go` 版本安装，以及通过`Docker`镜像使用，请查阅[安装说明](/docs/QuickStart/StartFirstAINativeApplication/install.md)


## 快速开始你的AI原生应用开发之旅
> - 请在`>=3.9`的Python环境安装`appbuilder-sdk`后使用该端到端应用示例
> - 示例中提供了试用Token，访问和QPS受限，正式使用请替换为您的个人Token


### 1. 调用大模型
- 使用`Playground`组件可自由调用，您在百度智能云千帆大模型平台有权限的任何模型，并可自定义`prompt`模板 与 模型参数

#### 代码示例

```python
import appbuilder
import os

# 设置环境中的TOKEN，以下TOKEN为访问和QPS受限的试用TOKEN，正式使用请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# 定义prompt模板
template_str = "你扮演{role}, 请回答我的问题。\n\n问题：{question}。\n\n回答："

# 定义输入，调用playground组件
input = appbuilder.Message({"role": "java工程师", "question": "请简要回答java语言的内存回收机制是什么，要求100字以内"})

playground = appbuilder.Playground(prompt_template=template_str, model="Qianfan-Agent-Speed-8K")

# 以打字机的方式，流式展示大模型回答内容
output = playground(input, stream=True, temperature=1e-10)
for stream_message in output.content:
    print(stream_message)
    
# 流式输出结束后，可再次打印完整的大模型对话结果，除回答内容外，还包括token的用量情况
print(output.model_dump_json(indent=4))

```
#### 回答展示

```shell
Java语言的
内存回收机制是通过垃圾回收器（Garbage Collector）来实现的。
垃圾回收器会自动检测不再使用的对象，并释放其占用的内存空间，从而确保系统的内存不会被耗尽。
Java提供了多种垃圾回收器，如串行回收器、并行回收器、CMS回收器和G1回收器等，以满足不同场景下的性能需求
。

{
    "content": "Java语言的内存回收机制是通过垃圾回收器（Garbage Collector）来实现的。垃圾回收器会自动检测不再使用的对象，并释放其占用的内存空间，从而确保系统的内存不会被耗尽。Java提供了多种垃圾回收器，如串行回收器、并行回收器、CMS回收器和G1回收器等，以满足不同场景下的性能需求。",
    "name": "msg",
    "mtype": "dict",
    "id": "2bbee989-40e3-45e4-9802-e144cdc829a9",
    "extra": {},
    "token_usage": {
        "prompt_tokens": 35,
        "completion_tokens": 70,
        "total_tokens": 105
    }
}
```

### 2. 调用能力组件
- SDK提供了40+个源于百度生态的优质组件，列表可见[组件列表](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz#3%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1), 调用前需要申领[免费试用额度](https://console.bce.baidu.com/ai/#/ai/apaas/overview/resource/getFree)
- 示例中的组件为`RAG with Baidu Search增强版`, 结合百度搜索的搜索引擎技术和ERNIE模型的语义理解能力，可以更准确地理解用户的搜索意图，并提供与搜索查询相关性更高的搜索结果

#### 代码示例
```python
import appbuilder
import os

# 设置环境中的TOKEN，以下TOKEN为访问和QPS受限的试用TOKEN，正式使用请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

rag_with_baidu_search_pro = appbuilder.RagWithBaiduSearchPro(model="ERNIE-Lite-AppBuilder-8K")

input = appbuilder.Message("9.11和9.8哪个大")
result = rag_with_baidu_search_pro.run(
    message=input,
    instruction=appbuilder.Message("你是专业知识助手"))

# 输出运行结果
print(result.model_dump_json(indent=4))
```

#### 回答展示
```shell
{
    "content": "9.11小于9.8。在比较两个小数的大小时，需要逐位比较它们的数值，包括整数部分和小数部分。对于9.11和9.8，整数部分都是9，所以需要在小数部分进行比较。小数点后的第一位是1和8，显然1小于8，所以9.11小于9.8。",
    "name": "msg",
    "mtype": "dict",
    "id": "eb31b7de-dd6a-485f-adb9-1f7921a6f4bf",
    "extra": {
        "search_baidu": [
            {
                "content": "大模型‘智商’受质疑:9.11 vs 9...",
                "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/souhu.ico",
                "url": "https://m.sohu.com/a/793754123_121924584/",
                "ref_id": "2",
                "site_name": "搜狐网",
                "title": "大模型‘智商’受质疑:9.11 vs 9.8的比较揭示AI理解能力的..."
            },
            {
                "content": "究竟|9.11比9.8大?大模型们为何会...",
                "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/tencent.svg.png",
                "url": "https://new.qq.com/rain/a/20240717A07JLV00",
                "ref_id": "4",
                "site_name": "腾讯网",
                "title": "究竟|9.11比9.8大?大模型们为何会在小学数学题上集体..."
            },
            ...
        ]
    },
    "token_usage": {
        "completion_tokens": 77,
        "prompt_tokens": 2008,
        "total_tokens": 2085
    }
}
```


### 3. 调用AI原生应用
- 示例中的应用为：[说唱导师](https://appbuilder.baidu.com/s/3qfjXy7k)，点击该连接在网页端试用

#### 代码示例

```python
import appbuilder
import os

# 设置环境中的TOKEN，以下TOKEN为访问和QPS受限的试用TOKEN，正式使用请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# 从AppBuilder网页获取并传入应用ID，以下为说唱导师应用ID
app_id = "4678492a-5864-472e-810a-654538d3503c"

app_builder_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_builder_client.create_conversation()

answer = app_builder_client.run(conversation_id, "以“上班狼狈却又追逐梦想“为主题进行一首说唱创作，保持押韵, 控制在200字以内")
print(answer.content.answer)
```

#### 回答展示
```shell
好的，我们来以“上班狼狈却又追逐梦想”为主题，进行一段简短的说唱创作。这里是一个简单的示例，你可以根据自己的感觉进行调整：

Intro:
朝九晚五，生活重压，
狼狈上班，却心怀梦想，
每一天，都是新的挑战，
为了那未来，我奋发向前。

Verse 1:
穿上西装，打好领带，
步入人群，去追逐名利，
虽然狼狈，却不曾言败，
因为心中，有梦想在激励。

Hook:
上班狼狈，却不曾放弃，
追逐梦想，是我心中的火炬，
照亮前路，指引我前行，
无论多难，我都要坚持到底。

这首小曲儿以“上班狼狈却又追逐梦想”为主题，通过押韵的方式表达了上班族虽然生活艰辛，但依然怀揣梦想，勇往直前的精神。希望你喜欢！
```

#### 更多示例

- 更多AI原生应用示例，请浏览[应用广场](https://console.bce.baidu.com/ai_apaas/appCenter)
- 更多代码Cookbook，请浏览 [Cookbooks](./cookbooks/README.md)，我们有以下cookbook推荐您优先阅读：

| 应用类型 |应用链接 | 推荐理由 |
|--|--|--|
| 基础能力组件 | [通用文字识别](/cookbooks/components/general_ocr.ipynb) | 体验百度AI开放平台提供的通用文字识别-高精度版的精准识别结果 |
| 基础能力组件 | [基础组件服务化](/cookbooks/components/agent_runtime.ipynb) | 基础组件可通过flask实现服务化部署 或 通过chainlit实现可交互的前端部署，集成到您的系统中 |
| 流程编排 |  [Assistant SDK](/cookbooks/pipeline/assistant_function_call.ipynb) | 学习如何纯代码态搭建一个Agent应用，并实现自定义工作流程及FunctionCall |
| 端到端应用 |  [AppBuilder Client SDK](/cookbooks/agent_builder.ipynb) | 使用AppBuilder网页端创建并发布一个Agent应用后，通过AppBuilderClient SDK集成到你的系统中 |
| 端到端应用 |  [Agent应用-工作流Agent](/cookbooks/end2end_application/agent/chatflow.ipynb) | 使用AppBuilder网页端创建并发布一个工作流Agent应用后，通过AppBuilderClient SDK集成到你的系统中 |
| 端到端应用 |  [通过AppBuilder-ToolCall功能实现端云组件联动的Agent](/cookbooks/end2end_application/agent/tool_call.ipynb) | 学习Agent、FunctionCall的知识，并构造调用本地组件的Agent |
| 端到端应用 |  [简历筛选小助手](/cookbooks/end2end_application/rag/rag.ipynb) | 通过对本地简历库的简历进行解析、切片、创建索引，实现基于JD进行简历筛选，并对筛选的Top1简历进行总结 |
| 端到端应用 |  [企业级问答系统](/cookbooks/end2end_application/rag/qa_system_2_dialogue.ipynb) | 学习如何通过SDK与网页平台搭配，实现离线知识库生产与在线问答 |
| 进阶应用 |  [使用appbuilder_bce_deploy部署公有云服务](/cookbooks/advanced_application/cloud_deploy.ipynb) | 一键将自己的服务部署到百度智能云，部署后可以自动生成公网ip，联动工作流的API节点 |
| 进阶应用 |  [使用appbuilder_trace_server实现对使用状态的跟踪](/cookbooks/appbuilder_trace/trace.ipynb) | 使用Appbuilder-SDK Trace功能实现对组件、应用调用情况的追踪|


## 百度智能云千帆AppBuilder-SDK 能力全景图
<div align="center">
<img src='docs/image/structure-cn.png' alt='wechat' width='800' >
</div>


## 用户文档

## Github 文档
- [首页](https://github.com/baidubce/app-builder/blob/master/docs/README.md)
    - 快速上手: 
        - 开始你的第一个AI原生应用: 
            - [安装](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/StartFirstAINativeApplication/install.md)
            - [快速开始](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/StartFirstAINativeApplication/README.md)
        - 产业实践应用范例: 
            - [SDK使用示例](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/ExamplesOfIndustrialPracticeApplications/README.md)
        - [SDK当前支持的编程语言](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/CurrentlySupportedProgrammingLanguages/README.md)
    - 基础:
        - 模型:
            - [获取模型列表](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Model/get_model_list.md)
        - [组件](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Components/Components.md)
        - 监控:
            - [TRACE基础功能](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Trace/basic.md)
            - [TRACE拓展功能](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Trace/phoenix_method.md)
        - 部署:
            - [交互式前端部署](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/chainlit_deploy.md)
            - [公有云部署](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/cloud.md)
            - [API 访问](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/flask_deploy.md)
            - [UserSession](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/usersession.md)
        - 平台:
            - 应用:
                - [AppBuilderClient组件](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/Application/appbuilder_client.md)
                - [获取AppBuilder已发布的应用列表](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/Application/get_app_list.md)
            - 知识库:
                - [知识库组件](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/KnowledgeBase/knowledgebase.md)
            - 自定义组件:
                - [基础能力组件](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/CustomComponents/components.md)
    - 应用:
        - Agent:
            - [基础知识](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/BasicKnowledge/agent.md)
            - [使用官方组件](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/UseOfficialComponents/use_official_components.md)
            - [ToolCall](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/ToolCall/tool_call.md)
            - [ToolChoice](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/ToolChoice/tool_choice.md)
            - [使用异步和流式加速客户端调用](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
        - RAG:
            - [基础知识](https://github.com/baidubce/app-builder/blob/master/docs/Application/RAG/BasicKnowledge/rag.md)
            - [知识库管理](https://github.com/baidubce/app-builder/blob/master/docs/Application/RAG/DatasetManage/dataset_manage.md)
            - [Reference信息处理](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
        - Workflow:
            - [基础知识](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
            - [从零使用Workflow组装一个RAG应用](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
            - [从零使用Workflow组装一个Agent应用](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
    - 开发者指南:
        - [如何贡献代码](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/HowToContributeCode/README.md)
        - [二次开发](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/AdvancedDevelopment/README.md)
        - [版本升级日志](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/ChangeLog/changelog.md)
        - [错误信息](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/ErrorMessage/error_message.md)
        - [环境参数](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/EnvironmentalParameters/env.md)


## 开源社区与活动
<div align="center">
<h3>百度智能云千帆AppBuilder-SDK微信交流群</h3>
<img src='docs/image/wechat_group.png' alt='wechat' width='200' >
</div>

- [Github Issue](https://github.com/baidubce/app-builder/issues):  提交安装/使用问题、报告bug、建议新特性、沟通开发计划等

- [百度智能云千帆社区](https://cloud.baidu.com/qianfandev)：
    - [千帆杯新手训练营 - 多类型主题练习赛](https://cloud.baidu.com/qianfandev/aimatch)
    - [千帆杯AI原生应用创意挑战赛 - 教育生态行业赛](https://cloud.baidu.com/qianfandev/topic/269711)
    - [千帆杯AI原生应用创意挑战赛 - 效率工具常规赛](https://cloud.baidu.com/qianfandev/topic/269599)



## License

AppBuilder-SDK遵循Apache-2.0开源协议。

