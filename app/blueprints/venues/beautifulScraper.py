
from bs4 import BeautifulSoup
import requests
from ...models import Event
from datetime import datetime
from app import db
from .imageHelpers import download_image, save_temp_image, upload_to_supabase, get_supabase_image_url
from .dateHelpers import parse_date, find_ticket_link, setShowDateRaw
import traceback

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

def beautifulScraper(url, eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, venueName):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    venueEvents = []
    if resp.status_code == 200:
        try:
            allShows = soup.find_all(eventContainer["container"], eventContainer["classes"])
            print(f"Found {len(allShows)} shows to process.")

            for show in allShows:
                show_date_raw = setShowDateRaw(show, dateContainer, soup)
                try:
                    show_date = parse_date(show_date_raw)
                except ValueError as e:
                    print(f"Error parsing date: {e}")
                    continue
                if titleContainer["classes"] == "sc-hKgILt sc-jUEnpm gXKGT fmxDzY": 
                    # the odd special case
                    show_title_parts = show.find(name=titleContainer["container"], class_=titleContainer["classes"]).text.split('-')[1:]
                    show_title = ' '.join(show_title_parts).strip()
                else:
                    show_title = show.find(name=titleContainer["container"], class_=titleContainer["classes"]).text.strip()
                if 'ORANGE PEEL EVENTS & ASHEVILLE BREWING PRESENTS' in show_title:
                    show_title = show_title.replace('ORANGE PEEL EVENTS & ASHEVILLE BREWING PRESENTS', '').strip()
                existing_event = Event.query.filter_by(title=show_title, show_date=show_date).first()
                if existing_event:
                    print(f'{show_title} already in db: skipping')
                    # return venueEvents 
                    continue # replace when done testing with above line
                if existing_event is None:
                    try:
                        original_image_url = show.find(imageContainer["container"], class_=imageContainer["classes"])[imageContainer["attribute"]]
                        if imageContainer["attribute"] == "style":
                            original_image_url = original_image_url[23:-3]
                        if imageContainer["attribute"] == "srcset":
                            original_image_url = original_image_url.split('?')[0]
                        image_data = download_image(original_image_url)
                        if image_data is None:
                            show_image = 'https://www.ashevenue.com/static/images/sad.jpeg'
                        if image_data:
                            temp_file_path = save_temp_image(image_data)
                            if temp_file_path:
                                split_name = venueName.split(' ')
                                venueNickName = split_name[1].lower() if len(split_name) > 1 else split_name[0].lower()
                                file_path = f'/{venueNickName}/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'
                                upload_response = upload_to_supabase(temp_file_path, file_path)
                                if upload_response:
                                    show_image = get_supabase_image_url(file_path)
                                else:
                                    show_image = "https://www.ashevenue.com/static/images/sad.jpeg"
                        show_tickets = find_ticket_link(show, ticketContainerIdOrClass, url)
                        venueEvents.append({
                            "showDate": show_date, 
                            "showTitle": show_title, 
                            "showImage": show_image, 
                            "showTickets": show_tickets})
                        new_event = Event(
                            venue = venueName,
                            title = show_title,
                            show_date = show_date,
                            tickets = show_tickets,
                            image = show_image,
                        )
                        db.session.add(new_event)
                        db.session.commit()
                    except Exception as e:
                        print(f"An error occurred in processing {show_title}: {e}")     
        except Exception as e:
            print(f'Error scraping {venueName}: {e}')
            traceback.print_exc()
    return venueEvents