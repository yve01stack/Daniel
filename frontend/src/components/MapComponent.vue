<template>

  <div style="position: relative; ">
    <div id="map" style="height: 240px;"></div>
  </div>
  
  <div>
    <el-timeline style="max-width: 600px; margin: 7px 0 0 -40px;">
      <el-timeline-item :timestamp="selectedOrderCopy.created_on" placement="top">
        <div>
          <span style="font-weight: 600;">Votre colis est en cours de livraison</span>
          <div><span>{{ selectedOrderCopy.paid_desc }}</span></div>
        </div>
      </el-timeline-item>
      <el-timeline-item :timestamp="selectedOrderCopy.updated_on" placement="top">
        <div v-if="selectedOrderCopy.delivered">
          <div><span style="font-weight: 600;">Numéro de commande: </span>{{ selectedOrderCopy.order_number }}</div>
          <div><span style="font-weight: 600;">Montant total: </span>{{ selectedOrderCopy.total_price }} {{ selectedOrderCopy.currency }}</div>
          <div><span style="font-weight: 600;">No. livraison: </span>{{ selectedOrderCopy.delivery_number }}</div>
          <div><span style="font-weight: 600;">Centre de livraison: </span>{{ selectedOrderCopy.delivery_center }}</div>
          <el-alert 
          title="Colis Livré, soyez toujours les bienvenus sur notre platforme" 
          style="background-color: transparent; margin-left: -16px;"
          type="success" :closable="false"
          show-icon></el-alert>
        </div>
      </el-timeline-item>
    </el-timeline>
  </div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

const props = defineProps({
    selectedOrder: { type: Object, required: true },
});

// OpenRouteService API key
const API_KEY = '5b3ce3597851110001cf6248fd32a25bf5a749a69766fc08d40f5e12';

const selectedOrderCopy = ref(props.selectedOrder);

// Starting and ending coordinates  
const start = ref([
  selectedOrderCopy.value.delivery_from.latitude,
  selectedOrderCopy.value.delivery_from.longitude 
]);

const end = ref([
  selectedOrderCopy.value.delivery_to.latitude,
  selectedOrderCopy.value.delivery_to.longitude 
]);

watch(() => props.selectedOrder, (newValue) => {
  selectedOrderCopy.value = newValue;
});


const map = ref(null);

const initializeMap = () => {
  map.value = L.map('map').setView([11.6899699, -0.8999695], 4); // Center of Gabon
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map.value);
  
  // Add markers for start and end points
  L.marker(start.value).addTo(map.value).bindPopup('Agent: '+selectedOrderCopy.value.managed_by.name).openPopup();
  L.marker(end.value).addTo(map.value).bindPopup(selectedOrderCopy.value.ordered_by.name).openPopup();

  // Get the route and draw it on the map
  getRoute(start.value, end.value);
};

const getRoute = async (start, end) => {
  const url = `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${API_KEY}&start=${start[1]},${start[0]}&end=${end[1]},${end[0]}`;
  
  try {
    const response = await axios.get(url);
    const route = response.data.features[0].geometry.coordinates;
    
    // Convert route to Leaflet LatLng objects
    const latLngs = route.map(coord => [coord[1], coord[0]]);
    
    // Draw the route on the map
    L.polyline(latLngs, { color: 'blue' }).addTo(map.value);
    
  } catch (error) {
    console.error('Error fetching route:', error);
  }
};

const coordinates = ref(null);

const getCoordinates = async (address) => {
  if (!address) {
    console.error('Please enter an address');
    return;
  }

  const url = `https://nominatim.openstreetmap.org/search?q=${address}&format=json&addressdetails=1&limit=1&polygon_svg=1`;

  try {
    const response = await axios.get(url);

    if (response.data.length > 0) {
      coordinates.value = [response.data[0].lon, response.data[0].lat];
      return coordinates.value;

    } else {
      console.log('Address not found');
    }
  } catch (error) {
    console.error('Error fetching coordinates:', error);
  }
};

onMounted(() => {
  initializeMap();
});
</script>

<style>
#map {
  height: 100%;
  width: 100%;
  position: relative;
}
</style>
