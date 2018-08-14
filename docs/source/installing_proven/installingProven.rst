
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

Clone Proven Repositories
-------------------------

* https://github.com/pnnl/proven-message
* https://github.com/pnnl/proven-cluster
* https://github.com/pnnl/proven-client
* https://github.com/pnnl/proven-docker

Import Gradle Projects in Eclipse
---------------------------------

* Import proven-message and proven-member projects as gradle projects.
	* Note:  The “proven-cluster” project contains several nested layers of projects.  
	* Import the “proven-cluster” subproject “proven-member”  – importing “proven-cluster will cause undesirable effects, limiting what you can build. 
		
.. figure:: import_projects.png
    :align: left
    :alt: import_projects-image
    :figclass: align-left
	
Create General Eclipse Project for testbed Resources
----------------------------------------------------
This project(name it "payara-resources") will be used to provide a micro service engine for testing later. Add the payara-micro jar in the top folder

.. figure:: payara-resources.png    
    :alt: payara-resources-image
   
..



Build and publish proven_message jar
-------------------------------------

* Open the following Eclipse views using Window->show view
	* General->Console
	* Gradle->Gradle Executions
	* Gradle->Gradle Tasks
* Click on the proven_message project (you may need to click on the build.gradle file).

.. figure:: build_publish.png    
    :alt: build_publish-image
    
..



Build and publish proven_message-0.1-all-in-one jar
----------------------------------------------------

Build and publish the proven_message-0.1-all-in-one.jar file to maven local repository so that the hybrid services can use the interface.
* Open build task folder
* Double click on “build” task.
* Open publishing task folder.
* Double click on “publish” task.
* Double click on “publishToMavenLocal”
* Confirm no errors in Console View.
* Inspect the proven-message/build/libs/ directory for proven-message-0.1-all-in-one.jar

.. figure:: build_maven_local.png
    :align: left
    :alt: build_maven_local-image
    :figclass: align-left
..

Building the ProvEn Server (proven-member)
------------------------------------------

* Use Gradle Tasks to Build the Proven hybrid service war file
* If necessary use Gradle IDE tasks to rebuild eclipse files.

.. figure:: build_proven_server.png
    :align: left
    :alt: build_proven_server-image
    :figclass: align-left

Create External Tools Configurations 
------------------------------------

	
Create Debug Configuration
--------------------------

.. figure:: debug_config.png
    :align: left
    :alt: debug_config-image
    :figclass: align-left

Running the Hybrid Service
--------------------------
* Steps to running server in debug mode:
	* Start InfluxDB
	* Run External Tools Configurations “proven payara micro 181 [DEBUG CLONE 1]”
	* Run debug  configuration “proven micro 181 hybrid-service node 1”
	* Startup can take several minutes


.. figure:: hybrid_service1.png
    :align: left
    :alt: hybrid_service1-image
    :figclass: align-left
	
.. figure:: hybrid_service2.png
    :align: left
    :alt: hybrid_service2-image
    :figclass: align-left
	
Correct startup should look something like this in the console

.. figure:: startup.png
    :align: left
    :alt: startup-image
    :figclass: align-left

Swagger UI of Debug Interface
-----------------------------
.. figure:: swagger.png
    :align: left
    :alt: swagger-image
    :figclass: align-left
