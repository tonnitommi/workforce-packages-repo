from robocorp.tasks import task

def get_currency_conversion_rates(currencies: list) -> str:
    """Fetches USD conversion rates for a list of currencies."""
    import requests
    import json
    unique_currencies = [c for c in set(currencies) if c.upper() != "USD"]
    if not unique_currencies:
        return json.dumps({})
    base_url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        conversion_rates = {}
        for currency in unique_currencies:
            currency_upper = currency.upper()
            if currency_upper in rates and rates[currency_upper] != 0:
                conversion_rates[currency_upper] = 1.0 / rates[currency_upper]
            else:
                conversion_rates[currency_upper] = 0
        return json.dumps(conversion_rates)
    except Exception:
        return json.dumps({})

@task
def run_task():
    """Auto-generated entrypoint."""
    result = get_currency_conversion_rates(currencies=['EUR', 'GBP', 'JPY', 'USD'])
    if result is not None:
        print(result)
    return result
