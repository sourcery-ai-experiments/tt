"""
Tests for tt.utils.format_order
"""

import pytest

from tt.utils import format_order


def test_format_order_with_sl_and_tp():
    order = {
        "action": "buy",
        "symbol": "BTC",
        "quantity": 0.5,
        "stop_loss": 100,
        "take_profit": 200,
    }
    assert format_order(order) == "BUY 0.5 BTC (SL 100, TP 200)"


def test_format_order_without_optional_fields():
    assert (
        format_order({"action": "sell", "symbol": "ETH", "quantity": 2}) == "SELL 2 ETH"
    )


def test_format_order_only_stop_loss():
    order = {"action": "BUY", "symbol": "BTC", "quantity": 1, "stop_loss": 90}
    assert format_order(order) == "BUY 1 BTC (SL 90)"


def test_format_order_only_take_profit():
    order = {"action": "BUY", "symbol": "BTC", "quantity": 1, "take_profit": 110}
    assert format_order(order) == "BUY 1 BTC (TP 110)"


def test_format_order_none_optional_fields_are_omitted():
    order = {
        "action": "buy",
        "symbol": "BTC",
        "quantity": 1,
        "stop_loss": None,
        "take_profit": None,
    }
    assert format_order(order) == "BUY 1 BTC"


def test_format_order_drops_trailing_zero_on_whole_floats():
    order = {
        "action": "buy",
        "symbol": "BTC",
        "quantity": 3.0,
        "stop_loss": 100.0,
        "take_profit": 200.5,
    }
    assert format_order(order) == "BUY 3 BTC (SL 100, TP 200.5)"


@pytest.mark.parametrize("missing", ["action", "symbol", "quantity"])
def test_format_order_missing_required_field(missing):
    order = {"action": "buy", "symbol": "BTC", "quantity": 1}
    del order[missing]
    with pytest.raises(ValueError, match=missing):
        format_order(order)
