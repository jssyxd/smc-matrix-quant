# Delete All Orders

Source: https://docs.alpaca.markets/us/reference/deleteallorders-1.md

---
updatedAt: 2026-05-27T17:58:22.000Z
---

Fetch the complete documentation index at: https://docs.alpaca.markets/us/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Delete All Orders

Attempts to cancel all open orders. A response will be provided for each order that is attempted to be cancelled. If an order is no longer cancelable, the server will respond with status 500 and reject the request.

# OpenAPI definition

```json
{
  "components": {
    "schemas": {
      "CanceledOrderResponse": {
        "description": "Represents the result of a request to cancel and order",
        "examples": [
          {
            "id": "d56ba3ea-6d04-48ce-8175-817e242ee608",
            "status": 200
          }
        ],
        "properties": {
          "id": {
            "description": "orderId",
            "format": "uuid",
            "type": "string"
          },
          "status": {
            "description": "http response code",
            "example": 200,
            "type": "integer"
          }
        },
        "title": "CanceledOrderResponse",
        "type": "object"
      }
    },
    "securitySchemes": {
      "API_Key": {
        "description": "",
        "in": "header",
        "name": "APCA-API-KEY-ID",
        "type": "apiKey"
      },
      "API_Secret": {
        "description": "",
        "in": "header",
        "name": "APCA-API-SECRET-KEY",
        "type": "apiKey"
      }
    }
  },
  "info": {
    "contact": {
      "email": "support@alpaca.markets",
      "name": "Alpaca Support",
      "url": "https://alpaca.markets/support"
    },
    "description": "Alpaca's Trading API is a modern platform for algorithmic trading.",
    "termsOfService": "https://s3.amazonaws.com/files.alpaca.markets/disclosures/library/TermsAndConditions.pdf",
    "title": "Trading API",
    "version": "2.0.1"
  },
  "openapi": "3.1.2",
  "paths": {
    "/v2/orders": {
      "delete": {
        "description": "Attempts to cancel all open orders. A response will be provided for each order that is attempted to be cancelled. If an order is no longer cancelable, the server will respond with status 500 and reject the request.",
        "operationId": "deleteAllOrders",
        "responses": {
          "207": {
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/CanceledOrderResponse"
                  },
                  "type": "array"
                }
              }
            },
            "description": "Multi-Status with body.\n\nan array of objects that include the order id and http status code for each status request."
          },
          "500": {
            "description": "Failed to cancel order."
          }
        },
        "summary": "Delete All Orders",
        "tags": [
          "Orders"
        ]
      }
    }
  },
  "security": [
    {
      "API_Key": [],
      "API_Secret": []
    }
  ],
  "servers": [
    {
      "description": "Paper",
      "url": "https://paper-api.alpaca.markets"
    },
    {
      "description": "Live",
      "url": "https://api.alpaca.markets"
    }
  ],
  "tags": [
    {
      "name": "Orders"
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": false
  }
}
```