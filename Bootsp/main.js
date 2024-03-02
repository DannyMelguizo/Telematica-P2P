const config = require('./config_file.js');
const pears = require('./pears_file.js');
const server = require('./server.js');

const main = async () => {
    await config.create_config_file();
    await pears.create_pears_file();

    await server.main();
}

main()