# DevNet Create Mini-Hack: Fastlane

---

[image1]: ./imgs/pipeline.png
[image2]: ./imgs/report_sample.png

# Pipeline for the mini-hack:

![alt text][image1]

## 0. Copy DC2017_WORKSHOP folder from Finder->Documents to the Desktop

## 1. Open Desktop -> DC2017_WORKSHOP -> iOS Client -> Examples -> UdpEchoClient -> UdpEchoClient.xcodeproj

## 2. In Xcode (Navigator) open UdpEchoClient -> UdpEchoClient -> ViewController.m

Check setupSocket method (uncomment a part of code, responsible for marking) and Set one of the following parameters for `optval` variable:

* NET_SERVICE_TYPE_BE
* NET_SERVICE_TYPE_BK
* NET_SERVICE_TYPE_VI
* NET_SERVICE_TYPE_VO
* NET_SERVICE_TYPE_RV
* NET_SERVICE_TYPE_AV
* NET_SERVICE_TYPE_OAM
* NET_SERVICE_TYPE_RD

## 3. Compile project and run it on your iOS device

## 4. Preparations for Capturing

Requirement: Your iOS device and Mac must be in the same FastLane enabled Wi-Fi network!

4.1 Open Desktop -> DC2017_WORKSHOP -> FastLaneTestingScript -> config.json

4.2 Change parameter "src_ip". It's IP address of your iOS device. You could find it by opening Settings ->
Wi-Fi -> IP Address.

4.3 Change parameter "dst_ip". It's IP address of your Mac. You could find it by opening Settings ->
Network -> Advanced... -> TCP/IP -> IPv4 Address.

4.4 Save changes and close config.json

4.5 Run PacketSender on your Mac. Check UDP port value in the bottom of the window.

4.6 Open UdpEchoClient (from step 3) on your iOS device. Put IP address from step 4.3 and 
put UDP Port value from step 4.5

4.7. Write some message and Push 'Send' button. In case of success you will see message in the Log of PacketSender.
Ok, let's start capturing.

## 5. Traffic capturing and analysis

5.1 Run Termilal on your Mac and use command:

`cd Desktop/DC2017_WORKSHOP/FastLaneTestingScript/`

`python main.py`

5.3 Capturing just started. You need to push 'Send' button on your iOS app **as more times as possible**.

5.4 After the end of a capturing process you will see the capturing report:

![alt text][image2]

