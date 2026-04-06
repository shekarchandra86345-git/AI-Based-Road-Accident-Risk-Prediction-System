let map, marker;
let currentCoords = [17.385, 78.486]; // Default: Hyderabad

// ── Persistent Profile (localStorage) ───────────────────────
const PROFILE_FIELDS = ['driver_age', 'experience', 'vehicle_age', 'vehicle_type'];

function saveProfile() {
    PROFILE_FIELDS.forEach(id => {
        const el = document.getElementById(id);
        if (el) localStorage.setItem('ag_' + id, el.value);
    });
}

function clearProfile() {
    PROFILE_FIELDS.forEach(id => localStorage.removeItem('ag_' + id));
    // Reset to defaults
    const defaults = { driver_age: 25, experience: 5, vehicle_age: 3, vehicle_type: 0 };
    PROFILE_FIELDS.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = defaults[id];
    });
    const notice = document.getElementById('profile-notice');
    if (notice) notice.style.display = 'none';
}

function loadProfile() {
    PROFILE_FIELDS.forEach(id => {
        const saved = localStorage.getItem('ag_' + id);
        if (saved !== null) {
            const el = document.getElementById(id);
            if (el) el.value = saved;
        }
    });
    // Show a subtle notice if profile was restored
    const anyRestored = PROFILE_FIELDS.some(id => localStorage.getItem('ag_' + id) !== null);
    if (anyRestored) {
        const notice = document.getElementById('profile-notice');
        if (notice) notice.style.display = 'block';
    }
}

// Initialize Map
function initMap() {
    map = L.map('map').setView([17.3850, 78.4867], 13);
    
    // Light themed tiles (Google Maps style)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    marker = L.marker([17.3850, 78.4867], { draggable: true }).addTo(map);

    marker.on('dragend', function(e) {
        const pos = e.target.getLatLng();
        document.getElementById('lat').value = pos.lat.toFixed(6);
        document.getElementById('lon').value = pos.lng.toFixed(6);
    });

    map.on('click', function(e) {
        marker.setLatLng(e.latlng);
        document.getElementById('lat').value = e.latlng.lat.toFixed(6);
        document.getElementById('lon').value = e.latlng.lng.toFixed(6);
    });

    // Handle Geolocation
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            map.setView([lat, lon], 14);
            marker.setLatLng([lat, lon]);
            document.getElementById('lat').value = lat.toFixed(6);
            document.getElementById('lon').value = lon.toFixed(6);
        });
    }
}

async function predictRisk() {
    const data = {
        lat: parseFloat(document.getElementById('lat').value),
        lon: parseFloat(document.getElementById('lon').value),
        driver_age: parseInt(document.getElementById('driver_age').value),
        driver_experience: parseInt(document.getElementById('experience').value),
        vehicle_age: parseInt(document.getElementById('vehicle_age').value),
        vehicle_type: parseInt(document.getElementById('vehicle_type').value),
        speed: parseInt(document.getElementById('speed').value),
        weather: parseInt(document.getElementById('weather').value),
        road_type: parseInt(document.getElementById('road_type').value),
        light_condition: parseInt(document.getElementById('light').value),
        traffic_density: parseInt(document.getElementById('traffic').value),
        surface_condition: parseInt(document.getElementById('surface').value),
        hour_of_day: new Date().getHours(),
        accident_count: parseInt(document.getElementById('accident_count').value)
    };

    // Save persistent profile fields before submitting
    saveProfile();

    const resultDiv = document.getElementById('risk-result');
    const predictBtn = document.getElementById('predict-btn');
    
    predictBtn.disabled = true;
    predictBtn.innerText = "Analyzing Risk...";

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === 'success') {
            // Redirect to the result page (speedometer + chatbot)
            window.location.href = '/result';
        } else {
            alert("Error: " + result.message);
        }
    } catch (error) {
        console.error(error);
        alert("Server communication failed.");
    } finally {
        predictBtn.disabled = false;
        predictBtn.innerText = "Check Risk Status";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    initMap();
    // Auto-save profile whenever a persistent field changes
    PROFILE_FIELDS.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', saveProfile);
    });
});
