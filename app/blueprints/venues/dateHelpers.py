from datetime import datetime

def setShowDateRaw(show, dateContainer, soup):
    if dateContainer["classes"] == "event-list-date-top":
        parent_div = soup.find('div', class_='event-list-date-top')
        day = parent_div.find('div', class_='event-list-day').get_text(strip=True)
        month = parent_div.find('div', class_='event-list-month').get_text(strip=True)
        date_number = parent_div.find('div', class_='event-list-number').get_text(strip=True)
        year = parent_div.find('div', class_='event-list-year').get_text(strip=True)
        show_date_raw = f"{day} {month} {date_number} {year}"
        return show_date_raw
    elif dateContainer["classes"] == "sc-hKgILt sc-jUEnpm gXKGT fmxDzY":
        show_date_raw = show.find(dateContainer["container"], class_=dateContainer["classes"]).text.split('-')[0].strip()
        return show_date_raw  
    else:
        show_date_raw = show.find(dateContainer["container"], class_=dateContainer["classes"]).text.strip()
        return show_date_raw

def check_Event_Year(eventMonth: int):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    if eventMonth <= 3 and currentMonth >= 8:
        return currentYear + 1
    else:
        return currentYear
    
def parse_date(date_str):
        # Remove extra whitespace
    date_str = " ".join(date_str.split())

        # Split the string to ignore the time part if it exists
    date_without_time = date_str.split('@')[0].strip()
    date_formats = ["%B %d", "%b %d", "%a, %b %d", "%a, %b %d %Y", "%a %b %d %Y","%a, %B %d %Y", "%b %d, %Y"]
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_without_time, date_format)
            if "%Y" not in date_format:
                eventYear = check_Event_Year(parsed_date.month)
                return datetime(eventYear, parsed_date.month, parsed_date.day)
            return parsed_date
        except ValueError:
           # Correct 'Sept' to 'Sep' and other similar corrections if needed
            if 'Sept' in date_without_time:
                try:
                    corrected_date_without_time = date_without_time.replace('Sept', 'Sep')
                    return datetime.strptime(corrected_date_without_time, date_format)
                except ValueError:
                    continue
            if 'April' in date_without_time:
                try:
                    corrected_date_without_time = date_without_time.replace('April', 'Apr')
                    return datetime.strptime(corrected_date_without_time, date_format)
                except ValueError:
                    continue
            if 'July' in date_without_time:
                try:
                    corrected_date_without_time = date_without_time.replace('July', 'Jul')
                    return datetime.strptime(corrected_date_without_time, date_format)
                except ValueError:
                    continue
    raise ValueError(f"Date format not supported: {date_without_time}")

def find_ticket_link(show, container_id, event_calendar_url):
    # Try finding the container by ID, which could be any tag (div, span, etc.)
    container = show.find(id=container_id) or show.find(class_=container_id)
    if container:
        # Find the first <a> tag within the container
        ticket_link = container.find('a', href=True)
        if ticket_link and ticket_link.has_attr('href'):
            return ticket_link['href']
    # Fallback: Try finding an <a> tag directly by ID
    direct_link = show.find('a', id=container_id) or show.find('a', class_=container_id)
    if direct_link and direct_link.has_attr('href'):
        return direct_link['href']
    # If no link is found
    return event_calendar_url