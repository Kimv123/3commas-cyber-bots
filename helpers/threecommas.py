"""Cyberjunky's 3Commas bot helpers."""
from py3cw.request import Py3CW


def load_blacklist(logger, api, blacklistfile):
    """Return blacklist data to be used."""

    # Return file based blacklist
    if blacklistfile:
        newblacklist = []
        try:
            with open(blacklistfile, "r") as file:
                newblacklist = file.read().splitlines()
            if newblacklist:
                logger.info(
                    "Reading local blacklist file '%s' OK (%s pairs)"
                    % (blacklistfile, len(newblacklist))
                )
        except FileNotFoundError:
            logger.error(
                "Reading local blacklist file '%s' failed with error: File not found"
                % blacklistfile
            )

        return newblacklist

    # Return defined blacklist from 3Commaas
    return get_threecommas_blacklist(logger, api)


def init_threecommas_api(cfg):
    """Init the 3commas API."""
    return Py3CW(
        key=cfg.get("settings", "3c-apikey"),
        secret=cfg.get("settings", "3c-apisecret"),
        request_options={
            "request_timeout": 10,
            "nr_of_retries": 3,
            "retry_status_codes": [502, 429],
            "retry_backoff_factor": 1,
        },
    )


def get_threecommas_blacklist(logger, api):
    """Get the pair blacklist from 3Commas."""

    newblacklist = list()
    error, data = api.request(
        entity="bots",
        action="pairs_black_list",
    )
    if data:
        logger.info(
            "Fetched 3Commas pairs blacklist OK (%s pairs)" % len(data["pairs"])
        )
        newblacklist = data["pairs"]
    else:
        if "msg" in error:
            logger.error(
                "Fetching 3Commas pairs blacklist failed with error: %s" % error["msg"]
            )
        else:
            logger.error("Fetching 3Commas pairs blacklist failed")

    return newblacklist


def get_threecommas_btcusd(logger, api):
    """Get current USDT_BTC value to calculate BTC volume24h in USDT."""

    price = 60000
    error, data = api.request(
        entity="accounts",
        action="currency_rates",
        payload={"market_code": "binance", "pair": "USDT_BTC"},
    )
    if data:
        logger.info("Fetched 3Commas BTC price OK (%s USDT)" % data["last"])
        price = data["last"]
    else:
        if error and "msg" in error:
            logger.error(
                "Fetching 3Commas BTC price in USDT failed with error: %s"
                % error["msg"]
            )
        else:
            logger.error("Fetching 3Commas BTC price in USDT failed")

    logger.debug("Current price of BTC is %s USDT" % price)
    return price


def get_threecommas_accounts(logger, api):
    """Get all data for an account."""

    # Fetch all account data, in real mode
    error, data = api.request(
        entity="accounts",
        action="",
        additional_headers={"Forced-Mode": "real"},
    )
    if data:
        return data

    if error and "msg" in error:
        logger.error("Fetching 3Commas accounts data failed error: %s" % error["msg"])
    else:
        logger.error("Fetching 3Commas accounts data failed")

    return None


def get_threecommas_account(logger, api, accountid):
    """Get account details."""

    # Find account data for accountid, in real mode
    error, data = api.request(
        entity="accounts",
        action="account_info",
        action_id=str(accountid),
        additional_headers={"Forced-Mode": "real"},
    )
    if data:
        return data

    if error and "msg" in error:
        logger.error(
            "Fetching 3Commas account data failed for id %s error: %s"
            % (accountid, error["msg"])
        )
    else:
        logger.error("Fetching 3Commas account data failed for id %s", accountid)

    return None


def get_threecommas_account_marketcode(logger, api, accountid):
    """Get market_code for account."""

    # get account data for accountid, in real mode
    error, data = api.request(
        entity="accounts",
        action="account_info",
        action_id=str(accountid),
        additional_headers={"Forced-Mode": "real"},
    )
    if data:
        marketcode = data["market_code"]
        logger.info(
            "Fetched 3Commas account market code in real mode OK (%s)" % marketcode
        )
        return marketcode

    if error and "msg" in error:
        logger.error(
            "Fetching 3Commas account market code failed for id %s error: %s"
            % (accountid, error["msg"])
        )
    else:
        logger.error("Fetching 3Commas account market code failed for id %s", accountid)

    return None


def get_threecommas_account_balance(logger, api, accountid):
    """Get account balances."""

    # Fetch account balance data for accountid, in real mode
    error, data = api.request(
        entity="accounts",
        action="load_balances",
        action_id=str(accountid),
        additional_headers={"Forced-Mode": "real"},
    )
    if data:
        return data

    if error and "msg" in error:
        logger.error(
            "Fetching 3Commas account balances data failed for id %s error: %s"
            % (accountid, error["msg"])
        )
    else:
        logger.error(
            "Fetching 3Commas account balances data failed for id %s", accountid
        )

    return None


def get_threecommas_account_balance_chart_data(
    logger, api, accountid, begindate, enddate
):
    """Get account balance chart data."""

    # Fetch account balance chart data for accountid, in real mode
    error, data = api.request(
        entity="accounts",
        action="balance_chart_data",
        action_id=str(accountid),
        additional_headers={"Forced-Mode": "real"},
        payload={"date_from": begindate, "date_to": enddate},
    )
    if data:
        return data

    if error and "msg" in error:
        logger.error(
            "Fetching 3Commas account balance chart data failed for id %s error: %s"
            % (accountid, error["msg"])
        )
    else:
        logger.error(
            "Fetching 3Commas account balance chart data for id %s", accountid
        )

    return None


