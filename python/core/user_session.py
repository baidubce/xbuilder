# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime
import uuid
import json
import os
import logging
from typing import Union, List, Dict, Optional, Any

from appbuilder.core.message import Message
from appbuilder.core.context import get_context, _LOCAL_KEY


def lazy_import_sqlalchemy():
    try:
        import sqlalchemy
        from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Boolean
        from sqlalchemy.orm import declarative_base, sessionmaker
    except ImportError as e:
        raise ImportError("Please install SQLAlchemy first: python3 -m pip install SQLAlchemy==2.0.31")

class UserSession(object):
    """
    会话数据管理工具，实例化后将是一个全局变量。
    提供保存对话数据与获取历史数据的方法，**必须**在 FlaskRuntime和ChainlitRuntime 启动的服务中使用。
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        """
        lazy_import_sqlalchemy()

        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, user_session_config: Optional[Union[Any, str]] = None):
        """
        初始化 UserSession
        
        Args:
            user_session_config (str|None): Session 配置字符串，遵循 sqlalchemy 后端定义，参考文档
              https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
        
        Returns:
            None
        """
        if self._initialized:
            return
        self._initialized = True

        import sqlalchemy
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.orm import declarative_base
        from sqlalchemy import create_engine
        from appbuilder.core. session_message import get_db_base_class
        
        _db = get_db_base_class()

        if user_session_config is None:
            user_session_config = "sqlite:///user_session.db"
        if not isinstance(user_session_config, (sqlalchemy.engine.URL, str)):
            raise ValueError("user_session_config must be sqlalchemy.URL or str")
        logging.info(f"create user_session by {user_session_config}")
        engine = create_engine(user_session_config)
        _db.metadata.create_all(engine) # 创建表
        Session = sessionmaker(engine)
        self._db_session = Session()
    

    def get_history(self, key: str, limit: int=10) -> List[Message]:
        """
        获取同个 session 中名为 key 的历史变量。
        在非服务化版本中从内存获取。在服务化版本中，将从数据库获取。
        
        Args:
            key (str): 变量名
            limit (int): 最近 limit 条 Message 数据
        
        Returns:
            List[Message]
        """
        from appbuilder.core.session_message import SessionMessage
        ctx = get_context()
        if ctx.session_id.startswith(_LOCAL_KEY):
            # 非服务化版本使用内存存储
            if key not in ctx.session_vars_dict:
                return []
            session_messages = ctx.session_vars_dict[key][-limit:]
            return session_messages
        else:
            # 服务化版本使用数据库存储
            session_messages = self._db_session.query(SessionMessage).filter(
                SessionMessage.session_id == ctx.session_id,
                SessionMessage.message_key == key,
                SessionMessage.deleted == False).order_by(
                    SessionMessage.updated_at.desc()).limit(limit).all()
            return [Message(content=item.message_value) for item in session_messages][::-1]

    def append(self, message_dict: Dict[str, Message]) -> None:
        """
        将 message_dict 中的变量保存到 session 中。
        在非服务化版本中使用内存存储。在服务化版本中，将使用数据库进行存储。

        Args:
            message_dict (Dict[str, Message]): 包含 Message 的字典，其中键为字符串类型，值为 Message 类型。

        Returns:
            None
        """
        ctx = get_context()
        if ctx.session_id.startswith(_LOCAL_KEY):
            # 非服务化版本使用内存存储
            for key, message in message_dict.items():
                if not isinstance(message, Message):
                    raise ValueError("session format error, message must be Message type")
                if key not in ctx.session_vars_dict:
                    ctx.session_vars_dict[key] = []
                ctx.session_vars_dict[key].append(message)
        else:
            # 服务化版本使用数据库存储
            for key, message in message_dict.items():
                if not isinstance(message, Message):
                    raise ValueError("session format error, message must be Message type")
                if key in ctx.session_vars_dict:
                    raise KeyError(
                        f"session format error, key {key} has already been appended"
                    )
                ctx.session_vars_dict[key] = message

    def _post_append(self) -> None:
        """
        后置保存。流式数据不能直接保存到数据库，需要通过该方法后置保存。
        
        Args:
            None
        
        Returns:
            None
        """
        from appbuilder.core.session_message import SessionMessage
        ctx = get_context()
        try:
            for key, message_value in ctx.session_vars_dict.items():
                message = SessionMessage(
                    session_id=ctx.session_id,
                    request_id=ctx.request_id,
                    message_key=key,
                    message_value=json.loads(message_value.json(exclude_none=True)),
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now())
                self._db_session.add(message)
                self._db_session.commit()
            ctx.session_vars_dict = {}
        except Exception as e:
            logging.error(e)
            self._db_session.rollback()
            raise e
