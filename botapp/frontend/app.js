
const chart = LightweightCharts.createChart(
    document.getElementById('chart'),
    { layout:{ background:{color:"#000"}, textColor:"#0f0"} }
);

const candleSeries = chart.addCandlestickSeries();

let markers = [];
let tpLine, slLine;

// WS URL AUTO
const ws_url = (location.protocol === "https:" ? "wss://" : "ws://") + location.host.replace("3000","8765");
const ws = new WebSocket(ws_url);

ws.onmessage = (e)=>{
    const data = JSON.parse(e.data);

    document.getElementById("price").innerText =
        "PRICE: " + data.price;

    document.getElementById("delta").innerText =
        "DELTA: " + data.delta;

    document.getElementById("pnl").innerText =
        "PNL: " + data.pnl;

    // candle
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

    // 🔥 marker entry
    if(data.position && data.entry){

        markers = [{
            time: Math.floor(Date.now()/1000),
            position: data.position=="long" ? "belowBar" : "aboveBar",
            color: data.position=="long" ? "green" : "red",
            shape: data.position=="long" ? "arrowUp" : "arrowDown",
            text: data.position.toUpperCase()
        }];

        candleSeries.setMarkers(markers);
    }

    // 🔥 TP/SL line
    if(data.tp && data.sl){

        if(!tpLine){
            tpLine = candleSeries.createPriceLine({
                price: data.tp,
                color: "green",
                lineWidth: 2,
                title: "TP"
            });
        } else {
            tpLine.applyOptions({price:data.tp});
        }

        if(!slLine){
            slLine = candleSeries.createPriceLine({
                price: data.sl,
                color: "red",
                lineWidth: 2,
                title: "SL"
            });
        } else {
            slLine.applyOptions({price:data.sl});
        }
    }
};