def get_threecommas_market(logger, api, market_code):
    """Get all the valid pairs for market_code from 3Commas account."""

    tickerlist = []
    error, data = api.request(
        entity="accounts",
        action="market_pairs",
        payload={"market_code": market_code},
    )
    if data:
        tickerlist = data
        logger.info(
            "Fetched 3Commas market data for '%s' OK (%s pairs)"
            % (market_code, len(tickerlist))
        )
    else:
        if error and "msg" in error:
            logger.error(
                "Fetching 3Commas market data failed for market code %s with error: %s"
                % (market_code, error["msg"])
            )
        else:
            logger.error(
                "Fetching 3Commas market data failed for market code %s", market_code
            )

    return tickerlist


def set_threecommas_bot_pairs(logger, api, thebot, newpairs, notify=True):
    """Update bot with new pairs."""

    # Do we already use these pairs?
    if newpairs == thebot["pairs"]:
        logger.info(
            "Bot '%s' with id '%s' is already using the new pairs"
            % (thebot["name"], thebot["id"]),
            notify,
        )
        return

    logger.debug("Current pairs: %s\nNew pairs: %s" % (thebot["pairs"], newpairs))

    error, data = api.request(
        entity="bots",
        action="update",
        action_id=str(thebot["id"]),
        payload={
            "name": str(thebot["name"]),
            "pairs": newpairs,
            "base_order_volume": float(thebot["base_order_volume"]),
            "take_profit": float(thebot["take_profit"]),
            "safety_order_volume": float(thebot["safety_order_volume"]),
            "martingale_volume_coefficient": float(
                thebot["martingale_volume_coefficient"]
            ),
            "martingale_step_coefficient": float(thebot["martingale_step_coefficient"]),
            "max_safety_orders": int(thebot["max_safety_orders"]),
            "max_active_deals": int(thebot["max_active_deals"]),
            "active_safety_orders_count": int(thebot["active_safety_orders_count"]),
            "safety_order_step_percentage": float(
                thebot["safety_order_step_percentage"]
            ),
            "take_profit_type": thebot["take_profit_type"],
            "strategy_list": thebot["strategy_list"],
            "leverage_type": thebot["leverage_type"],
            "leverage_custom_value": thebot["leverage_custom_value"],
            "bot_id": int(thebot["id"]),
        },
    )
    if data:
        logger.debug("Bot pairs updated: %s" % data)
        logger.info(
            "Bot '%s' with id '%s' updated with %d pairs (%s ... %s)"
            % (thebot["name"], thebot["id"], len(newpairs), newpairs[0], newpairs[-1]),
            notify,
        )
    else:
        if error and "msg" in error:
            logger.error(
                "Error occurred while updating bot '%s' error: %s"
                % (thebot["name"], error["msg"]),
                True,
            )
        else:
            logger.error(
                "Error occurred while updating bot '%s'" % thebot["name"],
                True,
            )


def trigger_threecommas_bot_deal(logger, api, thebot, pair, skip_checks=False):
    """Trigger bot to start deal asap for pair."""

    error, data = api.request(
        entity="bots",
        action="start_new_deal",
        action_id=str(thebot["id"]),
        payload={"pair": pair, "skip_signal_checks": skip_checks},
    )
    if data:
        logger.debug("Bot deal triggered: %s" % data)
        logger.info(
            "Bot '%s' with id '%s' triggered start_new_deal for: %s"
            % (thebot["name"], thebot["id"], pair),
            True,
        )
    else:
        if error and "msg" in error:
            logger.error(
                "Error occurred while triggering start_new_deal bot '%s' error: %s"
                % (thebot["name"], error["msg"]),
            )
        else:
            logger.error(
                "Error occurred while triggering start_new_deal bot '%s'"
                % thebot["name"],
            )


def control_threecommas_bot(logger, api, thebot, cmd):
    """Start or stop a bot."""

    if cmd == "stop_bot":
        action = "disable"
    else:
        action = "enable"

    error, data = api.request(
        entity="bots",
        action=action,
        action_id=str(thebot["id"]),
    )
    if data:
        logger.debug("Bot enabled or disabled: %s" % data)
        logger.info(
            "Bot '%s' is set to '%s'" % (thebot["name"], action),
            True,
        )
    else:
        if error and "msg" in error:
            logger.error(
                "Error occurred while '%s' bot was set to '%s' error: %s"
                % (thebot["name"], action, error["msg"]),
            )
        else:
            logger.error(
                "Error occurred while '%s' bot was set to '%s'"
                % (thebot["name"], action),
            )


def get_threecommas_deals(logger, api, botid):
    """Get all deals from 3Commas linked to a bot."""

    data = None
    error, data = api.request(
        entity="deals",
        action="",
        payload={
            "scope": "finished",
            "bot_id": str(botid),
            "limit": 100,
            "order": "closed_at",
        },
    )
    if error:
        if "msg" in error:
            logger.error(
                "Error occurred while fetching deals error: %s" % error["msg"],
            )
        else:
            logger.error("Error occurred while fetching deals")
    else:
        logger.info("Fetched the deals for bot OK (%s deals)" % len(data))

    return data
