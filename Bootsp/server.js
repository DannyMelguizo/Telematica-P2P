const grpc = require("@grpc/grpc-js")
const protoLoader = require("@grpc/proto-loader")
const pears = require('./pears_file.js');
const config = require('./config_file.js');
const client = require('./client.js');
const net = require('net');


const socket = async() => {
  const port = await config.get_port_server();
  const ip = await config.get_ip();
  const server = net.createServer((socket) => {
    console.log('Cliente conectado.');

    socket.on('data', (data) => {
        var my_connections = pears.get_pears().pears_available[ip];
        console.log("Data: ", data.toString());
         
        // for (let i = 0; i < my_connections.length; i++) {
        //   const client = new net.Socket();

        //   client.connect(port, my_connections[i], () => {
        //       client.write(data.toString());
      
        //   });
        //   client.on('data', (data) => {
        //       console.log(`Received: ${data}`);
        //       client.destroy();
        //   });
      
        //   client.on('error', (err) => {
        //       console.log(err);
        //   });
        // }
    });

    socket.on('end', () => {
        console.log('Cliente desconectado.');
    });

    // Manejar errores
    socket.on('error', (err) => {
        console.error(`Error: ${err}`);
    });
  });

  server.listen(port, () => {
      console.log(`Servidor escuchando en el puerto ${port}`);
  });

  server.on('error', (err) => {
      throw err;
  });

}


const AddIP = (call, callback) => {
  // Get a random ip from the server
  let ip = pears.get_available_pears();

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

  const port_grpc = await config.get_port_grpc();
  const getavailablepears = grpc.loadPackageDefinition(packageDefinition).getavailablepears;
  const server = new grpc.Server();
  const ip = `0.0.0.0:${port_grpc}`;

  socket();

  server.addService(getavailablepears.GetAvailablePears.service, { AddIP });
  server.bindAsync(ip, grpc.ServerCredentials.createInsecure(), (err, port) => {
    if (err) {
      console.error(err);
      return;
    }
  });


}

module.exports = { main }