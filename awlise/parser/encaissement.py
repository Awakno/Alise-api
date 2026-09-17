from bs4 import BeautifulSoup

def _html_encaissement_parser(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    credit = soup.find("label", class_="label-credit-lib")
    print("Credit", )
    credit = credit.contents[0]
    if credit:
        print(credit)
        credit = credit.split("(")[1]
        credit = credit.replace(",", ".")
        price, device, _ = credit.split(" ")
        return {"booking_price": (float(price), device) }
    return {"booking_price": (0.0, '€')}





