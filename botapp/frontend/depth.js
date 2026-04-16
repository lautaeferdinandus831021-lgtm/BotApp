function drawDepth(depth){
  const c = document.getElementById('depth');
  const ctx = c.getContext('2d');
  ctx.clearRect(0,0,c.width,c.height);

  const bid = depth.bid_cv||[];
  const ask = depth.ask_cv||[];

  const W=c.width, H=c.height;

  ctx.strokeStyle="#00e676";
  ctx.beginPath();
  bid.forEach((v,i)=>{
    const x = i/(bid.length||1)*W;
    const y = H - (v/(bid[bid.length-1]||1))*H;
    i?ctx.lineTo(x,y):ctx.moveTo(x,y);
  });
  ctx.stroke();

  ctx.strokeStyle="#ff1744";
  ctx.beginPath();
  ask.forEach((v,i)=>{
    const x = i/(ask.length||1)*W;
    const y = H - (v/(ask[ask.length-1]||1))*H;
    i?ctx.lineTo(x,y):ctx.moveTo(x,y);
  });
  ctx.stroke();
}
