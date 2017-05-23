var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;

/* GET home page. */
router.post('/install_marketplace_images', function(req, res, next) {
	var identity_domain = req.body.identity_domain;
	var datacenter = req.body.datacenter;
	var cmd =  "python ../install_marketplace_images_WD.py "+identity_domain+" "+datacenter;
    console.log(cmd);
    exec(cmd, {maxBuffer: 1024 * 1000 * 1000}, function (error2, stdout2, stderr2){        
        console.log( stdout2 );                           
  		res.write( stdout2 );                           
    });
});

module.exports = router;
