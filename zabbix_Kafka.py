from pyzabbix import ZabbixAPI
from datetime import datetime
import time
from pprint import pprint
import json
from kafka import SimpleProducer, KafkaClient, KafkaProducer
import requests



def main():
    while True:

        # The hostname at which the Zabbix web interface is available
        zapi = ZabbixAPI('http://10.4.0.14/zabbix')
        zapi.login("Admin", "zabbix")


        data = zapi.item.get(output = "extend")
        hostids= zapi.hostinterface.get(output = "extend")
        jsonResponseTime = { "data": [] }
        for member in data:
            if member['key_']== "icmppingsec":
               for ipHost in hostids:
                   if ipHost['hostid']== member['hostid']:
                      response = { "timestamp":member['lastclock'],"ipAddress": ipHost['ip'], "responseTime": member['lastvalue']}
                      jsonResponseTime['data'].append(response)
        print(json.dumps(jsonResponseTime))
        # Send to Kafka
        producer = KafkaProducer(bootstrap_servers=['10.255.255.151:9092'])
        producer.send('zabbix', json.dumps(jsonResponseTime).encode('utf-8'))
        time.sleep(10)

if __name__ == "__main__":
    main()

