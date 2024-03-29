from flask import jsonify
from . import venues
from bs4 import BeautifulSoup
import requests
from ...models import Event
from datetime import datetime
from app import db
from playwright.sync_api import sync_playwright

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

@venues.route('/eagle')
def eagle():
    
    url = "https://www.thegreyeagle.com/calendar/"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    eagleEvents = []
    showYear = ''
    if resp.status_code == 200:
        mainDiv = soup.find("div", class_="rhp-desktop-list")
        for child in mainDiv.children:
            if child.name == "span":
               showYear = child.span.text[-4::].strip()
            elif child.name == "div":
                try:
                    showDay = child.find(id="eventDate").text.strip()
                    showDateStr = showDay + " " + showYear
                    try:
                        showDate = datetime.strptime(showDateStr, "%a, %b %d %Y")
                    except:
                        showDate = datetime.strptime(showDateStr, "%a, %B %d %Y")
                except:
                    showDate = "Date Not Found"
                try:
                    showTitle = child.find(id="eventTitle").find('h2').text
                    print(f'Scraping {showTitle} at grey eagle')
                except:
                    showTitle = "Title not found"
                    
                existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
                if existing_event:
                    print(f'{showTitle} already in db: skipping')
                    continue
                if existing_event is None:
                    try:
                        showImage = child.find("img", class_="eventListImage")['src'] 
                    except:
                        showImage = "app/static/sad.jpg"
                    try:
                        showTickets = child.find(id="eventTitle")["href"]
                    except:
                        showTickets = "Tickets Not Found"
                    eagleEvents.append({
                        "showDate": showDate, 
                        "showTitle": showTitle, 
                        "showImage": showImage, 
                        "showTickets": showTickets})
                    new_event = Event(
                        venue = "Grey Eagle",
                        title = showTitle,
                        show_date = showDate,
                        tickets = showTickets,
                        image = showImage,
                    )
                    db.session.add(new_event)
                    db.session.commit()
    else:
        print(f"Failed to retrieve eagle Page. Status code: {resp.status_code}")
    return eagleEvents

@venues.route('/peel')
def peel():
    url = "https://theorangepeel.net/events/?view=list"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    peelEvents = []
    showYear = ''
    if resp.status_code == 200:
        mainDiv = soup.find("div", class_="rhp-desktop-list")
        for child in mainDiv:
            if child.name == "span":
                showYear = child.span.text[-4::].strip()
                print("SHOW YEAR: ", showYear)
            elif child.name == "div":
                try:
                    print('made it here')
                    showDay = child.find(id="eventDate").text.strip() 
                    showDateStr = showDay + " " + showYear
                    if showDateStr[5:9].upper() == "SEPT" or showDateStr[5:9].upper() == "MARCH" or showDateStr[5:9].upper() == "JUNE" or showDateStr[5:9].upper() == "JULY":
                        showDateStr = showDateStr[0:8] + showDateStr[9::]
                        print('date format off...')
                        print(showDateStr)
                    showDate = datetime.strptime(showDateStr, "%a, %b %d %Y")
                except:
                    showDate = "Date Not Found"
                try:
                    showTitle = child.find(id="eventTitle").find('h2').text.strip()
                    print(f'Scraping {showTitle} at Peel')
                except:
                    showTitle = "Title not found"
                
                existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
                if existing_event:
                    print(f'{showTitle} already in db: skipping')
                    continue
                if existing_event is None:
                    try:
                        showImage = child.find("img", class_="eventListImage")['src'] 
                    except:
                        showImage = "app/static/sad.jpg"
                    try:
                        showTickets = child.find(id="eventTitle")["href"]
                    except:
                        showTickets = "Tickets Not Found"
                    peelEvents.append({
                        "showDate": showDate, 
                        "showTitle": showTitle, 
                        "showImage": showImage, 
                        "showTickets": showTickets})
                    new_event = Event(
                        venue = "Orange Peel",
                        title = showTitle,
                        show_date = showDate,
                        tickets = showTickets,
                        image = showImage,
                    )
                    db.session.add(new_event)
                    db.session.commit()
    else:
        print(f"Failed to retrieve peel Page. Status code: {resp.status_code}")
    return peelEvents

