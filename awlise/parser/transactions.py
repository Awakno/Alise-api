from bs4 import BeautifulSoup
from awlise.models.transactions import Transaction


def _html_transactions_parser(html: str) -> list[Transaction]:
    """
    Parses the HTML content of the financial transactions page.

    :param html: The HTML content of the transactions page.
    :return: A list of Transaction objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr", class_="detail")
    transactions = []
    for row in rows:
        date = row.find("td", class_="detail_date").get_text(strip=True)
        description = row.find("td", class_="detail_data").get_text(strip=True)
        debit = row.find("td", class_="detail_debit_montant").get_text(strip=True) or None
        credit = row.find("td", class_="detail_credit_montant").get_text(strip=True) or None

        debit = float(debit.replace(",", ".")) if debit else None
        credit = float(credit.replace(",", ".")) if credit else None
        transactions.append(Transaction(date=date, description=description, debit=debit, credit=credit))

    return transactions
