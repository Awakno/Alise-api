import re
from bs4 import BeautifulSoup

from awlise.models.home import Home


def _html_home_parser(html: str) -> dict:
    """
    Parses the HTML content of the home page.

    :param html: The HTML content of the home page.
    :return: A dictionary containing the parsed data.
    """
    user_data = {}
    soup = BeautifulSoup(html, "html.parser")

    # Extracting responsible person's information
    for p in soup.find_all("p"):
        if "responsable" in p.get("class", []):
            responsable = p.text.strip().replace("\xa0", " ")
            user_data["responsable"] = responsable
            parts = responsable.split(" ", 1)
            user_data["responsable_first_name"] = parts[0]
            user_data["responsable_last_name"] = parts[1] if len(parts) > 1 else ""

        if "adresse" in p.get("class", []):
            user_data["adress"] = p.text.strip()

    # Extracting balance
    label = soup.find("label", class_="soldeplus")
    if label:
        balance_tag = label.find("b")
        try:
            if balance_tag and balance_tag.text:
                user_data["balance"] = (float(balance_tag.text.replace(",", ".").replace("€", "")), balance_tag.text[-2])
            else:
                user_data["balance"] = (0.0, "€")
        except ValueError:
            user_data["balance"] = (0.0,"€")  # Default to 0.0 if parsing fails

    # Extracting child information
    select = soup.find("select", class_="eleve")
    if select:
        option = select.find("option", selected=True)
        if option:
            child_name = option.text.strip()
            child_name_cleaned = re.sub(r"\s*\(.*?\)", "", child_name).strip()  # Remove text in parentheses
            parts = child_name_cleaned.split(" ", 1)
            user_data["childs"] = {
                "name": child_name_cleaned,
                "first_name": parts[0],
                "last_name": parts[1] if len(parts) > 1 else "",
            }

    return Home(**user_data)  # Returning dictionary instead of Home object for now
