// import grpc from "@grpc/grpc-js"
// import protoLoader from "@grpc/proto-loader"

fetch('https://ipinfo.io/json')
  .then(response => response.json())
  .then(data => {
    console.log(`Tu IP pública es: ${data.ip}`);
  });