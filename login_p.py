import time
import base64
import rsa
import binascii
import requests
import re
import urllib

#username = sinaSSOEncoder.base64.encode(urlencode(username));
def get_su(username):
    return base64.b64encode(urllib.quote(username).encode("utf-8")).decode("utf-8")

def get_pwd(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    print 'rsaPublickey' + ' ' + str(rsaPublickey )
    key = rsa.PublicKey(rsaPublickey,65537)
    print key
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    message = message.encode("utf-8")
    print 'message' + ' ' + str(message)
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    return passwd

print get_pwd('ws9302160011','1489365548','WU4LG7',"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443")
