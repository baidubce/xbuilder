# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
import unittest
import appbuilder
import asyncio
from unittest.mock import patch, AsyncMock
from appbuilder.core._session import AsyncInnerSession

class TestCoreSession(unittest.TestCase):


    @patch("appbuilder.core._session.AsyncInnerSession.put")
    def test_async_session_get(self, mock_put):
        async def demo():
            return {"status": 200}

        async def get_demo():
            mock_put.return_value.__aenter__.return_value.json = await demo()
            session = AsyncInnerSession()
            await session.get("http://www.baidu.com")
            session.put("https://example.com")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_demo())

if __name__ == "__main__":
    unittest.main()
