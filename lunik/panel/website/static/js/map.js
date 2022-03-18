
$(function () {
    var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        placeholder: 'Buscar',
        bbox: [-125.04773013010984, 13.362371876574812, -67.17510327073529, 49.341030255796454]
    });

    map.addControl(geocoder);
    // Add zoom and rotation controls to the map.
    map.addControl(new mapboxgl.NavigationControl());
    map.on('click', addMarker);
    map.on('mouseup', setLngLatInputs);

    geocoder.on('result', function (ev) {
        marker.setLngLat(ev.result.center);
        setLngLatInputs();
    });

    function addMarker(e) {
        marker.setLngLat(e.lngLat);
        setLngLatInputs();
    }

    function setLngLatInputs() {
        var lngLat = marker.getLngLat();
        var url = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + lngLat.lng + "," + lngLat.lat + ".json?access_token=" + mapboxgl.accessToken;
        $.get(url, function (data) {
            var address = data.features[0].place_name;
            // City
            var city = data.features[0].context[1].text
            // State
            var state = data.features[0].context[2].text
            // Country
            // console.log(data.features[0].context[3].text)
            $("input[name=address]").val(address);
            $("input[name=city]").val(city);
            $("input[name=state]").val(state);
            
        });
        $("input[name=latitude]").val(lngLat.lat);
        $("input[name=longitude]").val(lngLat.lng);
    }
});