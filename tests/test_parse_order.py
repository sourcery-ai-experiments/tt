"""
parse_order tests
"""

import pytest

from tt.utils import parse_order


def test_parse_order_full():
    assert parse_order("buy BTC 0.5 sl=100 tp=200") == {
        "action": "buy",
        "symbol": "BTC",
        "quantity": 0.5,
        "stop_loss": 100.0,
        "take_profit": 200.0,
    }


def test_parse_order_without_optional_fields():
    assert parse_order("sell ETH 2") == {
        "action": "sell",
        "symbol": "ETH",
        "quantity": 2.0,
        "stop_loss": None,
        "take_profit": None,
    }


def test_parse_order_only_stop_loss():
    order = parse_order("buy BTC 1 sl=95.5")
    assert order["stop_loss"] == 95.5
    assert order["take_profit"] is None


def test_parse_order_only_take_profit():
    order = parse_order("buy BTC 1 tp=120")
    assert order["stop_loss"] is None
    assert order["take_profit"] == 120.0


def test_parse_order_options_any_order():
    order = parse_order("buy BTC 1 tp=200 sl=100")
    assert order["stop_loss"] == 100.0
    assert order["take_profit"] == 200.0


def test_parse_order_normalises_case_and_whitespace():
    order = parse_order("  BUY   btc\t0.5  SL=100   TP=200 ")
    assert order == {
        "action": "buy",
        "symbol": "BTC",
        "quantity": 0.5,
        "stop_loss": 100.0,
        "take_profit": 200.0,
    }


@pytest.mark.parametrize(
    "message",
    [
        "",
        "   ",
        "buy",
        "buy BTC",
        "hold BTC 1",
        "buy BTC abc",
        "buy BTC 0",
        "buy BTC -1",
        "buy BTC nan",
        "buy BTC inf",
        "buy BTC 1 sl=abc",
        "buy BTC 1 sl=",
        "buy BTC 1 sl=-5",
        "buy BTC 1 tp=0",
        "buy BTC 1 sl100",
        "buy BTC 1 foo=1",
        "buy BTC 1 extra",
        "buy BTC 1 sl=100 sl=90",
    ],
)
def test_parse_order_invalid(message):
    with pytest.raises(ValueError):
        parse_order(message)


def test_parse_order_non_string():
    with pytest.raises(ValueError):
        parse_order(None)
