let WS = new WebSocket("ws://"+location.host+"/ws");

WS.onmessage = (e)=>{
  const d = JSON.parse(e.data);
  balance.innerText="BAL: "+(d.balance||0);
  price.innerText="PX: "+(d.price||0);
  pnl.innerText="PNL: "+(d.pnl||0);
  position.innerText="POS: "+(d.position||"-");
  signal.innerText="SIG: "+(d.signal||"-");

  updateChart(d);
  drawDepth(d.depth||{});
  drawFoot(d.footprint||[]);
};
