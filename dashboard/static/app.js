async function loadData() {
    const res = await fetch('/data');
    const data = await res.json();

    document.getElementById("nifty").innerText = data.nifty;
    document.getElementById("ce").innerText = data.ce;
    document.getElementById("pe").innerText = data.pe;

    document.getElementById("nifty_card").innerText = data.nifty;
    document.getElementById("ce_card").innerText = data.ce;
    document.getElementById("pe_card").innerText = data.pe;
    document.getElementById("atm").innerText = data.atm;

    const signal = document.getElementById("signal");
    signal.innerText = data.signal;

    signal.className = "signal";

    if (data.signal.includes("BUY")) signal.classList.add("green");
    else if (data.signal.includes("SELL")) signal.classList.add("red");
    else signal.classList.add("yellow");
}

setInterval(loadData, 2000);
loadData();