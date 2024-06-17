from cefi import CexTrader
from findmyorder import FindMyOrder
from loguru import logger

from tt.config import settings
from tt.plugins.plugin_manager import BasePlugin



class CexExchangePlugin(BasePlugin):
    """
    Class CexExchangePlugin
    to support CEX Exchange
    built via Cefi lib
    More info: https://github.com/mraniki/cefi
    Order are identified and parsed
    using Findmyorder lib
    More info: https://github.com/mraniki/findmyorder

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        super().__init__()
        self.enabled = settings.cex_enabled
        if not self.enabled:
            return
        self.fmo = FindMyOrder()
        self.exchange = CexTrader()


    async def handle_message(self, msg):
        """
        Handles incoming messages
        to route to the respective function

        Args:
            msg (str): The incoming message

        Returns:
            None

        """
        if self.should_filter(msg):
            return

        if self.is_command_to_handle(msg):
            command, *args = msg.split(" ")
            command = command[1:]

            command_mapping = {
                settings.bot_command_info: self.exchange.get_info,
                settings.bot_command_quote: lambda: self.exchange.get_quotes(args[0]),
                settings.bot_command_bal: self.exchange.get_balances,
                settings.bot_command_pos: self.exchange.get_positions,
            }

            if command in command_mapping:
                function = command_mapping[command]
                await self.send_notification(f"{await function()}")

        if not self.should_handle_timeframe():
             await self.send_notification("⚠️ Trading restricted")

        if await self.fmo.search(msg) and self.should_handle_timeframe():
            order = await self.fmo.get_order(msg)
            if order and settings.trading_enabled:
                trade = await self.exchange.submit_order(order)
                logger.debug("trade {}", trade)
                if trade:
                    await self.send_notification(trade)