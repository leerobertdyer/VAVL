homeURL = window.location.href

//sort handler
let sortedVenues = [];
let startDate = '';
let endDate = '';
document.addEventListener('DOMContentLoaded', () => {
    const venueList = document.querySelectorAll('.venueList');

    venueList.forEach((list) => {
        list.addEventListener('click', () => {
            const targetId = list.getAttribute('data-target');
            const targetVenue = document.getElementById(targetId);
            if (targetVenue.classList.contains('selected')){
                targetVenue.classList.remove('selected');
                const indexToRemove = sortedVenues.indexOf(targetId);
                sortedVenues.splice(indexToRemove, 1);
            } else {
                targetVenue.classList.add('selected');
                sortedVenues.push(targetId);
            }
        });
    });
});

const handleDate = (date) => {
    startDate = date[0];
    if (date.length === 2) {
        endDate = date[1];
    }
}

const submitSort = document.getElementById('submitSort');
submitSort.addEventListener('click', () => fetchSort(sortedVenues));

const fetchSort = (datesVenues) => {
    let params = '';
    for (venue of datesVenues){
        params += "venue=" + venue.replace(/\s+/g, '+') + "&";
    }
    if (startDate.length > 0){
        params += "start=" + startDate + "&";
    } if (endDate.length > 0) {
        params += "end=" + endDate;
    }
    url = `${homeURL}ed?${params}`;
    window.location.href = url;
}


mainDiv = document.getElementById('mainDiv')

