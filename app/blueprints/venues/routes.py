from . import venues
from bs4 import BeautifulSoup
from ...models import Event
from datetime import datetime
from app import db
from playwright.sync_api import sync_playwright
from .imageHelpers import save_temp_image, download_image, upload_to_supabase, get_supabase_image_url
from .beautifulScraper import beautifulScraper, headers

@venues.route('/eagle')
def eagle():
    eventContainer={"container": "div", "classes": "col-12 eventWrapper rhpSingleEvent py-4 px-0"}
    dateContainer={"container": "div", "classes": "mb-0 eventMonth singleEventDate text-uppercase"}
    titleContainer={"container": "h2", "classes": "font1by25 font1By5remMD marginBottom3PX lineHeight12 font1By75RemSM font1By5RemXS mt-md-0 mb-md-2"}
    imageContainer={"container": "img", "classes": "eventListImage", "attribute": "src"}
    ticketContainerIdOrClass = "eventTitle"
    eagleEvents = beautifulScraper("https://www.thegreyeagle.com/calendar/", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Grey Eagle")
    return eagleEvents

@venues.route('/peel') 
def peel():
    eventContainer={"container": "div", "classes": "col-12 eventWrapper rhpSingleEvent py-4 px-0"}
    dateContainer={"container": "div", "classes": "mb-0 eventMonth singleEventDate text-uppercase"}
    titleContainer={"container": "h2", "classes": "font1by25 font1By5remMD marginBottom3PX lineHeight12 font1By75RemSM font1By5RemXS mt-md-0 mb-md-2"}
    imageContainer={"container": "img", "classes": "eventListImage", "attribute": "src"}
    ticketContainerIdOrClass = "ctaspan-97828"
    peelEvents = beautifulScraper("https://theorangepeel.net/events/?view=list", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Orange Peel")
    return peelEvents

@venues.route('/rabbit')
def rabbit():    
    eventContainer={"container": "div", "classes": "tribe-common-g-row tribe-events-calendar-list__event-row tribe-events-calendar-list__event-row--featured"}
    dateContainer={"container": "span", "classes": "tribe-event-date-start"}
    titleContainer={"container": "h3", "classes": "tribe-events-calendar-list__event-title"}
    imageContainer={"container": "img", "classes": "tribe-events-calendar-list__event-featured-image", "attribute": "src"}
    ticketContainerIdOrClass = "tribe-events-calendar-list__event-title"
    rabbitEvents = beautifulScraper("https://rabbitrabbitavl.com/calendar/", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Rabbit Rabbit")
    return rabbitEvents

@venues.route('/cherokee')
def cherokee():
    eventContainer={"container": "div", "classes": "col col-lg-4 list-view"}
    dateContainer={"container": "div", "classes": "h1"}
    titleContainer={"container": "h3", "classes": ""}
    imageContainer={"container": "source", "classes": "", "attribute": "srcset"}
    ticketContainerIdOrClass = "event-ticket"
    cherokeeEvents = beautifulScraper("https://www.harrahscherokeecenterasheville.com/events-tickets/", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Harrah's Cherokee")
    return cherokeeEvents
    
@venues.route('/salvage')
def salvage():
    eventContainer={"container": "div", "classes": "event-list-wrapper"}
    dateContainer={"container": "div", "classes": "event-list-date-top"}
    titleContainer={"container": "div", "classes": "event-list-title"}
    imageContainer={"container": "a", "classes": "event-list-image", "attribute": "style"}
    ticketContainerIdOrClass = "event-list-button buy"
    salvageEvents = beautifulScraper("https://salvagestation.com/events/", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Salvage Station")
    return salvageEvents

@venues.route('/staticage')
def staticage():
    eventContainer={"container": "a", "classes": "border-x-0 border-b-2 last-of-type:border-b-0 border-background-200 p-3 false"}
    dateContainer={"container": "span", "classes": ""}
    titleContainer={"container": "h2", "classes": "text-md md:text-2xl flex-2"}
    imageContainer={"container": "img", "classes": "object-cover", "attribute": "srcset"}
    ticketContainerIdOrClass = "border-x-0 border-b-2 last-of-type:border-b-0 border-background-200 p-3 false"
    staticageEvents = beautifulScraper("https://www.staticagenc.com/events", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Static Age")
    return staticageEvents

@venues.route('/musichall')
def musicHall():
    eventContainer={"container": "article", "classes": "wfea-grid_event post status-live free city-asheville region-nc country-us event__public event__available"}
    dateContainer={"container": "time", "classes": "eaw-time published"}
    titleContainer={"container": "h4", "classes": "wfea-header__title entry-title"}
    imageContainer={"container": "img", "classes": "wp-post-image", "attribute": "src"}
    ticketContainerIdOrClass = "wfea-popup-booknow-6614b5130f0dc-878519905687"
    musicHallEvents = beautifulScraper("https://www.ashevillemusichall.com/all-shows/", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Asheville Music-Hall")
    return musicHallEvents

@venues.route('/odd')
def odd():
    eventContainer={"container": "div", "classes": "sc-bdfBwQ pkAuV"}
    dateContainer={"container": "p", "classes": "theOdd"}
    titleContainer={"container": "p", "classes": "theOdd"}
    imageContainer={"container": "img", "classes": "theOdd", "attribute": "src"}
    ticketContainerIdOrClass = "theOdd"
    oddEvents = beautifulScraper("https://linktr.ee/theoddavl", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "The Odditorium")
    return oddEvents

@venues.route('/eulogy')
def eulogy():
    url = 'https://burialbeer.com/pages/eulogy'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=headers['User-Agent'])    
        page = context.new_page() 
        page.goto(url, timeout=60000)
        ageVerificationBtn = 'button[name="confirm-age"]'

        if page.is_visible(ageVerificationBtn):
            page.click(ageVerificationBtn)
            
        # page.screenshot(path="debug_screenshot.png")
        page.wait_for_selector(".dice_event-listing-container", timeout=60000)  

        if "404" in page.title():
            browser.close()
            return "Euology not found", 404

        page_source = page.content()  
        soup = BeautifulSoup(page_source, 'html.parser')
    
    eulogyEvents = []
    
    showDivs = soup.find_all('article', class_='sc-olbas cuPXhY')
    for show in showDivs:
        try:
            showDateData = show.find("time").text[:11].strip()
            if showDateData[-1] == "―":
                showDateData = showDateData[:-2]
            showDateData += " 2024"
            showDate = datetime.strptime(showDateData, "%a %d %b %Y") 
        except:
            showDate = "Date/time Not Found"
        try:
            showTitle = show.find("a", class_="dice_event-title").text.strip()
            print(f'Scraping {showTitle} from Eulogy')
        except:
            showTitle = "Title not found"
        if showDate != "Date/time Not Found":
            existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
            if existing_event:
                print(f'{showTitle} already in db: skipping')
                return eulogyEvents
            if existing_event is None:
                try:
                    showImageElement = show.find("img")
                    original_image_url = showImageElement.get('src')
                    image_data = download_image(original_image_url)
                    if image_data:
                        temp_file_path = save_temp_image(image_data)
                        if temp_file_path:
                            file_path = 'peel/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'
                            upload_response = upload_to_supabase(temp_file_path, file_path)
                            if upload_response:
                                showImage = get_supabase_image_url(file_path)
                            else:
                                showImage = "app/static/sad.jpg"
                except Exception as e:
                    print(f"An error occurred in processing {showTitle}: {e}")
                try:
                    showTickets = show.find("a")['href']
                except:
                    showTickets = "Tickets Not Found"
                eulogyEvents.append({
                    "showDate": showDate, 
                    "showTitle": showTitle, 
                    "showImage": showImage, 
                    "showTickets": showTickets})
                new_event = Event(
                    venue = "Eulogy",
                    title = showTitle,
                    show_date = showDate,
                    tickets = showTickets,
                    image = showImage
                )
                db.session.add(new_event)
                db.session.commit()
    return eulogyEvents

@venues.route('/fleetwoods')
def fleetwoods():
    url = 'https://fleetwoodschapel.com/calendar-of-events/'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        context = browser.new_context(user_agent=headers['User-Agent'])    
        page = context.new_page() 

        page.goto(url, timeout=240000)
        page.wait_for_selector("#showslinger-widget-container-47077")  

        if "404" in page.title():
            browser.close()
            return "Euology not found", 404
        
        page_source = page.content()  
        soup = BeautifulSoup(page_source, 'html.parser')

    fleetwoodsEvents = []
    
    divOne = soup.find('div', class_="content clear fleft")
    divTwo = divOne.find('article', id="post-390")
    divThree = divTwo.find('div', class_="post-content clear")
    divFour = divThree.find('div', id="showslinger-widget-container-47077")
    iframe_src = divFour.find('iframe')["src"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        context = browser.new_context(user_agent=headers['User-Agent'])    
        page = context.new_page() 

        page.goto(iframe_src)
        page.wait_for_selector(".container-l")

        if "404" in page.title():
            browser.close()
            return "Euology not found", 404

        page_source = page.content()  
        newSoup = BeautifulSoup(page_source, 'html.parser') 
    
    newDiv1 = newSoup.find('div', id="container-widget")

    showDivs = newDiv1.find_all('div', class_='w-tick-item col-3 rel')
    for show in showDivs:
        try:
            showDateData = show.find("p", class_="text-color").text[:11].strip()
            if showDateData[-1] == ",":
                showDateData = showDateData[:-2]
            showDateData += " 2024"
            showDate = datetime.strptime(showDateData, "%a, %b %d %Y") 
        except Exception as e:
            print('Error:', e)
            showDate = "Date/time Not Found"
        try:
            showTitle = show.find("h2", class_="text-color").text.strip()
            print(f'Scraping {showTitle} from Fleetwoods')
        except:
            showTitle = "Title not found"
        if showDate != "Date/time Not Found":
            existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
            if existing_event:
                print(f'{showTitle} already in db: skipping')
                return fleetwoodsEvents
            if existing_event is None:
                try:
                    original_image_url = show.find('img')["style"][22:-2]
                    image_data = download_image(original_image_url)
                    if image_data:
                        temp_file_path = save_temp_image(image_data)
                        if temp_file_path:
                            file_path = 'fleetwoods/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'
                            upload_response = upload_to_supabase(temp_file_path, file_path)
                            if upload_response:
                                showImage = get_supabase_image_url(file_path)
                            else:
                                showImage = "app/static/sad.jpg"
                except Exception as e:
                    print(f"An error occurred in processing {showTitle}: {e}")
                try:
                    secondHalfOfLink = show.find("a")['href']
                    showTickets = 'https://app.showslinger.com' + secondHalfOfLink
                except:
                    showTickets = "Tickets Not Found"
                fleetwoodsEvents.append({
                    "showDate": showDate, 
                    "showTitle": showTitle, 
                    "showImage": showImage, 
                    "showTickets": showTickets})
                new_event = Event(
                    venue = "Fleetwoods",
                    title = showTitle,
                    show_date = showDate,
                    tickets = showTickets,
                    image = showImage
                )
                db.session.add(new_event)
                db.session.commit()
    return fleetwoodsEvents
    
