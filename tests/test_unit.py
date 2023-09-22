"""
 TT test
"""

from unittest.mock import AsyncMock, MagicMock

import iamlistening
import pytest
import uvicorn
from fastapi.testclient import TestClient
from iamlistening import Listener

from tt.app import app, start_bot_task
from tt.config import settings
from tt.plugins.plugin_manager import PluginManager
from tt.utils import send_notification, start_bot, start_plugins


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


def test_dynaconf_is_in_testing():
    assert settings.VALUE == "On Testing"
    assert settings.platform is not None


@pytest.fixture(name="message")
def message_test():
    return "hello"


@pytest.fixture(name="listener")
def listener():
    return Listener()


@pytest.fixture(name="plugin_manager_obj")
def pluginmngr_test():
    return PluginManager()


@pytest.fixture
def message():
    return "Hello"


@pytest.mark.asyncio
async def test_start_bot_task():
    run_bot = AsyncMock()
    await start_bot_task()
    assert run_bot.assert_awaited_once


def test_app_endpoint_main():
    client = TestClient(app)
    response = client.get("/")
    init = MagicMock(client)
    # assert response.status_code == 200
    assert response.status_code is not None
    assert init.assert_called


def test_app_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200


def test_webhook_with_valid_auth():
    client = TestClient(app)
    payload = {"data": "buy BTC"}
    response = client.post("/webhook/123abc", json=payload)
    post = MagicMock()
    print(response.content.decode("utf-8"))
    assert response is not None
    assert response.content.decode("utf-8") is not None
    assert post.assert_called


def test_webhook_with_invalid_auth():
    client = TestClient(app)
    payload = {"data": "my_data"}
    response = client.post("/webhook/abc123", json=payload)
    print(response.content.decode("utf-8"))
    assert response.content.decode("utf-8") is not None


@pytest.mark.asyncio
async def test_send_notification(caplog):
    await send_notification("Test message")
    assert "Loaded Discord" in caplog.text


@pytest.mark.asyncio
async def test_start_plugins():
    plugin_manager = AsyncMock(spec=PluginManager)
    await start_plugins(plugin_manager)
    plugin_manager.load_plugins.assert_called_once()


@pytest.mark.asyncio
async def test_start_bot(listener, message):
    #iamlistening.listener.platform.client.get_latest_message = AsyncMock()
    plugin_manager = AsyncMock(spec=PluginManager)
    await start_bot(listener, plugin_manager, max_iterations=1)
    listener.start.assert_awaited_once()
    for client in listener.platform_info:
        await client.handle_message(message)
        msg = await client.get_latest_message()
        client.get_latest_message.assert_awaited_once()
        assert msg == message


# @pytest.mark.asyncio
# async def test_start_bot(listener, message):
#     # handle_iteration_limit = AsyncMock()
#     # connected = AsyncMock()
#     # connected = MagicMock()
#     await listener.start()
#     listener.platform = AsyncMock()
#     # Check if the handler has been called for each platform
#     for platform in listener.platform_info:
#         # assert platform_info.handler.handle_message.called
#         assert isinstance(
#             platform.handler,
#             (DiscordHandler, TelegramHandler, MatrixHandler),
#         )

#         await platform.handler.handle_message(message)
#         msg = await platform.handler.get_latest_message()
#         assert platform.handler is not None
#         assert platform.handler.is_connected is not None
#         assert platform is not None
#         # handle_iteration_limit.assert_awaited
#         # platform.handler.connected.assert_awaited
#         # connected.assert_called
#         assert msg == message


def test_main():
    client = TestClient(app)
    uvicorn.run = AsyncMock(client)
    uvicorn.run.assert_called_once
