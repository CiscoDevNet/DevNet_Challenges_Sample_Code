# Cisco Meraki ExCap Splash Page Server

Overview

This Node.JS applications provides an example of a custom Captive Portal / Splash Page for Cisco Meraki access points.

### Meraki Captive Portal API documentation:
https://meraki.cisco.com/lib/pdf/meraki_whitepaper_captive_portal.pdf

# Usage

## Configure the Wi-Fi SSID

* Logon to the Meraki Dashboard

    Dashboard --> Wireless --> Access Control: (select SSID name from list)

* Configure an SSID with a Sign-on splash page

* Scroll down the page and enable the "Walled Garden". Enter the IP address of your web server, to provide access to your splash page content prior to authentication. Enter any additional IP addresses for hosted content such as images, terms of service, etc in this section as well.

## Create a Meraki Local User

* Dashboard --> Network Wide --> Configure --> Users

* Select the SSID from the drop-down, then add a new Meraki local user and grant 'Authorized for SSID'

## Configure the Splash Page

* Dashboard --> Wireless --> Configure --> Splash Page Select: Use custom URL

* Enter the URL for the splash page, e.g.:  http://myAppServer/signon

# Install

## Install MongoDB
https://docs.mongodb.com/manual/installation/

* Create a path to store MongoDB data
```
mkdir ../mongodata
```

* Start the MongoDB service:
```
mongod --dbpath=../mongodata --nojournal
```
(--nojournal keeps MongoDB from pre-allocating a 2GB default journal file)

## Clone this app into your intended directory
```
mkdir captiveportal
cd captiveportal
git clone https://github.com/tbd
```

## Install any missing dependencies
`npm install`

## Run the app
`node app.js`       or as a service using PM2:  `pm2 start app.js --name excap`

#Admin Report
You can see the session data by going to

http://myAppServer/admin

Note: for production, please implement SSL and appropriate authentication/authorization for the admin page.

#Credit
Cory Guynn, 2015
