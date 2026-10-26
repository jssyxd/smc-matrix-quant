# Retrieve JIT Reports

Source: https://docs.alpaca.markets/us/reference/get-v1-transfers-jit-reports.md

---
updatedAt: 2026-04-20T20:39:51.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Retrieve JIT Reports

Retrieves a JIT report for the requested report type and system date. By default, the report is returned inline. For large reports, use response_type=download_url to receive a temporary signed download URL.


# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "JITReport": {
        "description": "JIT Securities reports are made available through the API and can be accessed within the hour after 11:30 PM EST on the trade date (T+0). The reports communicate transaction-level details as well as overall settlement amounts, transfer direction, and payment timing.",
        "properties": {
          "detail": {
            "description": "Contains all activities that impact cash throughout the trading session including executed trades, trading fees, and corporate actions that involve cash allocations.\n\ncontent-type = application/csv",
            "type": "string"
          },
          "net_payment": {
            "description": "Highlights the net amount due to Alpaca by settlement or to the partner on the date of settlement in a formalized invoice format.\n\ncontent-type = application/pdf",
            "type": "string"
          },
          "net_payment_final": {
            "description": "Includes additional information to account for T+0 and T+1 settling activity to clarify settlement journaling reconciliation. This report is generated after trading session close on T+1.\n\ncontent-type = application/pdf",
            "type": "string"
          },
          "net_summary": {
            "description": "Consists of three columns and a single row, which lists the net money movement to or from Alpaca for T0, T1, and T2.\n\ncontent-type = application/csv",
            "type": "string"
          },
          "obligation": {
            "description": "Lists of all open obligations towards the partner that are to be settled.\n\ncontent-type = application/csv",
            "type": "string"
          }
        },
        "title": "JITReport",
        "type": "object"
      },
      "JITReportDownloadURL": {
        "properties": {
          "expires_at": {
            "description": "Timestamp when the signed URL expires.",
            "format": "date-time",
            "type": "string"
          },
          "filename": {
            "description": "Name of the generated report file.",
            "type": "string"
          },
          "url": {
            "description": "Temporary signed URL used to download the report.",
            "format": "uri",
            "type": "string"
          }
        },
        "required": [
          "url",
          "filename",
          "expires_at"
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
    "/v1/transfers/jit/reports": {
      "get": {
        "description": "Retrieves a JIT report for the requested report type and system date. By default, the report is returned inline. For large reports, use response_type=download_url to receive a temporary signed download URL.\n",
        "operationId": "get-v1-transfers-jit-reports",
        "parameters": [
          {
            "description": "The type of report you want to get.",
            "in": "query",
            "name": "report_type",
            "required": true,
            "schema": {
              "enum": [
                "detail",
                "net_summary",
                "net_payment",
                "net_payment_final",
                "gross_summary",
                "gross_payment",
                "gross_payment_final",
                "obligation"
              ],
              "type": "string"
            }
          },
          {
            "description": "Date of file generation.",
            "in": "query",
            "name": "system_date",
            "required": true,
            "schema": {
              "format": "date",
              "type": "string"
            }
          },
          {
            "description": "The asset class to retrieve for.",
            "in": "query",
            "name": "asset_class",
            "schema": {
              "enum": [
                "us_equity",
                "crypto"
              ],
              "type": "string"
            }
          },
          {
            "description": "Controls how the report is returned. Use inline to return the report content directly in the response. Use download_url to return a temporary signed URL that can be used to download the generated report. If omitted, the default value is inline.\n",
            "in": "query",
            "name": "response_type",
            "required": false,
            "schema": {
              "default": "inline",
              "enum": [
                "inline",
                "download_url"
              ],
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "examples": {
                  "download_url": {
                    "description": "Returned when response_type is download_url.",
                    "summary": "Download URL response",
                    "value": {
                      "expires_at": "2026-04-14T23:55:00Z",
                      "filename": "jit_detail_2026-04-14.csv",
                      "url": "<signed_s3_url>"
                    }
                  },
                  "inline": {
                    "description": "Returned when response_type is inline or omitted.",
                    "summary": "Inline report response",
                    "value": {
                      "detail": "<report_content>"
                    }
                  }
                },
                "schema": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/JITReport"
                    },
                    {
                      "$ref": "#/components/schemas/JITReportDownloadURL"
                    }
                  ]
                }
              }
            },
            "description": "OK"
          }
        },
        "summary": "Retrieve JIT Reports",
        "tags": [
          "Funding"
        ]
      }
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
      "name": "Funding"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```