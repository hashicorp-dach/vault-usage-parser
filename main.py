#!/usr/bin/python3
import json
import requests
import os
import sys

# Read a JSON file with usage metrics data from Vault
# Parses the data to get the namespace path and the associated client count
def parseFile(file_path):
    data = []
    for path in file_path:
        with open(path, "r") as json_input:
            json_parse = json.loads(json_input.read())
            
            for i in json_parse["by_namespace"]:
                data.append([i["namespace_path"],i["counts"]["clients"]])

    exportData(data)

# Requests Client Count data from Vaults usage metrics API
# Parses the data to get the namespace path and the associated client count     
def parseAPI(): 
    request_header = { "Content-Type": "application/json",'X-Vault-Token': vault_token, "X-Vault-Namespace": vault_namespace}
    
    try:
        vault_request = requests.get(vault_addr, headers=request_header) 
        #vault_request_monthly = request.get(vault_addr+"/monthly", headers=request_header)
    except:
        print("Vault API request failed")
        exit()
    
    json_parse = vault_request.json()
    data = []

    for i in json_parse["data"]["by_namespace"]:
        data.append([i["namespace_path"],i["counts"]["clients"]])

    exportData(data)

# Prints the RAW data from parseFile() and parseAPI() to stdout
# Groups data based on namespace path and prints it to stdout
def exportData(data):
    
    #Print Raw data to stdout
    print("{:<50} {:<15} {}".format('NAMESPACE','CLIENTS','\n'))
    for x in data:    
        print("{:<50} {:<15}".format(x[0],x[1]))

    #Group data by top level namespace path // current depth 2 e.g. /root/ns1
    grouped_namespaces = {}
    
    for i in data:
        namespace_slice = i[0].split("/")[0] + "/" + i[0].split("/")[1]
        #namespace_slice = i[0]
        if namespace_slice not in grouped_namespaces: 
            grouped_namespaces[namespace_slice] = i[1]
        else:
            grouped_namespaces.update({namespace_slice: grouped_namespaces[namespace_slice]+i[1]})
    
    print("{}{:<50} {:<15} {}".format('\n','GROUPED NAMESPACES','CLIENTS','\n'))
    
    for key, value in grouped_namespaces.items():
       print("{:<50} {:<15}".format(key, value))

# If a file path is given as a commandline arg parse this file
# If no arg is given call the Vault API based on the env vars connection information
if len(sys.argv) >= 2:
    sys.argv.pop(0)
    parseFile(sys.argv)
else:
    try:
        vault_addr = os.environ["VAULT_ADDR"] + "/v1/sys/internal/counters/activity/monthly"
        vault_token = os.environ["VAULT_TOKEN"]
        vault_namespace = os.environ["VAULT_NAMESPACE"]
    except:
        print("No env variables set defaults will be used")
        vault_addr = "http://localhost:8200" + "/v1/sys/internal/counters/activity/monthly"
        vault_token = "root"
        vault_namespace = "root"
    parseAPI()