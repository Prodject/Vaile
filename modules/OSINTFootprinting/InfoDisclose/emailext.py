#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    Vaile Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#
#
#Author : @_tID (0xInfection)
#This module requires Vaile Framework
#https://github.com/VainlyStrain/Vaile


import re
import sys
sys.path.append('files/signaturedb/')
import time
import requests as wrn
from core.methods.tor import session
from core.Core.colors import *
links = []
urls = []
found = 0x00
from bs4 import BeautifulSoup
from files.signaturedb.infodisc_signatures import EMAIL_HARVESTER_SIGNATURE as signature
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "This module tries to find email addresses disclosed in target's source code."
searchinfo = "Email hunter"
properties = {}

def mail0x00(url):
    requests = session()
    #print(R+'\n    ======================')
    #print(R+'     EMAIl INFO HARVESTER')
    #print(R+'    ======================\n')
    from core.methods.print import pleak
    pleak("email info harvester")
    time.sleep(0.5)
    links = [url]
    po = url.split('//')[1]
    for w in links:
        print(GR+' [*] Scraping Page: '+O+url)
        req = requests.get(w).text
        check0x00(req)

    soup = BeautifulSoup(req,'lxml')
    for line in soup.find_all('a', href=True):
        newline = line['href']
        try:
            if newline[:4] == "http":
                if po in newline:
                    urls.append(str(newline))
            elif newline[:1] == "/":
                combline = url+newline
                urls.append(str(combline))
        except:
            print(R+' [-] Unhandled Exception Occured!')

    try:
        for uurl in urls:
            print(G+"\n [+] Scraping Page: "+O+uurl)
            req = requests.get(uurl).text
            check0x00(req)

    except:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+'\n [-] No Emails found disclosed in plaintext in source code!\n')

    print(G+' [+] Scraping Done!')

def check0x00(req):
    comments = re.findall(signature,req)
    print(GR+" [*] Searching for Emails...")
    if comments:
        print(G+'\n [+] Found Email(s):')
        for comment in comments:
            print(C+'   - '+comment)
            time.sleep(0.03)
            found = 0x01

def emailext(web):

    print(GR+' [*] Loading module...')
    time.sleep(0.6)
    mail0x00(web)

def attack(web):
    emailext(web)