# Retrieve Trading Details for an Account

Source: https://docs.alpaca.markets/us/reference/gettradingaccount.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve Trading Details for an Account

As a broker you can view more trading details about your users.

The response is a Trading Account model.

# OpenAPI definition

```json
{
  "components": {
    "parameters": {
      "AccountID": {
        "description": "Account identifier.",
        "in": "path",
        "name": "account_id",
        "required": true,
        "schema": {
          "format": "uuid",
          "type": "string"
        }
      }
    },
    "schemas": {
      "AccountConfigurations": {
        "description": "Represents additional configuration settings for an account",
        "properties": {
          "disable_overnight_trading": {
            "description": "If true, overnight trading is disabled.",
            "type": "boolean"
          },
          "fractional_trading": {
            "description": "If true, account is able to participate in fractional trading",
            "type": "boolean"
          },
          "max_margin_multiplier": {
            "description": "Can be \"1\" or \"2\"",
            "type": "string"
          },
          "max_options_trading_level": {
            "description": "The desired maximum options trading level. 0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "type": "integer"
          },
          "no_shorting": {
            "description": "If true, account becomes long-only mode.",
            "type": "boolean"
          },
          "ptp_no_exception_entry": {
            "description": "If set to true then Alpaca will accept orders for PTP symbols with no exception. Default is false.",
            "type": "string"
          },
          "suspend_trade": {
            "description": "If true, new orders are blocked.",
            "type": "boolean"
          },
          "trade_confirm_email": {
            "description": "all or none. If none, emails for order fills are not sent.",
            "enum": [
              "all",
              "none"
            ],
            "type": "string"
          }
        },
        "title": "AccountConfigurations",
        "type": "object"
      },
      "AccountStatus": {
        "description": "Designates the current status of this account\n\nPossible Values:\n- **INACTIVE**\nAccount not set to trade given asset.\n- **PAPER_ONLY**\nThe account is limited to paper trading.\n- **ONBOARDING**\nAn application is expected for this user, but has not been submitted yet.\n- **SUBMITTED**\nThe application has been submitted and is being processed.\n- **SUBMISSION_FAILED**\nUsed to display if failure on submission\n- **ACTION_REQUIRED**\nThe application requires manual action.\n- **ACCOUNT_UPDATED**\nUsed to display when Account has been modified by user\n- **APPROVAL_PENDING**\nInitial value. The application approval process is in progress.\n- **APPROVED**\nThe account application has been approved, and waiting to be ACTIVE\n- **REJECTED**\nThe account application is rejected for some reason\n- **ACTIVE**\nThe account is fully active. Trading and funding are processed under this status.\n- **ACCOUNT_CLOSED**\nThe account is closed.\n",
        "enum": [
          "INACTIVE",
          "PAPER_ONLY",
          "ONBOARDING",
          "SUBMITTED",
          "SUBMISSION_FAILED",
          "ACTION_REQUIRED",
          "ACCOUNT_UPDATED",
          "APPROVAL_PENDING",
          "APPROVED",
          "REJECTED",
          "ACTIVE",
          "ACCOUNT_CLOSED"
        ],
        "example": "ACTIVE",
        "type": "string"
      },
      "AdminConfigurations": {
        "description": "These configurations show account properties that are overriden either by Alpaca Broker Operations or an automated process.\n\nThese values cannot be modified by the Broker Partners.\n\nThis schema represents the current, effective value of each configuration (e.g. as returned by the get trading account endpoint). For the shape of the payloads broadcast by the **events** streaming API when these values change, see [AdminConfigurationsEvent](#/components/schemas/AdminConfigurationsEvent).",
        "properties": {
          "acct_daily_transfer_limit": {
            "description": "Override the correspondent level daily transfer limits",
            "format": "decimal",
            "type": "string"
          },
          "allow_instant_ach": {
            "description": "If true, the account is allowed to perform instant ACH",
            "type": "boolean"
          },
          "disable_algodash_access": {
            "description": "If true, the account is allowed to access algo dash",
            "type": "boolean"
          },
          "disable_api_key": {
            "description": "If true, the account's API key will be disabled",
            "type": "boolean"
          },
          "disable_crypto": {
            "description": "If true, the account is not allowed to trade cryptos",
            "type": "boolean"
          },
          "disable_day_trading": {
            "description": "If true, the account is not allowed to day trade (e.g. buy and sell the same security on the same day)",
            "type": "boolean"
          },
          "disable_fractional": {
            "description": "If true, the account cannot create orders for fractional share positions",
            "type": "boolean"
          },
          "disable_shorting": {
            "description": "If true the account is not allowed to create short position orders",
            "type": "boolean"
          },
          "incoming_transfers_blocked": {
            "description": "If true, incoming transfers to this account are rejected",
            "type": "boolean"
          },
          "max_margin_multiplier": {
            "description": "The max margin multiplier set by admin for this account. Can be \"1\", \"2\", or \"4\".",
            "type": "string"
          },
          "max_options_trading_level": {
            "description": "The max options trading level set by admin for this account.\n0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\n",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "type": "integer"
          },
          "outgoing_transfers_blocked": {
            "description": "If true, outgoing transfers from this account are rejected",
            "type": "boolean"
          },
          "restrict_to_liquidation_reasons": {
            "$ref": "#/components/schemas/RestrictToLiquidationReasons"
          }
        },
        "title": "AdminConfigurations",
        "type": "object"
      },
      "RestrictToLiquidationReasons": {
        "description": "Reasons why the liquidation only flag was set",
        "properties": {
          "ach_return": {
            "description": "Set when an incoming ACH transfer gets rejected",
            "type": "boolean"
          },
          "position_to_equity_ratio": {
            "description": "Set when the position to equity ration exceeds the maximum limit",
            "type": "boolean"
          },
          "unspecified": {
            "description": "Default value for unknown reason",
            "type": "boolean"
          }
        },
        "title": "RestrictToLiquidationReasons",
        "type": "object"
      },
      "TradeAccount": {
        "description": "This is an extended version of the Account model found [in the trading api](https://alpaca.markets/docs/api-references/trading-api/account/#account-entity).\n\nExtra data has been added that would be useful for brokers.",
        "examples": [
          {
            "account_blocked": false,
            "account_number": "927584925",
            "accrued_fees": "0",
            "admin_configurations": {},
            "balance_asof": "2021-04-01",
            "buying_power": "103556.8572572922",
            "cash": "24861.91",
            "cash_transferable": "24861.91",
            "cash_withdrawable": "17861.91",
            "clearing_broker": "VELOX",
            "created_at": "2021-03-01T13:28:49.270232Z",
            "crypto_status": "ACTIVE",
            "currency": "USD",
            "effective_buying_power": "103556.8572572922",
            "equity": "28059.3882330664",
            "id": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4",
            "initial_margin": "1598.7391165332",
            "intraday_adjustments": "0",
            "last_buying_power": "104433.9158860662",
            "last_cash": "23861.91",
            "last_equity": "26977.323677655",
            "last_initial_margin": "1557.7068388275",
            "last_long_market_value": "3115.413677655",
            "last_maintenance_margin": "934.6241032965",
            "last_options_buying_power": "25419.62",
            "last_regt_buying_power": "50839.233677655",
            "last_short_market_value": "0",
            "long_market_value": "3197.4782330664",
            "maintenance_margin": "959.24346991992",
            "multiplier": "2",
            "non_marginable_buying_power": "24861.91",
            "options_approved_level": 0,
            "options_buying_power": "26460.65",
            "options_trading_level": 0,
            "pending_reg_taf_fees": "0",
            "pending_transfer_out": "0",
            "portfolio_value": "28059.3882330664",
            "position_market_value": "3197.4782330664",
            "previous_close": "2021-04-01T19:00:00-04:00",
            "regt_buying_power": "52921.2982330664",
            "short_market_value": "0",
            "shorting_enabled": true,
            "sma": "26758.0590204615",
            "status": "ACTIVE",
            "trade_suspended_by_user": false,
            "trading_blocked": false,
            "transfers_blocked": false
          },
          {
            "account_blocked": false,
            "account_number": "601612064",
            "accrued_fees": "0",
            "admin_configurations": {},
            "balance_asof": "2022-02-08",
            "buying_power": "83567.42",
            "cash": "83567.42",
            "cash_transferable": "41783.71",
            "cash_withdrawable": "0",
            "clearing_broker": "VELOX",
            "created_at": "2022-01-21T21:25:26.713802Z",
            "crypto_status": "PAPER_ONLY",
            "currency": "USD",
            "effective_buying_power": "83567.42",
            "equity": "83567.42",
            "id": "56712986-9ff7-4d8f-8e52-077e099e533e",
            "initial_margin": "0",
            "intraday_adjustments": "0",
            "last_buying_power": "41783.71",
            "last_cash": "41783.71",
            "last_equity": "41783.71",
            "last_initial_margin": "0",
            "last_long_market_value": "0",
            "last_maintenance_margin": "0",
            "last_options_buying_power": "41783.71",
            "last_regt_buying_power": "41783.71",
            "last_short_market_value": "0",
            "long_market_value": "0",
            "maintenance_margin": "0",
            "multiplier": "1",
            "non_marginable_buying_power": "41783.71",
            "options_approved_level": 2,
            "options_buying_power": "83567.42",
            "options_trading_level": 1,
            "pending_reg_taf_fees": "0.01",
            "pending_transfer_in": "0",
            "pending_transfer_out": "0",
            "portfolio_value": "83567.42",
            "position_market_value": "0",
            "previous_close": "2022-02-08T19:00:00-05:00",
            "regt_buying_power": "83567.42",
            "short_market_value": "0",
            "shorting_enabled": false,
            "sma": "0",
            "status": "ACTIVE",
            "trade_suspended_by_user": false,
            "trading_blocked": false,
            "transfers_blocked": false
          }
        ],
        "properties": {
          "account_blocked": {
            "description": "If true, the account activity by user is prohibited.",
            "example": false,
            "type": "boolean"
          },
          "account_number": {
            "description": "The account number",
            "example": "927584925",
            "type": [
              "string",
              "null"
            ]
          },
          "accrued_fees": {
            "description": "Accrued fees",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "admin_configurations": {
            "$ref": "#/components/schemas/AdminConfigurations"
          },
          "balance_asof": {
            "description": "The date of the snapshot for `last_*` fields",
            "example": "2021-04-01",
            "type": "string"
          },
          "buying_power": {
            "description": "Current available cash buying power. If multiplier = 2 then buying_power = max(equity-initial_margin(0) * 2). If multiplier = 1 then buying_power = cash.",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "cash": {
            "description": "Cash balance",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "cash_transferable": {
            "description": "Cash available for transfer (JNLC)",
            "example": "12345.6789",
            "type": "string"
          },
          "cash_withdrawable": {
            "description": "Cash available for withdrawal",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "clearing_broker": {
            "description": "Clearing broker",
            "example": "Velox",
            "type": "string"
          },
          "created_at": {
            "description": "Timestamp this account was created at",
            "example": "2021-03-01T13:28:49.270232Z",
            "type": "string"
          },
          "crypto_status": {
            "$ref": "#/components/schemas/AccountStatus"
          },
          "currency": {
            "description": "Always USD",
            "example": "USD",
            "type": "string"
          },
          "effective_buying_power": {
            "description": "Effective buying power (duplicate of buying power)",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "equity": {
            "description": "cash + long_market_value + short_market_value",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "id": {
            "description": "The account ID",
            "example": "c8f1ef5d-edc0-4f23-9ee4-378f19cb92a4",
            "format": "uuid",
            "type": "string"
          },
          "initial_margin": {
            "description": "Reg T initial margin requirement (continuously updated value)",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "intraday_adjustments": {
            "description": "The intraday adjustment by non_trade_activities such as fund deposit/withdraw.\n",
            "example": "0",
            "type": "string"
          },
          "last_buying_power": {
            "description": "Value of buying_power as of previous trading day at 16:00:00 ET",
            "example": "12345.6789",
            "type": "string"
          },
          "last_cash": {
            "description": "Value of all cash as of previous trading day at 16:00:00 ET",
            "example": "12345.6789",
            "type": "string"
          },
          "last_equity": {
            "description": "Equity as of previous trading day at 16:00:00 ET",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "last_initial_margin": {
            "description": "Value of Reg T margin as of previous trading day at 16:00:00 ET",
            "example": "12345.6789",
            "type": "string"
          },
          "last_long_market_value": {
            "description": "Value of all long positions as of previous trading day at 16:00:00 ET",
            "example": "12345.6789",
            "type": "string"
          },
          "last_maintenance_margin": {
            "description": "Maintenance margin requirement on the previous trading day",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "last_options_buying_power": {
            "description": "Value of option buying power as of previous trading day at 16:00:00 ET",
            "example": "12345.6789",
            "type": "string"
          },
          "last_regt_buying_power": {
            "description": "Value of Reg T buying power as of previous trading day at 16:00:00 ET",
            "example": "12345.6789",
            "type": "string"
          },
          "last_short_market_value": {
            "description": "Value of all short positions as of previous trading day at 16:00:00 ET",
            "example": "0",
            "type": "string"
          },
          "long_market_value": {
            "description": "Real-time MtM value of all long positions held in the account",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "maintenance_margin": {
            "description": "Maintenance margin requirement (continuously updated value)",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "memoposts": {
            "description": "Outstanding memopost value",
            "example": "100",
            "type": "string"
          },
          "multiplier": {
            "description": "\"1\", \"2\", \"3\", or \"4\"",
            "example": "2",
            "format": "decimal",
            "type": "string"
          },
          "non_marginable_buying_power": {
            "description": "Non-marginable buying power (currently used for only crypto trading)",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "options_approved_level": {
            "description": "The options trading level that was approved for this account.\n0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\n",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "example": 3,
            "type": "integer"
          },
          "options_buying_power": {
            "description": "Your buying power for options trading",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "options_trading_level": {
            "description": "The effective options trading level of the account.\nThis is the minimum between account options_approved_level and account configurations max_options_trading_level.\n0=disabled, 1=Covered Call/Cash-Secured Put, 2=Long Call/Put, 3=Spreads/Straddles.\n",
            "enum": [
              0,
              1,
              2,
              3
            ],
            "example": 3,
            "type": "integer"
          },
          "pending_reg_taf_fees": {
            "description": "Pending regulatory fees for the account.",
            "example": "0.01",
            "type": "string"
          },
          "pending_transfer_out": {
            "description": "Cash pending transfer out",
            "example": "12345.6789",
            "type": "string"
          },
          "portfolio_value": {
            "description": "Total value of cash + holding positions. (This field is deprecated. It is equivalent to the equity field.)",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "position_market_value": {
            "description": "Real-time MtM value of all the positions held in the account",
            "example": "0",
            "format": "decimal",
            "type": "string"
          },
          "previous_close": {
            "description": "Previous sessions close time",
            "example": "2021-04-01T19:00:00-04:00",
            "type": "string"
          },
          "regt_buying_power": {
            "description": "User's buying power under Regulation T (excess equity - (equity - margin value) - * margin multiplier)",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "short_market_value": {
            "description": "Real-time MtM value of all short positions held in the account",
            "example": "0",
            "format": "decimal",
            "type": "string"
          },
          "shorting_enabled": {
            "description": "Flag to denote whether or not the account is permitted to short",
            "example": false,
            "type": "boolean"
          },
          "sma": {
            "description": "Value of Special Memorandum Account (will be used at a later date to provide additional buying_power)",
            "example": "12345.6789",
            "format": "decimal",
            "type": "string"
          },
          "status": {
            "$ref": "#/components/schemas/AccountStatus"
          },
          "trade_suspended_by_user": {
            "description": "If true, the account is not allowed to place orders.",
            "example": false,
            "type": "boolean"
          },
          "trading_blocked": {
            "description": "If true, the account is not allowed to place orders.",
            "example": false,
            "type": "boolean"
          },
          "transfers_blocked": {
            "description": "If true, the account is not allowed to request money transfers.",
            "example": false,
            "type": "boolean"
          },
          "user_configurations": {
            "anyOf": [
              {
                "$ref": "#/components/schemas/AccountConfigurations"
              },
              {
                "type": "null"
              }
            ],
            "description": "Custom user-level configuration overrides for this account.\n\nThis field is always present in the response, but its value will be `null` until user-level configurations have been explicitly set for the account."
          }
        },
        "required": [
          "id",
          "admin_configurations",
          "account_number",
          "status",
          "crypto_status",
          "currency",
          "buying_power",
          "regt_buying_power",
          "effective_buying_power",
          "non_marginable_buying_power",
          "accrued_fees",
          "portfolio_value",
          "trading_blocked",
          "transfers_blocked",
          "account_blocked",
          "created_at",
          "trade_suspended_by_user",
          "multiplier",
          "shorting_enabled",
          "equity",
          "last_equity",
          "long_market_value",
          "short_market_value",
          "position_market_value",
          "initial_margin",
          "maintenance_margin",
          "last_maintenance_margin",
          "sma",
          "balance_asof",
          "cash"
        ],
        "type": "object"
      }
    },
    "securitySchemes": {
      "BasicAuth": {
        "scheme": "basic",
        "type": "http"
      }
    }
  },
  "info": {
    "contact": {
      "email": "support@alpaca.markets",
      "name": "Alpaca Support",
      "url": "https://alpaca.markets/support"
    },
    "description": "Open brokerage accounts, enable stock, options and crypto trading. Manage the ongoing user experience and brokerage customer lifecycle with the Alpaca Broker API",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Broker API",
    "version": "1.1.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v1/trading/accounts/{account_id}/account": {
      "get": {
        "description": "As a broker you can view more trading details about your users.\n\nThe response is a Trading Account model.",
        "operationId": "getTradingAccount",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/TradeAccount"
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve Trading Details for an Account",
        "tags": [
          "Accounts"
        ]
      },
      "parameters": [
        {
          "$ref": "#/components/parameters/AccountID"
        }
      ]
    }
  },
  "security": [
    {
      "BasicAuth": []
    }
  ],
  "servers": [
    {
      "description": "Sandbox endpoint",
      "url": "https://broker-api.sandbox.alpaca.markets"
    },
    {
      "description": "Production endpoint",
      "url": "https://broker-api.alpaca.markets"
    }
  ],
  "tags": [
    {
      "name": "Accounts"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```