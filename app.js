function main() {

    const five_min_in_ms = 300000;
    console.log("Hello!");
    fetchJSONData();
    setInterval(fetchJSONData, five_min_in_ms);

}

async function fetchJSONData() {

    let url="roomstatus.json";
    let response = await fetch(url);
    let status = await response.json();

    let room_temp = status["room"][0]["temperature"];
    let humidity = status["room"][0]["humidity"];
    let plant1_moisture = status["room"][0]["bop_moisture"];
    let plant1_mpercent = status["room"][0]["bop_percent"];

    let plant2_moisture = status["room"][0]["mon_moisture"];
    let plant2_percent = status["room"][0]["mon_percent"]
    
    let temparea = document.getElementById("temperature");
    temparea.innerText = room_temp;

    let bop_area = document.getElementById("bop-moisture");
    bop_area.innerHTML = `${plant1_moisture} (${plant1_mpercent}%)`;

    let mon_area = document.getElementById("mon-moisture");
    mon_area.innerHTML = `${plant2_moisture} (${plant2_percent}%)`;

    let hum_area = document.getElementById("humidity");
    hum_area.innerHTML = `${humidity}% `;
}


window.addEventListener("load", main);