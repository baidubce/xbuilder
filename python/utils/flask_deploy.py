import uuid
import json
import copy
from typing import Optional, Union, Any

import appbuilder
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core.user_session import UserSession
from appbuilder.utils.logger_util import logger
from appbuilder.core.context import init_context


# 流式场景首包超时时，最大重试次数
MAX_RETRY_COUNT = 3

class FlaskRuntime(object):
    r"""
    FlaskRuntime 是对应用调用的服务化封装, 开发者不是必须要用 ChainlitRuntime 才能运行自己的组件服务。
    FlaskRuntime提供chat直接对话接口; 也支持使用 Gunicorn 这样的 WSGI 服务器来运行服务, 提供API部署方式。


    Examples:
    # 直接调用chat接口进行对话
    .. code-block:: python

        import os
        import sys
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

    # 启动一个flask服务, 使用curl调用flask服务
    .. code-block:: python

        import os
        import sys
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

    .. code-block:: shell
        
        curl --location 'http://0.0.0.0:8091/chat' \
            --header 'Content-Type: application/json' \
            --header 'X-Appbuilder-Token: ...' \
            --data '{
                "message": "你是谁",
                "stream": false
            }'

    Session 数据管理 : 除去上述简单应用外，还支持 Session 数据管理，下面是一个例子

    .. code-block:: python

        import os
        import sys
        from appbuilder.core.component import Component
        from appbuilder import (
            FlaskRuntime, UserSession, Message, QueryRewrite, Playground,
        )

        os.environ["APPBUILDER_TOKEN"] = '...'

        class PlaygroundWithHistory(Component):
            def __init__(self):
                super().__init__()
                self.query_rewrite = QueryRewrite(model="Qianfan-Agent-Speed-8k")
                self.play = Playground(
                    prompt_template="{query}",
                    model="eb-4"
                )

            def run(self, message: Message, stream: bool=False):
                user_session = UserSession()
                # 获取 Session 历史数据
                history_queries = user_session.get_history("query", limit=1)
                history_answers = user_session.get_history("answer", limit=1)

                if history_queries and history_answers:
                    history = []
                    for query, answer in zip(history_queries, history_answers):
                        history.extend([query.content, answer.content])
                    logging.info(f"history: {history}")
                    message = self.query_rewrite(
                        Message(history + [message.content]), rewrite_type="带机器人回复")
                logging.info(f"message: {message}") 
                answer = self.play.run(message, stream)
                # 保存本轮数据
                user_session.append({
                    "query": message,
                    "answer": answer,
                }) 
                return answer

        agent = FlaskRuntime(component=PlaygroundWithHistory())
        agent.chainlit_component(port=8091)

    Session 信息查看 : 查看本地user_session.db数据库内部信息，下面是一个例子

    .. code-block:: python

        import sqlite3  
        import json  
        
        # 连接到 SQLite 数据库  
        # 如果文件不存在，会自动在当前目录创建:  
        user_session_path = 'your_user_session.db地址'  
        conn = sqlite3.connect(user_session_path)  
        cursor = conn.cursor()  
        
        # 执行一条 SQL 语句，列出所有表  
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
        print(cursor.fetchall())  

        # 查询appbuilder_session_messages表的列信息  
        cursor.execute("PRAGMA table_info(appbuilder_session_messages);")  
        columns_info = cursor.fetchall()  

        column_names = [info[1] for info in columns_info]  # info[1]是列名的位置  
        for column_name in column_names:  
            print(column_name)   

        # 查询特定表中的数据  
        cursor.execute("SELECT message_value FROM appbuilder_session_messages;")  
        for row in cursor.fetchall():  
            print(json.loads(row[0]))
        
        # 关闭 Connection:  
        conn.close()
    """
    def __init__(self, 
            component: Component,
            user_session_config: Optional[Union[Any, str]] = None,
            user_session: Optional[UserSession] = None
            ):
        """init

        Args:
            component (Component): 可运行的 Component, 需要实现 run(message, stream, args) 方法  
            user_session_config (sqlalchemy.engine.URL|str|None): Session 输出存储配置字符串。默认使用 sqlite:///user_session.db
                遵循 sqlalchemy 后端定义，参考文档：https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
            user_session (UserSession): 用户会话管理器，如果不指定则自动生成一个默认的 UserSession
        """
        try:
            from flask import Flask

        except ImportError:
            raise ImportError("Flask module is not installed. Please install it using 'pip install "
                                "flask~=2.3.2 flask-restful==0.3.9'.")
        self.app = Flask(__name__)
        self.app.json.ensure_ascii = False
        self.component = component
        if user_session is None:
            if user_session_config is None:
                self.user_session = UserSession()
                logger.info("init user_session with default UserSession")
            else:
                self.user_session = UserSession(user_session_config)
                logger.info("init user_session with user_session_config")
        else:
            self.user_session = user_session

    def chat(self, message: Message, stream: bool = False, **args) -> Message:
        """
        执行一次对话

        Args:
            message (Message): 该次对话用户输入的 Message
            stream (bool): 是否流式请求
            **args: 其他参数，会被透传到 component

        Returns:
            Message(Message): 返回的 Message
        """
        return self.component.run(message=message, stream=stream, **args)
        
    def create_flask_app(self, url_rule="/chat"):
        """ 
        创建 Flask 应用，主要用于 Gunicorn 这样的 WSGI 服务器来运行服务。

        Args:
            None

        Returns:
            Flask
        """
        try:
            from flask import request, Response
            from werkzeug.exceptions import BadRequest
            from flask import stream_with_context

        except ImportError:
            raise ImportError("Flask module is not installed. Please install it using 'pip install "
                                "flask~=2.3.2 flask-restful==0.3.9'.")
        @self.app.errorhandler(BadRequest)
        def handle_bad_request(e):
            return {"code": 400, "message": f'{e}', "result": None}, 400

        @self.app.errorhandler(Exception)
        def handle_bad_request(e):
            if hasattr(e, "code"):
                return {"code": e.code, "message": str(e), "result": None}, 200
            else:
                return {"code": 500, "message": "Internal Server Error", "result": None}, 200

        def warp():
            """
            根据component的lazy_certification属性处理请求。
            
            Args:
                无参数。
            
            Returns:
                如果stream为True，则返回流式响应（Content-Type为text/event-stream）。
                如果stream为False，则返回包含处理结果的字典。
            
            Raises:
                BadRequest: 当请求头中缺少必要的X-Appbuilder-Authorization时抛出。
                BadRequest: 当请求体中缺少必要的message字段时抛出。
                BadRequest: 当请求体中session_id字段不是字符串类型时抛出。
                BadRequest: 当请求体中stream字段不是布尔类型时抛出。
            
            """
            # 根据component是否lazy_certification，分成两种情况：
            # 1. lazy_certification为True，初始化时未被认证，每次请求都需要带入AppbuilderToken
            # 2. lazy_certification为False，初始化时已经认证，请求时不需要带入AppbuilderToken，并且带入也无效
            if self.component.lazy_certification:
                app_builder_token = None
                for key in ["X-Appbuilder-Token", "X-Appbuilder-Authorization"]:
                    if key in request.headers:
                        app_builder_token = request.headers[key]
                        break
                if not app_builder_token:
                    raise BadRequest(
                        "X-Appbuilder-Authorization is required in Headers")
                try:
                    self.component.set_secret_key_and_gateway(
                        secret_key=app_builder_token)
                except appbuilder.core._exception.BaseRPCException as e:
                    logger.error(f"failed to verify. err={e}", exc_info=True)
                    raise BadRequest("X-Appbuilder-Authorization invalid")
                except Exception as e:
                    logger.error(f"failed to verify. err={e}", exc_info=True)
                    raise e
            else:
                pass

            data = request.get_json()
            if "message" not in data:
                raise BadRequest("message is required")
            message = Message(data.pop('message'))
            if "session_id" not in data:
                session_id = str(uuid.uuid4())
            else:
                session_id = data.pop("session_id")
                if not isinstance(session_id, str):
                    raise BadRequest("session_id must be str type")
            if "stream" not in data:
                stream = False
            else:
                stream = data.pop("stream")
                if not isinstance(stream, bool):
                    raise BadRequest("stream must be bool type")
            request_id = request.headers.get("X-Appbuilder-Request-Id", str(uuid.uuid4()))
            user_id = request.headers.get("X-Appbuilder-User-Id", None)

            init_context(session_id=session_id, request_id=request_id, user_id=user_id)
            logger.info(
                f"request_id={request_id}, session_id={session_id}] message={message},"
                f" stream={stream}, data={data}, start run...")

            def gen_sse_resp():
                with self.app.app_context():
                    received_first_packet = False
                    retry_count = 0
                    while retry_count < MAX_RETRY_COUNT:
                        try:
                            answer = self.chat(message, stream, **data)
                        except Exception as e:  # 调用chat方法报错，直接返回
                            code = 500 if not hasattr(e, "code") else e.code
                            err_resp = {"code": code, "message": "InternalServerError", "result": None}
                            logger.error(
                                f"request_id={request_id}, session_id={session_id}, err={e}, execute self.chat failed", exc_info=True)
                            yield "data: " + json.dumps(err_resp, ensure_ascii=False) +  "\n\n"
                            return
                        else:  # 调用chat方法成功，开始生成流式事件
                            content_iterator = iter(answer.content)
                            answer.content = None
                            result = None
                            try:
                                for sub_content in content_iterator:
                                    result = copy.deepcopy(answer)
                                    result.content = sub_content
                                    yield "data: " + json.dumps({
                                        "code": 0, "message": "",
                                        "result": {
                                            "session_id": session_id,
                                            "is_completion": False,
                                            "answer_message": json.loads(result.json(exclude_none=True))
                                        }
                                    }, ensure_ascii=False) + "\n\n"
                                    received_first_packet = True
                            except Exception as e:
                                retry_count += 1
                                logger.error(
                                    f"[request_id={request_id}, session_id={session_id}] err={e}, "
                                    f"retry_count={retry_count}", exc_info=True)
                                # 如果未收到首包且重试次数小于最大重试次数，则尝试重新执行一次chat方法
                                if not received_first_packet and retry_count < MAX_RETRY_COUNT:
                                    continue
                                else:  # 其它情况返回
                                    logger.error(
                                        f"[request_id={request_id}, session_id={session_id}] err={e}, "
                                        f"retry_count={retry_count}, received_first_packet={received_first_packet}"
                                        , exc_info=True)
                                    code = 500 if not hasattr(e, "code") else e.code
                                    err_resp = {"code": code, "message": "InternalServerError", "result": None}
                                    yield "data: " + json.dumps(err_resp, ensure_ascii=False) + "\n\n"
                                    return
                            result.content = ""
                            yield "data: " + json.dumps({
                                "code": 0, "message": "",
                                "result": {
                                    "session_id": session_id,
                                    "is_completion": True,
                                    "answer_message": json.loads(result.json(exclude_none=True))
                                }
                            }, ensure_ascii=False) + "\n\n"
                            logger.info(
                                f"request_id={request_id}, session_id={session_id}]"
                                f"retry_count={retry_count}, success response", exc_info=True)
                            self.user_session._post_append()
                            return  # 正常返回

            if stream:  # 流式
                return Response(stream_with_context(gen_sse_resp()), 200,
                        {'Content-Type': 'text/event-stream; charset=utf-8'})
            if not stream:  # 非流式
                try:
                    answer = self.chat(message, stream, **data)
                    blocking_result = json.loads(copy.deepcopy(answer).json(exclude_none=True))
                    logger.debug(f"[request_id={request_id}, session_id={session_id}] blocking_result={blocking_result}")
                    self.user_session._post_append()
                    return {
                        "code": 0, "message": "",
                        "result": {"session_id": session_id, "answer_message": blocking_result}
                    }
                except Exception as e:
                    logger.error(
                        f"[request_id={request_id}, session_id={session_id}] err={e}", exc_info=True)
                    code = 500 if not hasattr(e, "code") else e.code
                    return {"code": code, "message": "InternalServerError", "result": None}

        self.app.add_url_rule(url_rule, 'chat', warp, methods=['POST'])
        return self.app

    def serve(self, host='0.0.0.0', debug=True, port=8092, url_rule="/chat"):
        """
        将 component 服务化，提供 Flask http API 接口
        
        Args:
            host (str): 服务运行的host地址，默认为'0.0.0.0'
            debug (bool): 是否开启debug模式，默认为True
            port (int): 服务运行的端口号，默认为8092
            url_rule (str): 服务的URL规则，默认为"/chat"
        
        Returns:
            None
        """
        self.app = self.create_flask_app(url_rule=url_rule)
        self.app.run(host=host, debug=debug, port=port)