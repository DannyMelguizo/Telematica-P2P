const fs = require('fs');

const create_config_file = async () => {
    const ip = await get_my_ip();
    const name_directory = 'shared_files'
    const proto_path = 'protobufs/service.proto'

    fs.mkdir(name_directory, (err) => {
        if (err) {
            console.log("The directory already exists");
        }
    });

    const config = {
        'config': {
            "ip": ip,
            'port_server': '8000',
            'port_grpc': '9998',
            'port_mom': '9997',
            'port_rest': '9996',
            'directory': `${name_directory}`,
            'proto_path': `${proto_path}`
        }
    };

    await fs.promises.writeFile('config.json', JSON.stringify(config), (err) => {});
};


const get_my_ip = async () => {
    let ip = await fetch('https://ipinfo.io/json').then(response => (response.json()));
    return ip.ip;
};

const get_config = () => {
    let config = fs.readFileSync('config.json');
    return JSON.parse(config);
}

const get_ip = () => get_config().config.ip;
const get_port_server = () => get_config().config.port_server;
const get_port_grpc = () => get_config().config.port_grpc;
const get_port_mom = () => get_config().config.port_mom;
const get_port_rest = () => get_config().config.port_rest;
const get_directory = () => get_config().config.directory;
const get_proto_path = () => get_config().config.proto_path;

module.exports = { 
    create_config_file, 
    get_ip,
    get_port_server,
    get_port_grpc,
    get_port_mom,
    get_port_rest,
    get_directory,
    get_proto_path
};