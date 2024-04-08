const homeURL = window.location.href;

// Pagination
currentPage = 2;
const eventContainer = document.querySelector(".eventsDiv");
document.addEventListener("scroll", async () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
    currentPage += 1;
    const response = await fetch(`${homeURL}/next-events?page=${currentPage}`);
    const data = await response.json();
    console.log(data);
    for (const event of data.events) {
      if (event.newDate) {
        const dateHeader = document.createElement("h1");
        dateHeader.className = "dateHeader";
        dateHeader.textContent = event.newDate;
        eventContainer.appendChild(dateHeader);
      } else if (event.venue) {
        const eventDiv = document.createElement("div");
        eventDiv.className = "blackBorder";
        eventContainer.appendChild(eventDiv);

        const eventLink = document.createElement("a");
        eventLink.href = event.tickets;
        eventLink.classList = getVenueClass(event.venue) + " eventLink";
        eventLink.style.backgroundImage = `url(${event.image})`;
        eventLink.style.backgroundSize = "cover";

        const eventVenue = document.createElement("h2");
        eventVenue.textContent = event.venue;
        eventLink.appendChild(eventVenue);

        const eventTitle = document.createElement("h3");
        eventTitle.textContent = event.title;
        eventLink.appendChild(eventTitle);

        eventDiv.appendChild(eventLink);
      }
    }
  }
});

function getVenueClass(venue) {
  switch (venue) {
    case "Grey Eagle":
      return "eagle";
    case "Orange Peel":
      return "peel";
    case "Rabbit Rabbit":
      return "rabbit";
    case "Salvage Station":
      return "salvage";
    case "Harrah's Cherokee":
      return "cherokee";
    default:
      return "";
  }
}

//sort handler
let sortedVenues = [];
let startDate = "";
let endDate = "";
document.addEventListener("DOMContentLoaded", () => {
  const venueList = document.querySelectorAll(".venueList");

  venueList.forEach((list) => {
    list.addEventListener("click", () => {
      const targetId = list.getAttribute("data-target");
      const targetVenue = document.getElementById(targetId);
      if (targetVenue.classList.contains("selected")) {
        targetVenue.classList.remove("selected");
        const indexToRemove = sortedVenues.indexOf(targetId);
        sortedVenues.splice(indexToRemove, 1);
      } else {
        targetVenue.classList.add("selected");
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
};

const submitSort = document.getElementById("submitSort");
submitSort.addEventListener("click", () => fetchSort(sortedVenues));

const fetchSort = (datesVenues) => {
  let params = "";
  for (venue of datesVenues) {
    params += "venue=" + venue.replace(/\s+/g, "+") + "&";
  }
  if (startDate.length > 0) {
    params += "start=" + startDate + "&";
  }
  if (endDate.length > 0) {
    params += "end=" + endDate;
  }
  url = `${homeURL}ed?${params}`;
  window.location.href = url;
};
