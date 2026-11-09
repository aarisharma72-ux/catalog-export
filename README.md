# catalog-export

Daily catalog CSV export for stock reviews. Requires Python 3.10 or newer.

```sh
python export.py --active-only
python export.py --input sample.json --output exports/catalog.csv
```

Exports SKU, name, category, price, stock, and active status. The default output name includes the current date.