@venues.route('/rabbit')
def rabbit():    
    url = "https://rabbitrabbitavl.com/calendar/"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    rabbitEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="tribe-events-calendar-list__event-row")
        for show in showDivs:
            try:
                currentYear = datetime.now().year
                # print('wtf wtf wtf wtf1: ', currentYear)
                dateAndTime = show.find("span", class_="tribe-event-date-start").text 
                # print('wtf wtf wtf wtf2: ', dateAndTime)
                showDateStrData = dateAndTime[:-9].strip()
                # print('wtf wtf wtf wtf3: ', showDateStrData)
                showDateStr = showDateStrData + " " + str(currentYear)
                # print('rabbit rabbit date: ', showDateStr)
                try:
                    showDate = datetime.strptime(showDateStr, "%B %d %Y")
                except ValueError:
                    try:
                        showDate = datetime.strptime(showDateStr, "%b %d %Y" )
                    except ValueError:
                        showDate = "Date/time Not Found"

            except Exception as e:
                print(f"An error occurred: {e}")
                # showDate = datetime.now()
            try:
                showTitle = show.find("h3", class_="tribe-events-calendar-list__event-title").find("a")['title']
                print(f'{showTitle} at Rabbit')
            except:
                showTitle = "Title not found"
            existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
            if existing_event:
                print(f'{showTitle} already in db: skipping')
                continue
            if existing_event is None:
                try:
                    showImage = show.find("img", class_="tribe-events-calendar-list__event-featured-image")['src'] 
                except:
                    showImage = "app/static/sad.jpg"
                try:
                    showTickets = show.find("h3", class_="tribe-events-calendar-list__event-title").find("a")['href']
                except:
                    showTickets = "Tickets Not Found"
                rabbitEvents.append({
                    "showDate": showDate, 
                    "showTitle": showTitle, 
                    "showImage": showImage, 
                    "showTickets": showTickets})
                new_event = Event(
                    venue = "Rabbit Rabbit",
                    title = showTitle,
                    show_date = showDate,
                    tickets = showTickets,
                    image = showImage
                )
                db.session.add(new_event)
                db.session.commit()
    else:
        print(f"Failed to retrieve Rabbit Page. Status code: {resp.status_code}")
    return rabbitEvents

@venues.route('/cherokee')
def cherokee():
    url = 'https://www.harrahscherokeecenterasheville.com/events-tickets/'
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    cherokeeEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="list-view")
        for show in showDivs:
            try:
                showDay = show.find("div", class_="event-date").text.strip()
                if len(showDay) < 5:
                    alternateDate = show.find("div", class_="event-subtitle").text.strip()
                    for char in alternateDate:
                        if char.isdigit():
                            showDay += " " + char
                            break
                showDate = showDay + " 2024"    
            except:
                showDate = "Date Not Found"
            try:
                showTitle = show.find("div", class_="event-details").find("h3").text
                print(f'scraping {showTitle} at Cherokee')
            except:
                showTitle = "Title not found"
            existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
            if existing_event:
                print(f'{showTitle} already in db: skipping')
                continue
            if existing_event is None:
                try:
                    showImage = show.find("div", class_="image-wrapper").find("img")['src'] 
                except:
                    showImage = "app/static/sad.jpg"
                try:
                    showTickets = show.find("a", class_="event-ticket")['href']
                except:
                    showTickets = "Tickets Not Found"
                cherokeeEvents.append({
                    "showDate": showDate, 
                    "showTitle": showTitle, 
                    "showImage": showImage, 
                    "showTickets": showTickets})
                new_event = Event(
                    venue = "Harrah's Cherokee",
                    title = showTitle,
                    show_date = showDate,
                    tickets = showTickets,
                    image = showImage
                )
                db.session.add(new_event)
                db.session.commit()
    else:
        print(f"Failed to retrieve cherokee page. Status code: {resp.status_code}")
    return cherokeeEvents
    
