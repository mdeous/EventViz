var eventIdRegex = /.*([a-f0-9]{24}).*/;
var eventTypeRegex = /.*eventtype-(\w+).*/;

function drawVisualization(data) {
    data.forEach(function (item, index) {
        item['start'] = new Date(Date.parse(item['start']));
    });
    var options = {
        cluster: true,
        groupsChangeable: false,
        showNavigation: true,
        axisOnTop: true
    };
    var timeline = new links.Timeline(document.getElementById('timeline'));
    links.Timeline.addEventListener(timeline.dom.content, "mousewheel", function() {
        setDoubleClickHandler();
    });
    timeline.draw(data, options);
}

function setDoubleClickHandler() {
    $('.timeline-event-box').dblclick(function () {
        var eventClassAttr = $(this).attr('class');
        var eventID = eventIdRegex.exec(eventClassAttr)[1];
        var eventType = eventTypeRegex.exec(eventClassAttr)[1];
        var getEventURL = '/timeline/' + eventType + '/' + eventID;
        $('#' + eventID).modal({remote: getEventURL});
        return true;
    });
}

function initTimeline(eventsData) {
    drawVisualization(eventsData);
    setDoubleClickHandler();
}
