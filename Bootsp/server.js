const grpc = require("@grpc/grpc-js")
const protoLoader = require("@grpc/proto-loader")
const pears = require('./pears_file.js');
const config = require('./config_file.js');


const AddIP = (call, callback) => {
  // Get a random ip from the server
  let ip = pears.get_available_pears();
  
  console.log("ip aleatoria" + ip)
  console.log("ip del cliente" + call.request.ip)

  // Add the new pear to the server
  pears.add_pear(ip, call.request.ip);

  // Return the ip to the client
  callback(null, { ip: ip });
}

const main = async () => { 
  const packageDefinition = protoLoader.loadSync(
    config.get_proto_path(),
    {
      keepCase: true,
      longs: String,
      enums: String,
      defaults: true,
      oneofs: true
    }
  );

  const getavailablepears = grpc.loadPackageDefinition(packageDefinition).getavailablepears;
  const server = new grpc.Server();
  const ip = `0.0.0.0:${config.get_port_grpc()}`

  server.addService(getavailablepears.GetAvailablePears.service, { AddIP });
  server.bindAsync(ip, grpc.ServerCredentials.createInsecure(), (err, port) => {
    if (err) {
      console.error(err);
      return;
    }
    server.start();
  })
}

module.exports = { main }