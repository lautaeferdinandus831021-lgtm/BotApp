let chart, series, lineTP, lineSL;
let tradeMarkers = [];

function initChart(){
  chart = LightweightCharts.createChart(document.getElementById('chart'), {
    layout:{background:{color:'#0b0b0b'}, textColor:'#ddd'},
    grid:{vertLines:{color:'#222'}, horzLines:{color:'#222'}}
  });
  series = chart.addLineSeries({color:'#4caf50'});
}

window.addEventListener('load', initChart);

function setTPSL(tp, sl){
  if(lineTP) chart.removeSeries(lineTP);
  if(lineSL) chart.removeSeries(lineSL);

  lineTP = chart.addLineSeries({color:'#00e676', lineWidth:1});
  lineSL = chart.addLineSeries({color:'#ff1744', lineWidth:1});

  const t = Math.floor(Date.now()/1000);
  lineTP.setData([{time:t, value:tp},{time:t+60, value:tp}]);
  lineSL.setData([{time:t, value:sl},{time:t+60, value:sl}]);
}

function addMarker(signal, price){
  const t = Math.floor(Date.now()/1000);
  tradeMarkers.push({
    time:t,
    position: signal==="BUY" ? "belowBar":"aboveBar",
    color: signal==="BUY" ? "#00e676":"#ff1744",
    shape: signal==="BUY" ? "arrowUp":"arrowDown",
    text: signal+" @"+price
  });
  series.setMarkers(tradeMarkers);
}

function updateChart(d){
  const t = Math.floor(Date.now()/1000);
  if(series) series.update({time:t, value:d.price||0});

  // last trade marker
  if(d.trades && d.trades.length){
    const last = d.trades[d.trades.length-1];
    addMarker(last.signal, last.price);
    setTPSL(last.tp, last.sl);
  }
}

function replay(){
  if(!window.__lastTrades) return;
  let i=0;
  const arr = window.__lastTrades;
  const iv = setInterval(()=>{
    if(i>=arr.length){ clearInterval(iv); return; }
    const tr = arr[i++];
    addMarker(tr.signal, tr.price);
    setTPSL(tr.tp, tr.sl);
  }, 500);
}