@venues.route('/salvage')
def salvage():
    url = 'https://salvagestation.com/events/'
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    salvageEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="event-list-wrapper")
        for show in showDivs:
            try:
                showDay = show.find("div", class_="event-list-day").text.strip()
                showMonth = show.find("div", class_="event-list-month").text.strip()
                showNum = show.find("div", class_="event-list-number").text.strip()
                showYear = show.find("div", class_="event-list-year").text.strip()
                showDateStr = f"{showDay} {showMonth} {showNum} {showYear}"
                showDate = datetime.strptime(showDateStr, "%a %b %d %Y")
            except:
                showDate = "Date/time Not Found"
            try:
                showTitle = show.find("div", class_="event-list-title").text.strip()
                print(f'Scraping {showTitle} from salvage')
            except:
                showTitle = "Title not found"
            existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
            if existing_event:
                print(f'{showTitle} already in db: skipping')
                continue
            if existing_event is None:
                try:
                    showImage = show.find("a", class_="event-list-image")["style"][23:-3]
                except:
                    showImage = "app/static/sad.jpg"
                try:
                    showTickets = show.find("div", class_="event-list-titles").find("a")["href"]
                except:
                    showTickets = "Tickets Not Found"
                salvageEvents.append({
                    "showDate": showDate, 
                    "showTitle": showTitle, 
                    "showImage": showImage, 
                    "showTickets": showTickets})
                new_event = Event(
                    venue = "Salvage Station",
                    title = showTitle,
                    show_date = showDate,
                    tickets = showTickets,
                    image = showImage
                )
                db.session.add(new_event)
                db.session.commit()
    else:
        print(f"Failed to retrieve salvage page. Status code: {resp.status_code}")
    return salvageEvents


# @venues.route('/eulogy')
# def eulogy():
#     url = 'https://burialbeer.com/pages/eulogy'
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)  
#         page = browser.new_page() 

#         page.goto(url)
#         page.wait_for_selector(".dice_events")  

#         if "404" in page.title():
#             browser.close()
#             return "Euology not found", 404

#         page_source = page.content()  
#         soup = BeautifulSoup(page_source, 'html.parser')
    
#     eulogyEvents = []
    
#     showDivs = soup.find_all('article', class_='sc-iHbSHJ fCPdMs')
#     for show in showDivs:
#         try:
#             showDateData = show.find("time", class_="sc-klVQfs").text[:11].strip()
#             if showDateData[-1] == "―":
#                 showDateData = showDateData[:-2]
#             showDateData += " 2024"
#             showDate = datetime.strptime(showDateData, "%a %d %b %Y") 
#         except:
#             showDate = "Date/time Not Found"
#         try:
#             showTitle = show.find("a", class_="dice_event-title").text.strip()
#             print(f'Scraping {showTitle} from Eulogy')
#         except:
#             showTitle = "Title not found"
#         existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
#         if existing_event:
#             print(f'{showTitle} already in db: skipping')
#             continue
#         if existing_event is None:
#             try:
#                 showImageElement = show.find("img", class_="sc-fxwrCY gPoyuC")
#                 showImage = showImageElement.get('src')
#             except:
#                 showImage = "app/static/sad.jpg"
#             try:
#                 showTickets = show.find("a", class_="sc-kdBSHD dougVq dice_book-now")['href']
#             except:
#                 showTickets = "Tickets Not Found"
#             eulogyEvents.append({
#                 "showDate": showDate, 
#                 "showTitle": showTitle, 
#                 "showImage": showImage, 
#                 "showTickets": showTickets})
#             new_event = Event(
#                 venue = "Eulogy",
#                 title = showTitle,
#                 show_date = showDate,
#                 tickets = showTickets,
#                 image = showImage
#             )
#             db.session.add(new_event)
#             db.session.commit()
#     return eulogyEvents

# @venues.route('/fleetwoods')
# def fleetwoods():
    url = 'https://fleetwoodschapel.com/calendar-of-events/'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page() 

        page.goto(url)
        page.wait_for_selector(".section-inner")  

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
        page = browser.new_page() 

        page.goto(iframe_src)
        # page.wait_for_selector(".section-inner")

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
        existing_event = Event.query.filter_by(title=showTitle, show_date=showDate).first()
        if existing_event:
            print(f'{showTitle} already in db: skipping')
            continue
        if existing_event is None:
            try:
                showImage = show.find('img')["style"][22:-2]
            except:
                showImage = "app/static/sad.jpg"
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
    
    
    