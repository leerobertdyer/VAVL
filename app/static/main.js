const getEvents = async () => {
    allEvents = {};

    const eagleResp = await fetch('http://127.0.0.1:5000/eagle');
    const eagleData = await eagleResp.json();
    allEvents.eagle = eagleData;

    const peelResp = await fetch('http://127.0.0.1:5000/peel');
    const peelData = await peelResp.json();
    allEvents.peel = peelData;

    const salvageResp = await fetch('http://127.0.0.1:5000/salvage');
    const salvageData = await salvageResp.json();
    allEvents.salvage = salvageData;

    const rabbitResp = await fetch('http://127.0.0.1:5000/rabbit');
    const rabbitData = await rabbitResp.json();
    allEvents.rabbit = rabbitData;

    const cherokeeResp = await fetch('http://127.0.0.1:5000/cherokee');
    const cherokeeData = await cherokeeResp.json();
    allEvents.cherokee = cherokeeData;

    console.log(allEvents);
    appendData(allEvents);
}

const appendData = (eventsByVenue) => {
    Object.keys(eventsByVenue).forEach(key => {
        const venue = eventsByVenue[key]
        for (const e of venue) {
            const eventLink = document.createElement('a');
            const eventTitle = document.createElement('h2');
            const eventDate = document.createElement('h3');
            const eventTime = document.createElement('h4');
            const eventCost = document.createElement('h5');

            eventLink.href = e.showTickets
            eventLink.style.backgroundImage = `url(${e.showImage})`;

            eventTitle.textContent = e.showTitle;
            eventDate.textContent = e.showDate;
            eventTime.textContent = e.showTime;
            eventCost.textContent = e.showCost;

            eventLink.classList.add('eventLink');
            eventLink.append(eventTitle, eventDate, eventTime, eventCost)
            mainDiv.append(eventLink)
        }
    })

}

mainDiv = document.getElementById('mainDiv')
showBtn = document.getElementById('showBtn');
