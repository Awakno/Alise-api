from bs4 import BeautifulSoup


def _html_payments_parser(html: str) -> dict:
    """
    Parses the HTML content of the payment/billing page.

    :param html: The HTML content of the payment page.
    :return: A dict with the `meal_price` key: a (float, currency_symbol) tuple.
    """
    soup = BeautifulSoup(html, "html.parser")
    credit = soup.find("label", class_="label-credit-lib")
    if credit and credit.contents:
        credit = credit.contents[0]
        credit = credit.split("(")[1]
        credit = credit.replace(",", ".")
        price, currency, _ = credit.split(" ")
        return {"meal_price": (float(price), currency)}
    return {"meal_price": (0.0, "€")}
