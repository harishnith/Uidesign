async function loadHome(){
    const res = await fetch("/api/home");
    const data = await res.json();

    if(!data.nifty) return;

    document.getElementById("trend").innerText = data.nifty.trend;
    document.getElementById("sentiment").innerText = data.nifty.direction;
}

setInterval(loadHome, 2000);