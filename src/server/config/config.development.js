var config = {};

config.env = 'development';
config.db = {};
config.db.host = 'localhost';
config.db.user = 'root';
config.db.password = 'root';
config.secret = 'secret';

// Port that express listens to
config.port = 4321;

module.exports = config;