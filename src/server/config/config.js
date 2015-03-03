var env = 'development'//(process.env.NODE_ENV == 'production') ? 'production' : 'development';
var config = require("./config." + env);

module.exports = config;