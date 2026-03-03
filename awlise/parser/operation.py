from bs4 import BeautifulSoup
from awlise.models.operation import Operation


def _html_operation_parser(html: str):
    """
    Parses the HTML of an operation.

    :param html: The HTML of the operation.
    :return: A list of Operation objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr", class_="detail")
    operations = []
    for row in rows:
        date = row.find("td", class_="detail_date").get_text(strip=True)
        description = row.find("td", class_="detail_data").get_text(strip=True)
        debit = row.find("td", class_="detail_debit_montant").get_text(strip=True) or None
        credit = row.find("td", class_="detail_credit_montant").get_text(strip=True) or None

        # Convert debit and credit to float if they are not None
        debit = float(debit.replace(",", ".")) if debit else None
        credit = float(credit.replace(",", ".")) if credit else None
        operations.append(Operation(date=date, description=description, debit=debit, credit=credit))

    return operations
