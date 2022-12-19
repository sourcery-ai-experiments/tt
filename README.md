# Telegram Trader
 CEX, DEX and Telegram integration. 
 Based on python telegram bot v20, CCXT v2, Web3 v6 and TinyDB v4.
 Deploy it via docker. 

[![](https://badgen.net/badge/icon/TT/E2B13C?icon=bitcoin&label)](https://github.com/mraniki/tt)
[![donate](https://badgen.net/badge/icon/coindrop/6F4E37?icon=buymeacoffee&label)](https://coindrop.to/mraniki) 
[![Docker Pulls](https://badgen.net/docker/pulls/mraniki/tt)](https://hub.docker.com/r/mraniki/tt)

Built with
[![telegrambot](https://badgen.net/badge/icon/telegrambot?icon=telegram&label)](https://t.me/pythontelegrambotchannel)
[![python3.10](https://badgen.net/badge/icon/3.10/black?icon=pypi&label)](https://www.python.org/downloads/release/python-3100/)
[![ccxt](https://badgen.net/badge/icon/ccxt/black?icon=libraries&label)](https://github.com/ccxt/ccxt)
[![Web3](https://badgen.net/badge/icon/web3/black?icon=libraries&label)](https://github.com/ethereum/web3.py)
[![apprise](https://badgen.net/badge/icon/apprise/black?icon=libraries&label)](https://github.com/caronc/apprise)
[![sublime](https://badgen.net/badge/icon/sublime/F96854?icon=terminal&label)](https://www.sublimetext.com/)
[![workingcopy](https://badgen.net/badge/icon/workingcopy/16DCCD?icon=github&label)](https://workingcopy.app/)

## Build status
[![Docker](https://github.com/mraniki/tt/actions/workflows/DockerHub.yml/badge.svg)](https://github.com/mraniki/tt/actions/workflows/DockerHub.yml) [![DockerNightly](https://github.com/mraniki/tt/actions/workflows/DockerHub_Dev.yml/badge.svg)](https://github.com/mraniki/tt/actions/workflows/DockerHub_Dev.yml)

## Install
1) Create a private channel and a bot via [@BotFather ](https://core.telegram.org/bots/tutorial)
2) Get your 
  - CEX API Keys supported by [CCXT](https://github.com/ccxt/ccxt) or 
  - DEX contract router supported by [Web3](https://github.com/ethereum/web3.py)
3) Update the config (as per below), bot token, API in the .env file or in db config (and point your config to container volume /code/config)
4) Deploy :
- via docker dockerhub (or ghcr.io) `docker push mraniki/tt:latest` (or `docker push mraniki/tt:nightly`)
- or `git clone https://github.com/mraniki/tt:main` and `pip install -r requirements.txt` and `python3 bot.py` 
6) Start your container
7) Submit order to the bot as per the following Order format DIRECTION SYMBOL STOPLOSS TAKEPROFIT QUANTITY 
  (e.g. `sell BTCUSDT sl=6000 tp=4500 q=1%`) or for DEFI `BUY BTCB`

## Config
Either use .env file or json db as per below structure.
Environment file is loaded in db at the startup. 
Approach: Env is best for 1 CEX setup. DB allows support for multiple DEX and CEX.

### Env
[env sample](config/env.sample)

### DB Structure
[DB sample](config/db.json.sample)

 ## Features Available
 
 v1 
 - Enable bot in pythontelegram v20 and support exchange formatted error via telegram
 - Push your signal manually or from system like trading view webhook to submit order to your ccxt exchange and receive confirmation
 - Disable or Enable trading process via /trading command
 - Query balance via /bal command and view it in formatted way
 - Enable dev and main branches with auto release and docker deployment pipeline setup for continueous deployment in dockerhub and github container repo
 - Support multiple enviroment via environment variable file (e.g. POC, DEV, SIT, PRD)
 - Support % of USDT balance for CEX order
 - Support bot in private channel (or private chat) and multiple channel per enviroment
 - Handle Multi CEFI config (verified with Binance, Binance Testnet and ~~FTX~~ Kraken) and DEFI (test with Pancakeswap and Quickswap) and switch between CEFI using `/cex binance` or `/cex kraken` or DEFI `/dex pancake`
 - Support config folder and config file in the dockerfile to automatically create the volume folder and its config
 - Setup send message overall function for further improvement
 - Integrate DEFI DEX (tested with BSC & pancakeswap) for balance query and order placing for mainnet and testnet with format `buy btcb`
 - Integrate with apprise library to support more notification delivery
 - Handle libraries exceptions in one consolidated function to ease notifications
 - Support `/price BTCB` or `/price btc/usdt` command for symbol price check for both CEX and DEX
 
![IMG_2517](https://user-images.githubusercontent.com/8766259/199422978-dc3322d9-164b-42af-9cf2-84c6bc3dae29.jpg)

 ## 🚧 Roadmap

v1.1
- Support DEFI DEX quickswap (built done and to be tested)

V1.2
- Update the buy/sell parsing logic to align dex and cex format and manage missing argument error with default values


V1.3
- Simplify the Exchange search
- Allow to start with DEX for initial start

v1.4
- Update the start logic to build the db to simplify the start 
- create / modify db via bot command

v1.5
- Support DEFI DEX uniswap
- Support Web3 ENS
- Support futures and margin for CEX (to be tested)

v2
- view daily pnl and free margin in /bal response
- view weekly pnl with /w command
- view opened future position via /pos command
- Support bot in webhook instead of getupdate

v3
- Integrate with messaging platform agnostic like Matrix (https://github.com/poljar/matrix-ni)
- Merge with Telegram MQL4 version which integrate with MT4 exchanges for TradFi support[![mql](https://badgen.net/badge/icon/mql/black?icon=libraries&label)](https://mql5.com/)


 ## ⚠️ Disclaimer
 This is an education tool and should not be considered professional financial investment system nor financial advice. Use a testnet account or **USE AT YOUR OWN RISK**

