const net = require('net');

const connect_to = (port, ip, data) =>{
    const client = new net.Socket();

    client.connect(port, ip, () => {
        client.write(data.toString());

    });

    
    client.on('data', (data) => {
        console.log(`Received: ${data}`);
        client.destroy();
    });

    client.on('error', (err) => {
        console.log(err);
    });
}

module.exports = { connect_to }