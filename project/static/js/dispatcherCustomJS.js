// Creates a red marker with the coffee icon
let markerGroup;

function testAlert() {
    alert ("Hello!")
}

function initialiseMap() {
    markerGroup = L.layerGroup().addTo(map);

}

function addMarker(markerType, colour, latitude, longitude) {

    if (markerType == 'incident') {
        var iconMarker = L.ExtraMarkers.icon({
            icon: 'fa-bell',
            markerColor: colour,
            shape: 'star',
            prefix: 'fa'
        });
    }

    if (markerType == 'response_unit') {
        var iconMarker = L.ExtraMarkers.icon({
            icon: 'fa-car',
            markerColor: colour,
            shape: 'star',
            prefix: 'fas'
        });
    }
    
    var new_marker = L.marker([latitude, longitude], {icon: iconMarker}).addTo(markerGroup);
}

function clearMarkers() {
    map.removeLayer(markerGroup);
    markerGroup = L.layerGroup().addTo(map);

}

function updateCallouts(){
    
    // Clear previous map
    clearMarkers()
    
    // Load new points
    $.getJSON($SCRIPT_ROOT + '/json/callout_data', {}, function(data) {

        $.each(data, function(n, element) {
            addMarker('incident', 'red', element.latitude, element.longitude)
        });

    })
}

function pingURL(urlToPing){

    $.get($SCRIPT_ROOT + urlToPing, function(data) {});

}