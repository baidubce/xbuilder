# `UserSession`类

## 简介

会话数据管理工具，实例化后将是一个全局变量。提供保存对话数据与获取历史数据的方法。

## 应用场景

**必须**在 FlaskRuntime和ChainlitRuntime 启动的服务中使用。

## Python基本用法

### 1、实例化`UserSession().__init__ -> UserSession`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| user_session_config | sqlalchemy.engine.URL、str、None | Session 输出存储配置字符串。默认使用 sqlite:///user_session.db | "正确的存储配置字符串" |

#### 方法功能

初始化 UserSession

#### 示例代码

```python
user_session = UserSession()
```

### 2、获取同个 session 中名为 key 的历史变量`UserSession().get_history(self, key: str, limit: int=10) -> List[Message]:`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| key | String | 历史变量 | "answer" |
| limit | int | 最近 limit 条 Message 数据 | 10 |

#### 方法功能

获取同个 session 中名为 key 的历史变量。在非服务化版本中从内存获取。在服务化版本中，将从数据库获取。

#### 方法返回值

`List[Message]` 

衍生类`Message`定义如下:

```python
class Message(BaseModel, Generic[_T], extra=Extra.allow):
    content: Optional[_T] = {}
    name: Optional[str] = "msg"
    mtype: Optional[str] = "dict"
    id: Optional[str] = str(uuid.uuid4())
```

#### 示例代码

```python
history_queries = user_session.get_history("query", limit=1)
```

### 3、将 message_dict 中的变量保存到 session 中`UserSession().append(self, message_dict: Dict[str, Message]) -> None`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| message_dict | Dict | 包含 Message 的字典，其中键为字符串类型，值为 Message 类型 | {"query": message} |

#### 方法功能

将 message_dict 中的变量保存到 session 中。在非服务化版本中使用内存存储。在服务化版本中，将使用数据库进行存储。

#### 示例代码

```python
user_session.append({
            "query": message,
            "answer": answer,
        }) 
```

### 4、UserSession结合FlaskRuntime/ChainlitRuntime使用以及user_session.db文件读取

- [UserSession结合FlaskRuntime/ChainlitRuntime使用以及user_session.db文件读取](https://github.com/baidubce/app-builder/blob/master/cookbooks/components/user_session.ipynb)




