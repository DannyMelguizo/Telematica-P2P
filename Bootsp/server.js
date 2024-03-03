const grpc = require("@grpc/grpc-js")
const protoLoader = require("@grpc/proto-loader")
const pears = require('./pears_file.js');
const config = require('./config_file.js');
const client = require('./client.js');
const net = require('net');

const AddIP = (call, callback) => {
  // Get a random ip from the server
  let ip = pears.get_available_pears();

  // Add the new pear to the server
  pears.add_pear(ip, call.request.ip);

  // Return the ip to the client
  callback(null, { ip: ip });
}

// const server = net.createServer((socket) => {
//   console.log('Cliente conectado.');

//   socket.on('data', (data) => {
//     port = config.get_port_mom();
//     connexions = pears.get_pears().pears_available[config.get_ip()];
//     data = JSON.parse(data.toString());

//     data.last_peer = config.get_ip();

//     connexions.forEach((ip) => {
//       if (ip != data.last_peer) {
//         client.connect_to(port, ip, data);
//       }
//     });

//   })

//   socket.end();

// });

// server.listen(config.get_port_server(), () => {});
// server.on('error', (err) => {throw err;});

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
  const ip = `0.0.0.0:${config.get_port_grpc()}`;

  server.addService(getavailablepears.GetAvailablePears.service, { AddIP });
  server.bindAsync(ip, grpc.ServerCredentials.createInsecure(), (err, port) => {
    if (err) {
      console.error(err);
      return;
    }
  });
}

module.exports = { main }