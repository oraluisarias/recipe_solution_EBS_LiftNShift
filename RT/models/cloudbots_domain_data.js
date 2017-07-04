var mysql_host = process.env.CLOUDBOTS_DBHOST;
if(mysql_host == undefined || mysql_host == ""){
    mysql_host = 'gse-admin.oraclecloud.com';
}
var Sequelize = require('sequelize');
var sequelize = new Sequelize('CloudBots', 'root', 'Welcome321', {
  host: mysql_host,
  dialect: 'mysql'
});
var DMN = sequelize.define('cloudbots_domain_data', {
    "identity_domain": { type: Sequelize.STRING, primaryKey: true  },
    "domain_data": { type: Sequelize.JSON }
});
DMN.sync();
module.exports = DMN;
