async function fetchWeather() {
    const location = document.getElementById('location').value;
    const response = await fetch(`/weather?location=${location}`);
    const data = await response.json();
    document.getElementById('weather-info').innerText = JSON.stringify(data.weather, null, 2);
}
