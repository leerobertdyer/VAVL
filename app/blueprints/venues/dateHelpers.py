from datetime import datetime
import dateparser


def setShowDateRaw(show, dateContainer):
    try:
        # =========> The Grey Eagle <=========
        if dateContainer["classes"] == "mb-0 eventMonth singleEventDate text-uppercase":
            show_date_raw = show.find(
                dateContainer["container"], class_=dateContainer["classes"]).text.strip()
            return show_date_raw

    # =========> Salvage Station <=========
        if dateContainer["classes"] == "event-list-date-top":
            parent_div = show.find('div', class_='event-list-date-top')
            day = parent_div.find(
                'div', class_='event-list-day').get_text(strip=True)
            month = parent_div.find(
                'div', class_='event-list-month').get_text(strip=True)
            date_number = parent_div.find(
                'div', class_='event-list-number').get_text(strip=True)
            year = parent_div.find(
                'div', class_='event-list-year').get_text(strip=True)
            show_date_raw = f"{day} {month} {date_number} {year}"
            return show_date_raw

    # ==========> The Odd <===========
        elif dateContainer["classes"] == "theOdd":
            show_date_raw = show.find(
                'p').text.split('-')[0].strip()
            return show_date_raw

    # ==========> Everything Else <===========
        else:
            show_date_raw = show.find(
                dateContainer["container"], class_=dateContainer["classes"]).text.strip()
            return show_date_raw
        
    except Exception as e:
        print(f"Error setting show date: {e} for {show}")
        return None


def parse_date(date_str):
    parsed_date = dateparser.parse(date_str)
    if parsed_date:
        return parsed_date
    else:
        print(f"Unable to parse date: {date_str}")
        return None


def find_ticket_link(show, container_id, event_calendar_url):
    # Try finding the container by ID, which could be any tag (div, span, etc.)
    container = show.find(id=container_id) or show.find(class_=container_id)
    if container:
        # Find the first <a> tag within the container
        ticket_link = container.find('a', href=True)
        if ticket_link and ticket_link.has_attr('href'):
            return ticket_link['href']
    # Fallback: Try finding an <a> tag directly by ID
    direct_link = show.find('a', id=container_id) or show.find(
        'a', class_=container_id)
    if direct_link and direct_link.has_attr('href'):
        return direct_link['href']
    # If no link is found
    return event_calendar_url
