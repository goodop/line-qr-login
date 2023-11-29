import os
import json
import requests, time
from .server import Server

class Login(object):
    def __init__(self):
        self.server = Server()
        self.e2eeloc = '../execross/execbase/e2eekeys'
        self.tokloc = '../execross/execbase/token'
        self.base_url = 'https://gate.execross.pw'
        self.apikey = 'execmans' #You can put justgood password here


    def login(self, appname=None, sysname=None, cert=None, proxy=None):
        getqr = '/api/lineqr'
        getpin = '/api/checkpin'
        gettoken = '/api/token'

        if appname is None:
            appname = 'DESKTOPWIN\t8.3.0.3186\tWindows\t10.0' #becarefull when you set your appname

        if sysname is None:
            sysname = 'Asking'
        print(cert)
        params1 = {
            'appname': appname,
            'sysname': sysname,
            'apikey': self.apikey,
            'cert': cert,
            'proxy': None
        }
        reqr = requests.post(self.base_url + getqr, params=params1).json()
        if reqr["status"] == 200:
            das = 'Download this QR code:\n' + reqr['result']['barcode']
            das += '\nOpen and scan your QR code on this link ' + reqr['result']['url']
            print(das)
            session = reqr['result']['session']
            params2 = {
                'session': session,
                'apikey': self.apikey
            }
            reqpin = requests.post(self.base_url + getpin, params=params2).json()
            print("Input this PIN code '" + reqpin['result']['pin'] + "' on your LINE for smartphone in 2 minutes.")
            if reqpin["status"] == 200:
                reqtoken = requests.post(self.base_url + gettoken, params=params2).json()
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
                        dsuccss += "\nAuth Token: {authToken}"
                        dsuccss += "\nCertificate: {certificate}"
                        print(dsuccss)
                        return authToken

## TOKEN VERSION 3
    def loginV2(self, appname=None, sysname=None, cert=None, proxy=None):
        getqr = '/api/lineqrV2'
        getpin = '/api/checkpinV2'
        gettoken = '/api/tokenV2'

        if appname is None:
            appname = 'DESKTOPWIN\t8.4.1.3186\tWindows\t10.0' #becarefull when you set your appname

        if sysname is None:
            sysname = 'Asking'
        print(cert)
        params1 = {
            'appname': appname,
            'sysname': sysname,
            'apikey': self.apikey,
            'cert': cert,
            'proxy': None
        }
        reqr = requests.post(self.base_url + getqr, params=params1).json()
        if reqr["status"] == 200:
            das = 'Download this QR code:\n' + reqr['result']['barcode']
            das += '\nOpen and scan your QR code on this link ' + reqr['result']['url']
            print(das)
            session = reqr['result']['session']
            params2 = {
                'session': session,
                'apikey': self.apikey
            }
            reqpin = requests.post(self.base_url + getpin, params=params2).json()
            if reqpin["status"] == 200:
                if 'authToken' not in reqpin['result']:
                    print("Input this PIN code '" + reqpin['result']['pin'] + "' on your LINE for smartphone in 2 minutes.")
                    reqtoken = requests.post(self.base_url + gettoken, params=params2).json()
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
                            dsuccss += "\nAuth Token: {authToken}"
                            dsuccss += "\nCertificate: {certificate}"
                            print(dsuccss)
                            return authToken
                else:
                    dsuccss = 'LINE Login successffully\n'
                    keyid = reqpin['result']['keyId']
                    privkey = reqpin['result']['privKey']
                    publickey = reqpin['result']['pubKey']
                    e2eeVer = reqpin['result']['e2eeVersion']
                    authToken = reqpin['result']['authToken']
                    certificate = reqpin['result']['cert']
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

    
    def loginEmail(self, email=None, passwd=None, appname=None, sysname=None, cert=None, proxy=None):
        logemail = '/api/lineemail'
        etoken = '/api/etoken'

        if appname is None:
            appname = 'DESKTOPWIN\t8.3.0.3186\tWindows\t10.0'

        if sysname is None:
            sysname = 'Asking'

        params1 = {
            'appname': appname,
            'sysname': sysname,
            'apikey': self.apikey,
            'cert': cert,
            'proxy': None,
            'email': email,
            'passwd': passwd
        }
        reqpin = requests.post(self.base_url + logemail , params=params1).json()
        if reqpin['status'] == 200:
            if 'authToken' in reqpin['result']:
                dsuccss = 'LINE Login successffully\n'
                authToken = reqpin['result']['authToken']
                certificate = reqpin['result']['cert']
                dsuccss += "\nAuth Token: {authToken}"
                dsuccss += "\nCertificate: {certificate}"
                print(dsuccss)
                os.makedirs(self.tokloc, exist_ok=True)
                token_path = os.path.join(self.tokloc, 'token.txt')
                with open(token_path, 'w') as token_file:
                    token_file.write(authToken)
                return authToken
            else:                
                print("Input this PIN code '" + reqpin['result']['pin'] + "' on your LINE for smartphone in 2 minutes.")
                params2 = {
                   'apikey': self.apikey
                }
                reqtoken = requests.post(self.base_url + etoken , params=params2).json()
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
                        dsuccss += "\nAuth Token: {authToken}"
                        dsuccss += "\nCertificate: {certificate}"
                        print(dsuccss)
                        return authToken

## TOKEN VERSION 3
    def loginEmailV2(self, email=None, passwd=None, appname=None, sysname=None, cert=None, proxy=None):
        logemail = '/api/lineemailV2'
        etoken = '/api/etokenV2'

        if appname is None:
            appname = 'DESKTOPWIN\t8.3.0.3186\tWindows\t10.0'

        if sysname is None:
            sysname = 'Asking'

        params1 = {
            'appname': appname,
            'sysname': sysname,
            'apikey': self.apikey,
            'cert': cert,
            'proxy': None,
            'email': email,
            'passwd': passwd
        }
        reqpin = requests.post(self.base_url + logemail , params=params1).json()
        if reqpin['status'] == 200:
            if 'authToken' in reqpin['result']:
                dsuccss = 'LINE Login successffully\n'
                authToken = reqpin['result']['authToken']
                certificate = reqpin['result']['cert']
                dsuccss += "\nAuth Token: {authToken}"
                dsuccss += "\nCertificate: {certificate}"
                print(dsuccss)
                os.makedirs(self.tokloc, exist_ok=True)
                token_path = os.path.join(self.tokloc, 'token.txt')
                with open(token_path, 'w') as token_file:
                    token_file.write(authToken)
                return authToken
            else:                
                print("Input this PIN code '" + reqpin['result']['pin'] + "' on your LINE for smartphone in 2 minutes.")
                params2 = {
                   'apikey': self.apikey
                }
                reqtoken = requests.post(self.base_url + etoken , params=params2).json()
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
                        dsuccss += "\nAuth Token: {authToken}"
                        dsuccss += "\nCertificate: {certificate}"
                        print(dsuccss)
                        return authToken
