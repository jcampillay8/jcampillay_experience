function initialize() {
    // Crear un array de estilos.
    var styles = [
      {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [
          {
            "color": "#444444"
          }
        ]
      },
      {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
          {
            "color": "#f2f2f2"
          }
        ]
      },
      {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [
          {
            "visibility": "off"
          }
        ]
      },
      {
        "featureType": "road",
        "elementType": "all",
        "stylers": [
          {
            "saturation": -100
          },
          {
            "lightness": 45
          }
        ]
      },
      {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [
          {
            "visibility": "simplified"
          }
        ]
      },
      {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [
          {
            "visibility": "off"
          }
        ]
      },
      {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [
          {
            "visibility": "off"
          }
        ]
      },
      {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
          {
            "color": "#585b5d"
          },
          {
            "visibility": "on"
          }
        ]
      }
    ];
  
    // Crear un nuevo objeto StyledMapType, pasándole el array de estilos,
    // así como el nombre para mostrar en el control de tipo de mapa.
    var styledMap = new google.maps.StyledMapType(styles, {name: "Styled Map"});
  
    // Crear un objeto mapa, e incluir el MapTypeId para añadir
    // al control de tipo de mapa.
    var mapOptions = {	  
      zoomControl: true,
      mapTypeControl: false,
      scaleControl: false,
      scrollwheel: false,
      streetViewControl: false,
      draggable: true,              
      zoom: 8, // Ajustar el nivel de zoom a 3 para tener 4 veces menos zoom
      center: new google.maps.LatLng(-33.4489, -70.6693), // Coordenadas de Santiago, Chile
      mapTypeControlOptions: {
        mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
      }
    };
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
  
    // Asociar el mapa estilizado con el MapTypeId y establecerlo para mostrar.
    map.mapTypes.set('map_style', styledMap);
    map.setMapTypeId('map_style');
  
    
    var marker1 = new google.maps.Marker({
      position: new google.maps.LatLng(-33.4489, -70.6693), // Coordenadas de Santiago, Chile
      map: map,		
      icon: marker,
      title: ''
    });  
  }
  
  google.maps.event.addDomListener(window, 'load', initialize);
  
  $(document).delegate('*[data-toggle="lightbox"]', 'click', function(event) {
    event.preventDefault();
    $(this).ekkoLightbox();
  });
  