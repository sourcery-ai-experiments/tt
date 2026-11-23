"""
 Talky Utils

 This module contains utility functions
 for the TalkyTrader app such as:

 - send_notification
 - run_bot
 - start plugins
 - start_bot
 - dheck version
 - format_order

"""

__version__ = "7.2.29"


import asyncio

import aiohttp
from apprise import Apprise, NotifyFormat
from iamlistening import Listener

from tt.config import logger, settings
from tt.plugins.plugin_manager import PluginManager


async def send_notification(msg):
    """
    💬 Notification via Apprise.
    Apprise endpoint URL can be a URL
    for the chat, an URL to an Apprise config
    or a URL to the Apprise API endpoint
    apprise_url = "tgram://BOTTOKEN/CHANNEL"
    apprise_url = "discord://token1/channel"

    Args:
        msg (str): Message

    Returns:
        None

    More info
    https://github.com/caronc/apprise/wiki

    """
    if not settings.apprise_url:
        logger.warning("No Apprise URL set")
        return
    if msg is None:
        logger.warning("No message to send")
        return
    aobj = Apprise(settings.apprise_url)
    msg_format = settings.apprise_format or NotifyFormat.MARKDOWN
    try:
        await aobj.async_notify(body=msg, body_format=msg_format)
    except Exception as error:
        logger.error("Verify Apprise URL", error)


async def run_bot():
    """
    🤖 Run the chat bot & the plugins
    via an asyncio loop.

    Returns:
        None

    More info: https://github.com/mraniki/iamlistening

    """
    if settings.version_check:
        await check_version()
    listener = Listener()
    plugin_manager = PluginManager()
    await asyncio.gather(start_bot(listener, plugin_manager))


async def start_plugins(plugin_manager):
    """
    🔌 Start all plugins.


    Returns:
        None

    Refer to chat manager for plugin info

    """
    if settings.plugin_enabled:
        plugin_manager.load_plugins(settings.authorized_plugins)
        loop = asyncio.get_running_loop()
        loop.create_task(plugin_manager.start_all_plugins())


async def start_bot(listener, plugin_manager, max_iterations=None):
    """
    👂 Start the chat listener and
    dispatch messages to plugins

    Args:
        listener (Listener): Listener
        plugin_manager (PluginManager): PluginManager
        max_iterations (int): Max iterations

    Returns:
        None

    """

    loop = asyncio.get_running_loop()
    loop.create_task(listener.start())
    await start_plugins(plugin_manager)
    iteration = 0
    if not listener.clients:
        logger.warning(
            """
            No listener clients.
            Verify settings and check wiki for example
            https://talky.readthedocs.io/en/latest/02_config.html
            """
        )
        return
    while True:
        for client in listener.clients:
            msg = await client.get_latest_message()
            if msg:
                await plugin_manager.process_message(msg)
        iteration += 1
        if max_iterations is not None and iteration >= max_iterations:
            break

    await asyncio.sleep(1)


async def check_version():
    """
    Asynchronously checks the version
    of the GitHub repository.

    This function sends a GET request to the
    specified GitHub repository URL and retrieves the
    latest version of the repository.
    It then compares the latest version
    with the current version (__version__)
    and logs the result.

    Parameters:
        None

    Returns:
        None
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.repo, timeout=10) as response:
                if response.status != 200:
                    return

                github_repo = await response.json()
                latest_version = github_repo["name"]
                if latest_version != f"v{__version__}":
                    logger.debug(
                        "You are NOT using the latest %s: %s",
                        latest_version,
                        __version__,
                    )
                else:
                    logger.debug(f"You are using the latest {__version__}")
    except Exception as error:
        logger.error("check_version: {}", error)


def _format_number(value):
    """
    Render a numeric value without a redundant trailing ".0"
    (e.g. 100.0 -> "100", 0.5 -> "0.5"). Non-float values
    are rendered with str().
    """
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def format_order(order: dict) -> str:
    """
    Format an order dict into a one-line
    human-readable message.

    Args:
        order (dict): Order with the keys ``action``,
            ``symbol``, ``quantity`` and the optional
            ``stop_loss`` and ``take_profit``.
            Optional keys that are missing or None are omitted.

    Returns:
        str: e.g. ``"BUY 0.5 BTC (SL 100, TP 200)"``

    Raises:
        ValueError: if a required key is missing or None.

    """
    # Read each field exactly once so validation and formatting
    # always use the same values.
    fields = {
        key: order.get(key)
        for key in ("action", "symbol", "quantity", "stop_loss", "take_profit")
    }
    missing = [key for key in ("action", "symbol", "quantity") if fields[key] is None]
    if missing:
        raise ValueError(f"Order is missing required field(s): {', '.join(missing)}")

    message = (
        f"{str(fields['action']).upper()} "
        f"{_format_number(fields['quantity'])} "
        f"{fields['symbol']}"
    )
    extras = [
        f"{label} {_format_number(fields[key])}"
        for key, label in (("stop_loss", "SL"), ("take_profit", "TP"))
        if fields[key] is not None
    ]
    if extras:
        message += f" ({', '.join(extras)})"
    return message
