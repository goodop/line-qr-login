import os
import json
import requests
from .server import Server

class Login(object):
    def __init__(self):
        self.server = Server()
        self.e2eeloc = 'main/execbase/e2eeKeys'
        self.tokloc = 'main/execbase/token'

    def login(self, appname=None, sysname=None, cert=None, proxy=None):
        base_url = 'https://gate.execross.pw'
        getqr = '/api/lineqr'
        getpin = '/api/checkpin'
        gettoken = '/api/token'
        apikey = '' # you can use apikey justgood

        if appname is None:
            appname = 'DESKTOPWIN\t8.3.0.3186\tWindows\t10.0' #becarefull when you set your appname

        if sysname is None:
            sysname = 'Asking'

        params1 = {
            'appname': appname,
            'sysname': sysname,
            'apikey': apikey,
            'cert': None,
            'proxy': None
        }
        reqr = requests.post(base_url + getqr, params=params1).json()
        if reqr["status"] == 200:
            das = 'Download this QR code:\n' + reqr['result']['barcode']
            das += '\nOpen and scan your QR code on this link ' + reqr['result']['url']
            print(das)
            session = reqr['result']['session']
            params2 = {
                'session': session,
                'apikey': apikey
            }
            reqpin = requests.post(base_url + getpin, params=params2).json()
            print("Input this PIN code '" + reqpin['result']['pin'] + "' on your LINE for smartphone in 2 minutes.")
            if reqpin["status"] == 200:
                reqtoken = requests.post(base_url + gettoken, params=params2).json()
                dsuccss = 'LINE Login successffully\n'
                if reqtoken['status'] == 200:
                    if 'keyId' in reqtoken['result']:
                        keyid = reqtoken['result']['keyId']
                        privkey = reqtoken['result']['privKey']
                        publickey = reqtoken['result']['pubKey']
                        e2eeVer = reqtoken['result']['e2eeVersion']
                        authToken = reqtoken['result']['authToken']
                        certificate = reqtoken['result']['cert']
                        data = {
                            "keyId": keyid,
                            "privKey": privkey,
                            "pubKey": publickey,
                            "e2eeVersion": e2eeVer
                        }
                        os.makedirs(self.e2eeloc, exist_ok=True)
                        os.makedirs(self.tokloc, exist_ok=True)

                        e2ee_path = os.path.join(self.e2eeloc, f'key_{keyid}.json')
                        with open(e2ee_path, 'w') as json_file:
                            json.dump(data, json_file)

                        token_path = os.path.join(self.tokloc, 'token.txt')
                        with open(token_path, 'w') as token_file:
                            token_file.write(authToken)

                        dsuccss += "\nAuth Token: " + authToken
                        dsuccss += "\nCertificate: " + certificate
                        dsuccss += "\nPrivate Key: " + privkey
                        dsuccss += "\nPublic Key: " + publickey
                        print(dsuccss)
                        return authToken
                    else:
                        authToken = reqtoken['result']['authToken']
                        certificate = reqtoken['result']['cert']
                        data += "\nAuth Token: {authToken}"
                        data += "\nCertificate: {certificate}"
                        print(data)
                        return authToken