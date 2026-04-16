const API = location.origin;
async function save(){
  await fetch(API+"/config",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({api_key:k.value, api_secret:s.value, passphrase:p.value})
  });
  alert("Saved");
}
