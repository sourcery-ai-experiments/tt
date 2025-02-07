import os

from dxsp import DexSwap
from findmyorder import FindMyOrder

from tt.config import settings
from tt.plugins.plugin_manager import BasePlugin
from tt.utils import send_notification


class DexExchangePlugin(BasePlugin):
    """
    Class DexExchangePlugin
    to support DexSwap object
    built via DXSP lib
    More info: https://github.com/mraniki/dxsp
    Order are identified and parsed
    using Findmyorder lib
    More info: https://github.com/mraniki/findmyorder

    Args:
        None

    Returns:
        None

    """

    name = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self):
        super().__init__()
        self.enabled = settings.dxsp_enabled
        if self.enabled:
            self.fmo = FindMyOrder()
            self.exchange = DexSwap()

    async def send_notification(self, message):
        """Sends notification"""
        # if self.enabled:
        await send_notification(message)

    async def handle_message(self, msg):
        """Handles incoming messages"""
        if not self.should_handle(msg):
            return

        if settings.bot_ignore not in msg or settings.bot_prefix not in msg:
            if await self.fmo.search(msg) and self.should_handle_timeframe():
                order = await self.fmo.get_order(msg)
                if order and settings.trading_enabled:
                    trade = await self.exchange.submit_order(order)
                    if trade:
                        await send_notification(trade)

        if msg.startswith(settings.bot_prefix):
            command, *args = msg.split(" ")
            command = command[1:]

            command_mapping = {
                settings.bot_command_info: self.exchange.get_info,
                settings.bot_command_bal: self.exchange.get_balances,
                settings.bot_command_pos: self.exchange.get_positions,
                settings.bot_command_quote: lambda: self.exchange.get_quotes(args[0]),
            }

            if command in command_mapping:
                function = command_mapping[command]
                await self.send_notification(f"{await function()}")
