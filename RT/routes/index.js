var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;

/* GET home page. */
router.post('/install_marketplace_images', function(req, res, next) {
	var identity_domain = req.body.identity_domain;
	var datacenter = req.body.datacenter;
	var password = req.body.password;
	var cmd =  "python ../install_marketplace_images_WD.py "+identity_domain+" "+datacenter+" "+password;
    console.log(cmd);
    exec(cmd, {maxBuffer: 1024 * 1000 * 1000}, function (error2, stdout2, stderr2){        
        console.log( stdout2 );                           
    });
	res.json( {"result":"Executing RT on background"} );                           
});

router.get('/getOPCZone/:identity_domain', function(req, res, next) {
	var identity_domain = req.params.identity_domain;
	var cmd =  "python ../getOPCZone.py "+identity_domain;
    console.log(cmd);
    exec(cmd, function (error2, stdout2, stderr2){      
    	var result = JSON.parse( stdout2 );  
        console.log( result );                           
		res.json( result );                           
    });
});

router.post('/getOPCZone', function(req, res, next) {
	var identity_domain = req.body.identity_domain;
	var cmd =  "python ../getOPCZone.py "+identity_domain;
    console.log(cmd);
    exec(cmd, function (error2, stdout2, stderr2){      
    	var result = JSON.parse( stdout2 );  
        console.log( result );                           
		res.json( result );                           
    });
});

module.exports = router;
