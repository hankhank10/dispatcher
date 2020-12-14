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

function addMarker(markerType, colour, latitude, longitude) {

    if (markerType == 'callout') {
        var iconMarker = L.ExtraMarkers.icon({
            icon: 'fa-bell',
            markerColor: colour,
            shape: 'star',
            prefix: 'fa'
        });
        var new_marker = L.marker([latitude, longitude], {icon: iconMarker}).addTo(calloutMarkerGroup);
    }

    if (markerType == 'response_unit') {
        var iconMarker = L.ExtraMarkers.icon({
            icon: 'fa-car',
            markerColor: colour,
            shape: 'star',
            prefix: 'fas'
        });
        var new_marker = L.marker([latitude, longitude], {icon: iconMarker}).addTo(responseUnitMarkerGroup);
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
            addMarker('callout', 'red', element.latitude, element.longitude)
        });
    })
}


function pingURL(urlToPing){
    $.get($SCRIPT_ROOT + urlToPing, function(data) {});
}