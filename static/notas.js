document.getElementById("event-form").addEventListener("submit", function(e) {
    e.preventDefault();
  
    var eventName = document.getElementById("event-name").value;
    var eventDate = document.getElementById("event-date").value;
    var eventTime = document.getElementById("event-time").value;
  
    var eventCard = document.createElement("div");
    eventCard.className = "event-card";
    eventCard.innerHTML = "<h3>" + eventName + "</h3><p>Data: " + eventDate + "</p><p>Hora: " + eventTime + "</p><button>Delete</button>";
  
    document.getElementById("event-list").appendChild(eventCard);
  
    document.getElementById("event-name").value = "";
    document.getElementById("event-date").value = "";
    document.getElementById("event-time").value = "";
  });
  
  document.getElementById("event-list").addEventListener("click", function(e) {
    if(e.target.tagName === "BUTTON") {
      e.target.parentNode.remove();
    }
  });
  