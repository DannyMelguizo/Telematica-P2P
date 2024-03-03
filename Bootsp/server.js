const grpc = require("@grpc/grpc-js")
const protoLoader = require("@grpc/proto-loader")
const pears = require('./pears_file.js');
const config = require('./config_file.js');
const client = require('./client.js');
const net = require('net');


const socket = async() => {
  const port = await config.get_port_server();
  const server = net.createServer((socket) => {
    console.log('Cliente conectado.');

    socket.on('data', (data) => {
        console.log('Datos recibidos del cliente:', data.toString());
    });

    socket.on('end', () => {
        console.log('Cliente desconectado.');
    });

    // Puedes enviar datos al cliente así
    socket.write('Hola desde el servidor.\n');

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