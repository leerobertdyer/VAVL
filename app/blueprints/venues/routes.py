from . import venues
from .beautifulScraper import beautifulScraper, headers, playwrightScraper

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
    eventContainer={"container": "article", "classes": ""}
    dateContainer={"container": "time", "classes": ""}
    titleContainer={"container": "a", "classes": "dice_event-title"}
    imageContainer={"container": "img", "classes": "", "attribute": "src"}
    ticketContainerIdOrClass = "a"
    eulogyEvents = playwrightScraper("https://burialbeer.com/pages/eulogy", ".dice_event-listing-container", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Eulogy")
    return eulogyEvents 

@venues.route('/fleetwoods')
def fleetwoods():
    eventContainer={"container": "div", "classes": "w-tick-item col-3 rel"}
    dateContainer={"container": "p", "classes": "text-color"}
    titleContainer={"container": "h2", "classes": "text-color"}
    imageContainer={"container": "img", "classes": "", "attribute": "style"}
    ticketContainerIdOrClass = "a"
    fleetwoodsEvents = playwrightScraper("https://fleetwoodschapel.com/calendar-of-events/", "#showslinger-widget-container-47077", eventContainer, dateContainer, titleContainer, imageContainer, ticketContainerIdOrClass, "Fleetwoods")
    return fleetwoodsEvents
