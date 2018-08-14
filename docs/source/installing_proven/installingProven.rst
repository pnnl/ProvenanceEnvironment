
Purpose
-------
* Setting up a development and testbed environment is not trivial.  This slide deck documents the testbed I set up on my MacOS laptop. Hopefully this will be helpful to the wider GridAPPS-D team or other development teams using ProvEn.
* Disclaimer:  This guide is intended to offer a complete set of notes.   However there may be differences depending on the platform you are using and unfortunately there may some gaps of knowledge.

What you should expect to do
----------------------------
Once the development system and testbed are completely setup you should be able to run a ProvEn server in debug mode, accessible by REST services

Prerequisites
-------------

* Download and install
	* Latest Eclipse IDE J2EE (I used Eclipse Oxygen.2 (4.7.2))	
	* Java 8 JDK
	
* Brew install
	* git 2.12.0
	* gradle 4.5.1
	* influxdb 1.4.2
	* maven 3.3.3 3.3.9
* Download and set aside for later use
	* payara-micro-5.181.jar from: https://s3-eu-west-1.amazonaws.com/payara.fish/Payara+Downloads/
* Please note that Eclipse will need to be configured to support your Gradle, Maven, use your Java 8 JDK

