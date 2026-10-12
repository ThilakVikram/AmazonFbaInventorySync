# SP_API_PACKAGE

A small Python package that pulls **FBA inventory summaries** from the Amazon Selling Partner API (SP-API) for several marketplaces and stores them in a MySQL `WarehouseStock` table.

## How it works

1. For each region (NA, EU, FE), it exchanges the region's refresh token for an LWA access token.
2. For each marketplace in that region, it calls the FBA Inventory API (`/fba/inventory/v1/summaries`) and follows pagination.
3. Each inventory summary is turned into a row (ASIN, SKU, FNSKU, fulfillable, inbound and unfulfillable quantities, and so on).
4. The rows are bulk-inserted into MySQL.

Marketplaces covered:

| Region | Marketplaces |
|--------|--------------|
| NA | US, CA, MX |
| EU | UK, DE, FR, SA, NL, PL, ES, AE |
| FE | JP |

## Project layout

| File | Purpose |
|------|---------|
| `__init__.py` | Exposes `main` as the package entry point. |
| `main.py` | `main()`: loops over regions and marketplaces, fetches inventory and inserts it into the database. |
| `__main__.py` | Same flow, run as a module. It also sends a status notification. |
| `SPAPI_Container.py` | Region and marketplace enums, credentials, and the marketplace-ID map. |
| `SPAPI_Caller.py` | Gets access tokens, fetches inventory page by page and builds the database rows. |
| `sp_api_caller.py` / `Initiate_Call.py` | An older, simpler caller and a sample script that uses it. |
| `Database.py` | MySQL connection, plus read and bulk-insert helpers. |
| `Tablequery.py` | Loads SQL files from the `query/` folder. |
| `query/warehouse_stock/insert.sql` | Insert statement for the `WarehouseStock` table. |

## Setup and usage

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for how to install, configure and run the package.
