const fs = require('fs');
const config = require('./config_file.js');

const create_pears_file = async () => {
    ip = await config.get_ip();
    const pears = {

        'pears_connected': [
            ip,
        ],
        'pears_available': {}
    };

    // I don't have pears connected
    pears.pears_available[ip] = []

    await fs.promises.writeFile('pears.json', JSON.stringify(pears), (err) => {});
};

const get_pears = () => {
    let pears = fs.readFileSync('pears.json');
    return JSON.parse(pears);
}

const get_available_pears = () => {
    let available_pears = get_pears().pears_available;
    let ips = Object.keys(available_pears);

    let random_ip = ips[Math.floor(Math.random() * ips.length)];
    while(Object.keys(available_pears[random_ip]).length >= 2) {
        random_ip = ips[Math.floor(Math.random() * ips.length)];
    }

    return random_ip;
}

const add_pear = async (ip_father, ip_son) => {
    let file = get_pears();
    let pears_json = file.pears_available;

    // Add the new pear to his father
    pears_json[ip_father] = [...pears_json[ip_father], ip_son];
    // Link the new pear with his father
    pears_json[ip_son] = [ip_father];

    // Update the main file
    file.pears_available[ip_father] = pears_json[ip_father];
    file.pears_available[ip_son] = pears_json[ip_son];

    file.pears_connected = [...file.pears_connected, ip_son];

    await fs.promises.writeFile('pears.json', JSON.stringify(file), (err) => {});

}

module.exports = { 
    create_pears_file,
    get_available_pears,
    add_pear,
    get_pears
};