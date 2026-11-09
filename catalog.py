import json
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from settings import API_KEY, API_URL, REQUEST_TIMEOUT


def fetch_products():
    request = Request(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Catalog request returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"Catalog request failed: {exc.reason}") from exc


def product_rows(payload, active_only=False):
    products = payload.get("items") if isinstance(payload, dict) else payload
    if not isinstance(products, list):
        raise ValueError("Expected a product list or an object containing items")

    for index, product in enumerate(products, start=1):
        if not isinstance(product, dict):
            raise ValueError(f"Product {index} is not an object")
        sku = str(product.get("sku", "")).strip()
        if not sku:
            raise ValueError(f"Product {index} has no SKU")
        active = product.get("active", True)
        if not isinstance(active, bool):
            raise ValueError(f"Product {sku} has an invalid active flag")
        if active_only and not active:
            continue
        try:
            price = Decimal(str(product.get("price", 0)))
            if not price.is_finite():
                raise InvalidOperation
            formatted_price = str(price.quantize(Decimal("0.01")))
            stock = int(product.get("stock", 0))
        except (ValueError, TypeError, InvalidOperation) as exc:
            raise ValueError(f"Product {sku} has an invalid price or stock") from exc
        yield {
            "sku": sku,
            "name": str(product.get("name", "")),
            "category": str(product.get("category", "")),
            "price": formatted_price,
            "stock": stock,
            "active": "yes" if active else "no",
        }
