# Setup and Usage

How to install, configure and run `SP_API_PACKAGE`. For what the package does, see [README.md](README.md).

## 1. Requirements

- Python 3.12 or newer
- A MySQL database with a `WarehouseStock` table (see step 4)
- SP-API app credentials (client ID and client secret) and a refresh token for each region you use

## 2. Install dependencies

From inside the package folder:

```bash
pip install -r requirements.txt
```

## 3. Configure `.env`

Copy the example file:

```bash
cp .env.example .env
```

Fill in the values:

```ini
# MySQL
host =
user =
password =
database =

# SP-API app credentials
client_id =
client_secret =
app_id =

# Refresh token for each region
na_refresh_token =
eu_refresh_token =
fe_refresh_token =

# Status notification endpoint (used when run as a module)
notification_url =
```

Keep these points in mind:

- `.env` must be in the package folder. The package loads it from there, not from where you run the command.
- Key names are case-sensitive. Use lowercase `host`, not `Host`.
- `.env` is ignored by git. Never commit real credentials.

## 4. Create the database table

The insert statement in `query/warehouse_stock/insert.sql` expects these columns:

| Column | Filled with |
|--------|-------------|
| `updated_date` | Today's date |
| `asin` | `asin` |
| `sku` | `sellerSku` |
| `fnsku` | `fnSku` |
| `item_name` | Empty |
| `quantity` | `fulfillableQuantity` |
| `inbound_quantity` | `inboundReceivingQuantity` |
| `outbound_quantity` | Always `0` |
| `reviewing_quantity` | Always `0` |
| `damaged_quantity` | `totalUnfulfillableQuantity` |
| `overall_quantity` | Fulfillable plus unfulfillable |
| `warehouse` | `FBA <marketplace>`, for example `FBA US` |
| `warehouse_id` | Empty |
| `unstructured_name` | Empty |

## 5. Run

Run these from the folder that **contains** `SP_API_PACKAGE`, not from inside it.

Run all marketplaces as a module (this also sends the status notification):

```bash
python -m SP_API_PACKAGE
```

Run all marketplaces from Python:

```python
from SP_API_PACKAGE import main

main()
```

Fetch rows for one marketplace without saving them:

```python
from SP_API_PACKAGE.SPAPI_Caller import Values_Getter, Region, EU_Marketplace

for rows in Values_Getter(Region.EU, EU_Marketplace.DE):
    print(rows)  # a list of row tuples, one page at a time
```

## 6. Change which marketplaces run

Edit the `available_marketplace` dictionary in `main.py` (or `__main__.py`). The supported values are defined in `SPAPI_Container.py`:

| Region | Available marketplaces |
|--------|------------------------|
| `Region.NA` | US, CA, MX, BR |
| `Region.EU` | UK, DE, FR, IT, ES, NL, SE, PL, BE, TR, AE, SA |
| `Region.FE` | JP, AU, SG, IN |

## Troubleshooting

| Problem | Likely cause |
|---------|--------------|
| `ImportError: attempted relative import` | You ran a file directly or ran from inside the package folder. Use `python -m SP_API_PACKAGE` from the parent folder. |
| MySQL cannot connect or the host is empty | `.env` is missing from the package folder, or the key is `Host` instead of `host`. |
| No access token, or repeated 403 errors | Wrong `client_id` or `client_secret`, or the refresh token for that region is wrong or expired. |
| 400 "Missing Required Details" | The marketplace is not set up for the seller account, or a request parameter is invalid. |
| 429 responses | SP-API rate limit. The caller waits 3 seconds and retries. |
| `SyntaxError` in `SPAPI_Caller.py` | Your Python is older than 3.12. |
