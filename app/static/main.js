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


//sort handler
let sortedVenues = []
document.addEventListener('DOMContentLoaded', () => {
    const venueList = document.querySelectorAll('.venueList');

    venueList.forEach((list) => {
        list.addEventListener('click', () => {
            const targetId = list.getAttribute('data-target');
            const targetVenue = document.getElementById(targetId);
            if (targetVenue.classList.contains('selected')){
                targetVenue.classList.remove('selected')
                const indexToRemove = sortedVenues.indexOf(targetId);
                sortedVenues.splice(indexToRemove, 1)
            } else {
                targetVenue.classList.add('selected')
                sortedVenues.push(targetId)
            }
        });
    });
});

const submitSort = document.getElementById('submitSort');
submitSort.addEventListener('click', () => fetchSort(sortedVenues))

const fetchSort = (datesVenues) => {
    let params = ''
    for (venue of datesVenues){
        params += "venue=" + venue.replace(/\s+/g, '+') + "&"
    }
    url = `http://127.0.0.1:5000/sorted?${params}`
    window.location.href = url

}


mainDiv = document.getElementById('mainDiv')

