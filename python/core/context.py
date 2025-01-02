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
import uuid
import logging
from typing import Optional
from contextvars import ContextVar


_LOCAL_KEY = 'LOCAL-'

class SessionContext:
    """
    维护当前 Session 的上下文信息。
    """
    id: str
    session_id: str
    request_id: str
    user_id: Optional[str]
    session_vars_dict: dict
    
    def __init__(self, id: str, session_id: str, request_id: str, user_id: Optional[str] = None):
        self.id = id
        self.session_id = session_id
        self.request_id = request_id
        self.user_id = user_id
        self.session_vars_dict = {}


context_var: ContextVar[SessionContext] = ContextVar("appbuilder_session")


def init_context(
    session_id: str,
    request_id: str,
    user_id: Optional[str] = None,
) -> SessionContext:
    """
    初始化 Session 的上下文信息。
    """
    ctx = SessionContext(
        id=str(uuid.uuid4()),
        session_id=session_id,
        request_id=request_id,
        user_id=user_id,
    )
    context_var.set(ctx)
    return ctx


def get_context() -> SessionContext:
    """
    获取当前 Session 的上下文信息。
    """
    try:
        return context_var.get()
    except LookupError:
        session_id = _LOCAL_KEY + str(uuid.uuid4())[:-len(_LOCAL_KEY)]
        request_id = _LOCAL_KEY + str(uuid.uuid4())[:-len(_LOCAL_KEY)]
        logging.debug(
            "Unable to find the context. You need to use UserSession "
            "in FlaskRuntime.serve or ChainlitRuntime.chainlit_component. "
            f"Generate session_id({session_id}) and request_id({request_id}) here for local debugging.")
        ctx = init_context(session_id=session_id, request_id=request_id)
        return ctx