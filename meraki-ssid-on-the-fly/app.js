// app.js

// ################################################################
// Overview
// ################################################################
/*
External Captive Portal (ExCAP) for Cisco Meraki MR access points and MX security appliances.

This application provides a basic click-through and sign-on splash page where the login will complete on a success page.

Click-through usage:   https://yourserver/click
Sign-on usage:         https://yourserver/signon

All HTML content uses Handlebars to provide dynamic data to the various pages.
The structure of the HTML pages can be modified under /views/filename.hbs
Images are stored in /public/img

All stateful session data is stored in a local MongoDB, which needs to be configured first.
This data will consist of the collected parameters and any form data collected from the user.

Original code by Cory Guynn - 2015
www.InternetOfLego.com
*/

// ################################################################
// Local Variables
// ################################################################

// web port
var port = 8181;

// ExCap parameters and form data object
//var session = {};

// ################################################################
// Utilities
// ################################################################

// used for debugging purposes to easily print out object data
var util = require('util');
  //Example: console.log(util.inspect(session, false, null));


// ################################################################
// Web Services and Middleware
// ################################################################

// express webserver service
var express = require('express');
var session = require('express-session');
var MongoDBStore = require('connect-mongodb-session')(session);

// create the web app
var app = express();

// session information stored to local mongo database
var store = new MongoDBStore({
    uri: 'mongodb://localhost:27017/test',
    collection: 'excap'
});

// Catch errors
store.on('error', function(error) {
  assert.ifError(error);
  assert.ok(false);
});

app.use(require('express-session')({
  secret: 'supersecret',  // this secret is used to encrypt cookie and session state. Client will not see this.
  cookie: {
    maxAge: 1000 * 60 * 60 * 24 // 1 day
  },
  store: store,
  resave: true,
  saveUninitialized: true
}));

// define the static resources for the splash pages
var path = require('path');
app.use("/public", express.static(path.join(__dirname, 'public')));
app.use("/css",  express.static(__dirname + '/public/css'));
app.use("/img", express.static(__dirname + '/public/img'));
app.use("/js", express.static(__dirname + '/public/js'));

// parses req.body
var bodyParser = require('body-parser');

// instruct the app to use the `bodyParser()` middleware for all routes
app.use(bodyParser.urlencoded({
extended: true
}));
app.use(bodyParser.json());

// ################################################################
// Handlebars to provide dynamic content in HTML pages
// ################################################################

var exphbs = require('express3-handlebars');
app.engine('.hbs', exphbs({defaultLayout: 'single', extname: '.hbs'}));
app.set('view engine', '.hbs');


// ################################################################
// Admin Site mongodb access
// ################################################################

var MongoClient = require('mongodb').MongoClient,
    format = require('util').format;


// ################################################################
// Sign-on Splash Page
// ################################################################

// #######
// signon page
// #######
app.get('/signon', function (req, res) {

  // extract parameters (queries) from URL
  req.session.host = req.headers.host;
  req.session.login_url = req.query.login_url;
  req.session.continue_url = req.query.continue_url;
  req.session.ap_name = req.query.ap_name;
  req.session.ap_tags = req.query.ap_tags;
  req.session.client_ip = req.query.client_ip;
  req.session.client_mac = req.query.client_mac;
  req.session.success_url = req.protocol + "://" + req.session.host + "/success";
  req.session.signon_time = new Date();
  req.session.recent_error = req.query.error_message;

  console.log(req.session.recent_error);

  // do something with the session and form data (i.e. console, database, file, etc. )
  // display data for debugging purposes
  console.log("Session data at signon page = " + util.inspect(req.session, false, null));

  // render login page using handlebars template and send in session data
  res.render('sign-on', req.session);

});

// #############
// success page
// #############
app.get('/success', function (req, res) {
  // extract parameters (queries) from URL
  req.session.host = req.headers.host;
  //req.session.logout_url = req.query.logout_url;
  req.session.logout_url = req.query.logout_url + "&continue_url=" + req.protocol + "://" + req.session.host + "/logout";
  req.session.success_time = new Date();

  // do something with the session data (i.e. console, database, file, etc. )
  // display data for debugging purposes
  console.log("Session data at success page = " + util.inspect(req.session, false, null));

  // render sucess page using handlebars template and send in session data
  res.render('success', req.session);


  var request = require('request');



  var options = { method: 'GET',
    url: 'https://dashboard.meraki.com/api/v0/organizations/549236/networks/L_646829496481092083/ssids',
    headers:
     {
       'x-cisco-meraki-api-key': 'c0b9de1eefb894c77073cc01e529e93c57cb071f'
     }
   };

  var number = 16;
  request(options, function (error, response, body) {
    if (error) throw new Error(error);

    jsonResp = JSON.parse(body);

    for(var counter in jsonResp){
      enabled = jsonResp[counter]["enabled"];

      if (enabled == false){
        number = jsonResp[counter]["number"];
        console.log("Updating SSID "+String(number));
        break;
      }
    }

    console.log(req.query.ssid + " " + req.query.wifipass);
    options = {
      url: 'https://n149.meraki.com/api/v0/networks/L_646829496481092083/ssids/' + number,
      method: 'PUT',
      headers:
       {
         'content-type': 'application/json',
         'x-cisco-meraki-api-key': 'c0b9de1eefb894c77073cc01e529e93c57cb071f'
       },
      body:
       { name: req.query.ssid,
         enabled: true,
         splashPage: 'None',
         ssidAdminAccessible: false,
         ipAssignmentMode: 'Bridge mode',
         useVlanTagging: false,
         authMode: 'psk',
         encryptionMode: 'wpa',
         psk: req.query.wifipass,
         minBitrate: 1,
         bandSelection: 'Dual band operation',
         perClientBandwidthLimitUp: 0,
         perClientBandwidthLimitDown: 0 },
      json: true };

    request(options, function (error, response, body) {
      if (error) throw new Error(error);
      console.log(response.statusCode);

    });

  });
});


// ################################################################
// Start application
// ################################################################

// start web services
app.listen(process.env.PORT || port);
console.log("Server listening on port " + port);
