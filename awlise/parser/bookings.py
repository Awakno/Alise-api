from bs4 import BeautifulSoup


def _html_booking_parser(html: str) -> list:
    """
    Parses the HTML content of the booking page.

    :param html: The HTML content of the booking page.
    :return: A list of dictionaries containing the parsed data.
    """
    soup = BeautifulSoup(html, "html.parser")
    bookings = []

    # Find all calendar cells with booking information
    for cell in soup.find_all("td", id=True):
        date_id = cell.get("id")

        if date_id:
            # Check if the cell contains a booking link
            booking_link = cell.find("a", href=True)
            if booking_link:
                bookings.append({
                    "status": "reserved" if "aliReservationCancel.php" in booking_link["href"] else "available",
                    "cancelable": True,
                    "link": booking_link["href"],
                    "date": date_id,
                    "identifier": booking_link["href"].split("date=")[1]
                })
            else:
                # Check if the cell is marked as non-reservable
                if "E8E8E8" in cell.get("bgcolor", ""):
                    bookings.append({"date": date_id, "status": "non-reservable"})
                if "FDFFFF" in cell.get("bgcolor", ""):
                    bookings.append({"date": date_id, "status": "non-reservable"})
    return bookings
