# `FlaskRuntime`类

## 简介

FlaskRuntime 是对组件调用的服务化封装，开发者不是必须要用 FlaskRuntime 才能运行自己的组件服务。但 FlaskRuntime 可以快速帮助开发者服务化组件服务，并且提供API、对话框等部署方式。此外，结合 Component 和 Message 自带的运行和调试接口，可以方便开发者快速获得一个调试 Agent 的服务。


## Python基本用法

### 1、实例化`FlaskRuntime() -> FlaskRuntime`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| component | Component | 可运行的 Component,需要实现 run(message, stream, **args) 方法  | "正确的component组件或client" |
| user_session_config | sqlalchemy.engine.URL、str、None | Session 输出存储配置字符串。默认使用 sqlite:///user_session.db | "正确的存储配置字符串" |
| user_session_config | sqlalchemy.engine.URL\|Str\|None | 否 | 会话 Session 数据存储的数据库配置，遵循 sqlalchemy 后端定义，可参考[文档](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)。默认使用 sqlite:///user_session.db，即本地的 SQLite 存储 | "sqlite:///user_session.db" |
｜user_session| UserSession | 否 | 用户会话管理器，如果不指定则自动生成一个默认的 UserSession | UserSession(user_session_config) |

#### 方法功能

返回一个调试 Agent 的服务

#### 示例代码

```python
import os
import appbuilder
from appbuilder.utils.flask_deploy import FlaskRuntime

os.environ["APPBUILDER_TOKEN"] = '...'
component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
agent = FlaskRuntime(component=component)
```

### 2、运行Agent服务`FlaskRuntime.chat(message: Message, stream: bool = False, **args) -> Message`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| message | Message | 该次对话用户输入的 Message | "正确的Message" |
| stream | bool | 是否使用流式请求。默认为 False | False |

#### 方法功能

运行一个 Agent 服务，执行一次对话

#### 示例代码

```python
import os
import appbuilder
from appbuilder.utils.flask_deploy import FlaskRuntime

os.environ["APPBUILDER_TOKEN"] = '...'
component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
agent = FlaskRuntime(component=component)
message = appbuilder.Message({"query": "你好"})
print(agent.chat(message, stream=False))
```

### 3、提供 Flask http API 接口`FlaskRuntime.serve(self, host='0.0.0.0', debug=True, port=8092, url_rule="/chat"`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| host | String | 服务主机地址，默认为 '0.0.0.0' | '0.0.0.0' |
| debug | bool | 是否是调试模式，默认为 True | False |
| port | int | 服务端口号，默认为 8092 | 8092 |
| url_rule | String | Flask 路由规则，默认为 '/chat' | '/chat' |

#### 方法功能

将 component 服务化，提供 Flask http API 接口

#### 示例代码

```python
import os
import appbuilder
from appbuilder.utils.flask_deploy import FlaskRuntime

os.environ["APPBUILDER_TOKEN"] = '...'
component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
user_session_config = "sqlite:///foo.db"
agent = FlaskRuntime(
    component=component, user_session_config=user_session_config)
agent.serve(debug=False, port=8091)
```