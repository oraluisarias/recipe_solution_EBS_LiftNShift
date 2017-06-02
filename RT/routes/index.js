var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
var DMN = require("./models/cloudbots_domain_data");

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

router.get('/getOPCZone/:identity_domain/:password', function(req, res, next) {	
	getOPCZone(req.params.identity_domain, req.params.password);
});

router.post('/getOPCZone', function(req, res, next) {	
	getOPCZone(req.body.identity_domain, req.body.password);
});

function getOPCZone(identity_domain, password){
	DMN.findOne({ where: { "identity_domain" : identity_domain } }).then(function(domain) {
        if(domain){
			res.json( { domain.identity_domain : domain.domain_data } );   
        }
        else{
			var cmd =  "python ../getOPCZone.py "+identity_domain+" "+password;
		    console.log(cmd);
		    exec(cmd, function (error2, stdout2, stderr2){      
		    	try{
			    	var result = JSON.parse( stdout2.replace(/\'/g, '"') );  
			        console.log( result );                           
					DMN.build( { identity_domain : identity_domain, domain_data : result[identity_domain] } ).save().then(function() {
						res.json( result );      				    	
				  	}).catch(function (err) {
		                console.log(err);
		            }); 
				} catch (e) {
					res.send( stdout2 );       
			      	console.error(e.stack);
			    }                    
		    });
        }
    });
}

module.exports = router;
