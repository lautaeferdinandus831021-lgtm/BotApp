
const chart = LightweightCharts.createChart(
    document.getElementById('chart'),
    { layout:{ background:{color:"#000"}, textColor:"#0f0"} }
);

const candleSeries = chart.addCandlestickSeries();

const ws = new WebSocket("ws://localhost:8765");

ws.onmessage = (e)=>{
    const data = JSON.parse(e.data);

    document.getElementById("price").innerText =
        "PRICE: " + data.price;

    document.getElementById("delta").innerText =
        "DELTA: " + data.delta;

    if(data.candles_m1.length){

        const c = data.candles_m1.slice(-1)[0];

        candleSeries.update({
            time: c.time,
            open: c.open,
            high: c.high,
            low: c.low,
            close: c.close
        });
    }
};
