function drawFoot(arr){
  window.__lastTrades = window.__lastTrades || [];
  const c = document.getElementById('foot');
  const ctx = c.getContext('2d');
  ctx.clearRect(0,0,c.width,c.height);

  const W=c.width, H=c.height;
  const N = arr.slice(-50);
  const max = Math.max(1, ...N.map(x=>Math.abs(x.delta)));

  N.forEach((x,i)=>{
    const x0 = i/N.length*W;
    const h = (Math.abs(x.delta)/max)*H;
    ctx.fillStyle = x.delta>=0 ? "#00e676" : "#ff1744";
    ctx.fillRect(x0, H-h, (W/N.length)-2, h);
  });
}
