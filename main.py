import requests
import json

subscriptionId = ""
bearer = ""

defaultUrl = f"https://management.azure.com/subscriptions/{subscriptionId}/"

resourceGroupName = "test4"
virtualNetworkName= "net4"
subnetName= "snet4"
ipName = "ip4"
vmName = "vm4"
apiVersion = "2021-04-01"

def sendHttpRequest(url, json_data, headers):
    # Senden der POST-Anfrage mit dem JSON-Payload
    response = requests.put(url, data=json_data, headers=headers)

    # Überprüfen der Antwort
    if response.status_code == 200:
        print("Erfolgreiche Anfrage")
        response_data = response.json()
        print("Antwortdaten:", response_data)
    else:
        print(f"Fehler bei der Anfrage. Statuscode: {response.status_code}")

def createResourceGroup():
    global json_data, headers
    # create Resourcegroup
    urlCreateResourceGroup = f"{defaultUrl}resourcegroups/{resourceGroupName}?api-version={apiVersion}"
    # JSON-Daten, die Sie senden möchten
    createResourceGroupPayloadData = {
        "location": "westeurope"
    }
    # Umwandeln der Python-Daten in JSON
    json_data = json.dumps(createResourceGroupPayloadData)
    # Festlegen der HTTP-Header, um den Inhaltstyp auf JSON festzulegen
    headers = {"Authorization": f"Bearer {bearer}",
               'Content-Type': 'application/json'}
    sendHttpRequest(urlCreateResourceGroup, json_data, headers)

def createVirtualNetwork():
    global json_data
    # create virtual network
    urlCreateVirtualNetwork = f"{defaultUrl}resourcegroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}?api-version={apiVersion}"
    payloadDataCreateVirtualNetwork = {
        "properties": {
            "addressSpace": {
                "addressPrefixes": [
                    "10.0.0.0/16"
                ]
            },
            "flowTimeoutInMinutes": 10
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVirtualNetwork)
    sendHttpRequest(urlCreateVirtualNetwork, json_data, headers)

def createSubnet():
    global json_data
    # create subnet
    urlCreateSubnet = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}?api-version=2023-05-01"
    payloadDataCreateSubnet = {
        "properties": {
            "addressPrefix": "10.0.0.0/16"
        }
    }
    json_data = json.dumps(payloadDataCreateSubnet)
    sendHttpRequest(urlCreateSubnet, json_data, headers)

def createPublicIpAdress():
    global json_data
    # create public ip adress
    urlCreatePublicIPAdress = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPAddresses/{ipName}?api-version=2023-05-01"
    payloadDataCreatePublicIpAdress = {
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreatePublicIpAdress)
    sendHttpRequest(urlCreatePublicIPAdress, json_data, headers)

def createNetworkInterface():
    global networkInterfaceName, json_data
    # create network interface
    networkInterfaceName = "nic4"
    urlCreateNetworkInterface = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}?api-version=2023-05-01"
    payloadDataCreateNetworkInterface = {
        "properties": {
            "ipConfigurations": [
                {
                    "name": "ipconfig1",
                    "properties": {
                        "publicIPAddress": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/publicIPAddresses/{ipName}"
                        },
                        "subnet": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}"
                        }
                    }
                }
            ]
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateNetworkInterface)
    sendHttpRequest(urlCreateNetworkInterface, json_data, headers)

def createVm():
    global json_data
    # create VM
    urlCreateVM = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}?api-version=2023-07-01"
    payloadDataCreateVM = {
        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Compute/virtualMachines/{vmName}",
        "type": "Microsoft.Compute/virtualMachines",
        "properties": {
            "osProfile": {
                "adminUsername": "jakob",
                "secrets": [

                ],
                "computerName": f"{vmName}",
                "linuxConfiguration": {
                    "ssh": {
                        "publicKeys": [
                            {
                                "path": "/home/jakob/.ssh/authorized_keys",
                                "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD5Z2jjPCFqQz6vI3Hl/Ycrqigbl/i8eVgra1IH5p0cUI57hhoL1WgQStVJuvimgmWb1BaslSjHIwhlm2FiEcLBmhTlePtZYJAA3yAnol2QNb/NsETFwHdGcWUjbFLGg2SB3jV5g+ty0xsBqE0cUWhqREcT0p9EfsUe09oqlQL+m6lIfy2xbeVX7jJjanb3YJj/7ouRuSxdcpHTO265OdeZMYmF+fvaRV57T6A18tLgDaQwJor7UDds3AbnyA85ch7Q/81h+DzVYicllcOmSwG5sFON5Yh+RaVkiW5O9GboOR6TFURoUHXYAghA9xEN5CdUPiwkiGv7ZiFdHl9zkAymqC51KzKawPmpryfVpsoHqXZyXrCN8v519acqI2ALBlxOx5oYTWMJVbK6u/aM9DLnH2b6DfnHFNo1ys2Iq/Xs9yI40ak8M6eEUPh6x4GC6LFMtW5XMdWThGm+upLaiuR7YKrDLXoSWrRBNW5rEIRX3EiSkP4+S44zlFGVV4wZXiM= jakob@LAPTOP-HRNKJDME"
                            }
                        ]
                    },
                    "disablePasswordAuthentication": True
                }
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            },
            "storageProfile": {
                "imageReference": {
                    "sku": "16.04-LTS",
                    "publisher": "Canonical",
                    "version": "latest",
                    "offer": "UbuntuServer"
                },
                "dataDisks": [

                ]
            },
            "hardwareProfile": {
                "vmSize": "Standard_D1_v2"
            },
            "provisioningState": "Creating"
        },
        "name": f"{vmName}",
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVM)
    sendHttpRequest(urlCreateVM, json_data, headers)

createResourceGroup()
createVirtualNetwork()
createSubnet()
createPublicIpAdress()
createNetworkInterface()
createVm()

