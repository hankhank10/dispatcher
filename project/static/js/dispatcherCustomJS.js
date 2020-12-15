// Creates a red marker with the coffee icon
let calloutMarkerGroup;
let responseUnitMarkerGroup;

function testAlert() {
    alert ("Hello!")
}

function initialiseMap() {
    calloutMarkerGroup = L.layerGroup().addTo(map);
    responseUnitMarkerGroup = L.layerGroup().addTo(map);

}

function addMarker(latitude, longitude, markerType, colour, iconText, tooltip) {

    if (markerType == 'callout') {
        var iconMarker = L.ExtraMarkers.icon({
            icon: 'fa-number',
            number: iconText,
            markerColor: colour,
            shape: 'star',
            prefix: 'fa'
        });
        var new_marker = L.marker([latitude, longitude], {icon: iconMarker}).bindPopup(tooltip).addTo(calloutMarkerGroup);
    }

    if (markerType == 'response_unit') {
        var iconMarker = L.ExtraMarkers.icon({
            icon: 'fa-number',
            markerColor: colour,
            number: iconText,
            shape: 'circle',
            prefix: 'fa'
        });
        var new_marker = L.marker([latitude, longitude], {icon: iconMarker}).bindPopup(tooltip).addTo(responseUnitMarkerGroup);
    }
}


function clearMarkers(markerType) {
    
    if (markerType == 'callout') {
        map.removeLayer(calloutMarkerGroup);
        calloutMarkerGroup = L.layerGroup().addTo(map);
    }

    if (markerType == 'response_unit') {
        map.removeLayer(responseUnitMarkerGroup);
        responseUnitMarkerGroup = L.layerGroup().addTo(map);
    }

    if (markerType == 'all') {
        clearMarkers('callout');
        clearMarkers('response_unit');
    }

}


function updateCallouts(){
    
    // Clear previous map layer
    clearMarkers('callout');
    
    // Load new points
    $.getJSON($SCRIPT_ROOT + '/json/callout_data', {}, function(data) {
        $.each(data, function(n, element) {
            addMarker(element.latitude, element.longitude, 'callout', 'red', 2, 'test tooltip')
        });
    })
}


function pingURL(urlToPing){
    $.get($SCRIPT_ROOT + urlToPing, function(data) {});
}