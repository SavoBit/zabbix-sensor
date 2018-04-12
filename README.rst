======================
Zabbix Sensor
======================
Introduction:
	- Zabbix is an open source network monitoring tool that can be used to monitor the performance and availability of the server, network devices and other network components.
	- Zabbix uses a Zabbix agent on the monitored device to collect the data and send it to the Zabbix server.
	
Objective:
	- Zabbix Server will measure network latency by collecting Response Time data coming from Zabbix Agents and then send it to the monitoring layer via Kafka.
	

======================
Requirements
======================
	- Zabbix server with Ubuntu installed.
	- MySQL
	- Appache Service
	- Zookeeper
	- Kafka

for more information: https://www.zabbix.com/documentation/3.2/manual/installation/requirements


======================
Installation
======================
Download Zabbix:
	# wget http://repo.zabbix.com/zabbix/3.2/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.2-1+xenial_all.deb
	# dpkg -i zabbix-release_3.2-1+xenial_all.deb
	# apt-get update

Install Zabbix server and web frontend with MySQL database:
	# apt-get install zabbix-server-mysql zabbix-frontend-php	

Install Zabbix agent (only on Client machine):
	# apt-get install zabbix-agent

Install frontend:
	- open Zabbix URL: http://<server_ip_or_name>/zabbix and follow the frontend installation wizard.
	- More information on: https://www.zabbix.com/documentation/3.2/manual/installation/install#installing_frontend


======================
Configuration
======================
1. Zabbix server:

 Database configuration:
	# vi /etc/zabbix/zabbix_server.conf
	- DBHost=localhost
	- DBName=zabbix
	- DBUser=zabbix
	- DBPassword=<password>; where DBPassword is the password you've set creating initial database.

 Apache configuration file for Zabbix frontend:
	# vi /etc/zabbix/apache.conf
	- uncomment the “date.timezone” setting and set the right timezone for you.

 Finally, start Apache server and Zabbix server and enable them to start on boot time:
	# sudo systemctl restart apache2
	# sudo systemctl restart zabbix-server
	# sudo systemctl enable apache2
	# sudo systemctl enable zabbix-server

2. Zabbix Agent:

 Open the Zabbix agent default configuration file located at /etc/zabbix/zabbix_agentd.conf:
	- Server=IP address of Zabbix Server
	- ServerActive=IP address of Zabbix Server
	- Hostname=Zabbix-Client
	
 Restart Zabbix agent and enable it to start on boot time:
	- sudo systemctl restart zabbix-agent
	- sudo systemctl enable zabbix-agent
	
3. Add Zabbix Client Machine to Zabbix Server for Monitoring:
 
 Move to the Zabbix server web interface
 
 Discovery rules configuration: configuration>Discovery>Creat discovery rule:
	- Name: AutoDiscoveryName
	- Discovery by proxy: No proxy
	- IP range: The IP range of the clients being monitored.
	- Delay (in sec): 10
	- Checks: Zabbix agent "system.uname"
	- Device uniqueness criteria: Zabbix agent "system.uname"
	- Add

 Actions configuration: configuration>Actions>Creat action:
	- Conditions:
		# Discovery rule = AutoDiscoveryName	
		# Received value like Linux	
		# Discovery status = Up	
		# Service type = Zabbix agent
	- Operations:
		# Add to host groups: Linux servers
		# Link to templates: Template OS Linux
		# Link to templates: Template ICMP Ping; where Template ICMP Ping has ICMP response time Item
		
		
		
======================
Usage
======================

On Zookeeper folder:
	# sudo bin/zkServer.sh start

On Kafka folder:
	# bin/kafka-server-start.sh config/server.properties
	
To send collected data to the monitoring layer via Kafka, Run the script:
	# nohup python zabbix_Kafka.py &