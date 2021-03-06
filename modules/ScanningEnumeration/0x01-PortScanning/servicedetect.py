#!/usr/bin/env python3
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    Vaile Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This script is a part of Vaile Framework
#https://github.com/VainlyStrain/Vaile


import time
import sys
import os
import socket
import scapy
from scapy.all import *
from multiprocessing import Pool, TimeoutError
from core.methods.multiproc import listsplit
from core.variables import processes
from core.Core.colors import *

info = "This module tries to find out what services the target is running."
searchinfo = "Service Detection"
properties = {"INIT":["Start of port range to scan.", " "], "FIN":["End of the port range to scan.", " "], "VERBOSE":["Verbose Output? [1/0]", " "]}

# feel free to add your own :)
common_ports = {
'20': 'FTP',
'21': 'FTP',
'22': 'SSH',
'23': 'TELNET',
'25': 'SMTP',
'53': 'DNS',
'67': 'DHCP',
'68': 'DHCP',
'69': 'TFTP',
'80': 'HTTP',
'109': 'POP2',
'110': 'POP3',
'111': 'RPCBIND',
'123': 'NTP',
'137': 'NETBIOS-NS',
'138': 'NETBIOS-DGM',
'139': 'NETBIOS-SSN',
'143': 'IMAP',
'156': 'SQL-SERVER',
'161': 'SNMP',
'162': 'SNMP II',
'179': 'BGP',
'389': 'LDAP',
'443': 'HTTPS',
'445': 'NETBIOS-SSN',
'512': 'EXEC',
'513': 'LOGIN',
'546': 'DHCP-CLIENT',
'547': 'DHCP-SERVER',
'636': 'LDAPS',
'995': 'POP3-SSL',
'993': 'IMAP-SSL',
'1099': 'RMI-REGISTRY',
'2121': 'FTP',
'2049': 'NFS',
'2086': 'WHM/CPANEL',
'2087': 'WHM/CPANEL',
'2082': 'CPANEL',
'2083': 'CPANEL',
'3306': 'MYSQL',
'3632': 'DISTCC',
'5061': 'SIP-TLS',
'5432': 'POSTGRESQL',
'5900': 'VNC',
'6000': 'X11',
'6667': 'IRC',
'8009': 'AJP13',
'8080': 'HTTP PROXY',
'8180': 'HTTP',
'8443': 'PLESK',
'10000': 'VIRTUALMIN/WEBMIN'
}

def portloop(portlist, host, verbose):
    open = []
    closed = []
    for p in portlist:
        if verbose:
            response = check_portv(host, p)
        else:
            response = check_port(host, p)
        if response == 0:
            print(''+G+' [!] Port ' +O+ str(p) +G+ ' detected Open !')
            open.append(p)
        else:
            if verbose:
                print(''+R+' [!] Port ' +O+ str(p) +R+ ' detected Closed !')
            closed.append(p)
    return (open, closed)

def get_servicev(port):
    port = str(port)
    if port in common_ports:
        return common_ports[port]
    else:
        return 0

def check_portv(host, port, result = 1):

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        print(C+"\n [*] Connecting to '%s' via port %s" % (host, port))
        r = sock.connect_ex((host, port))
        #print(GR+' [*] Analysing results...')
        time.sleep(0.0015)

        if r == 0:
            result = r

        sock.close()

    except Exception as e:
        print(''+R+' [!] Exception detected at port %s !' % port)
        pass

    return result

def check_port(host, port, result = 1):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((host, port))
        if r == 0:
            result = r
        sock.close()
    except:
        pass

    return result

def get_service(port):
    port = str(port)
    if port in common_ports:
        return common_ports[port]
    else:
        return 0

def service0x00(host):

    #print(R+'\n   ===================================')
    #print(R + "    S E R V I C E   D E T E C T I O N")
    #print(R + '   ===================================\n')
    from core.methods.print import pscan
    pscan("service detection")
    if properties["INIT"][1] == " ":
        start_port = input(O+' [#] Enter initial port :> ')
    else:
        start_port = properties["INIT"][1]
    if properties["FIN"][1] == " ":
        end_port = input(O+' [#] Enter ending port :> ')
    else:
        end_port = properties["FIN"][1]

    start_port = int(start_port)
    end_port = int(end_port)

    open_ports = []
    closed_ports = []

    try:
        ip = socket.gethostbyname(host)
        print(G+'\n [+] Target server detected up and running...')
        print(GR+' [*] Preparing for scan...')
        pass
    except:
        print(R+' [-] Server not responding...')
        time.sleep(0.3)
        print(R+' [*] Exiting...')
        quit()

    if properties["VERBOSE"][1] == " ":
        mn = input(O+'\n [*] Do you want a verbose output (enter if not) :> ')
        verbose = mn is not ""
    else:
        verbose = properties["VERBOSE"][1] == "1"
    if verbose:
        print(''+G+'\n [+] Verbose mode selected !\n')
        print(GR+" [!] Scanning %s from port %s - %s: " % (host, start_port, end_port))
    print(B+" [*] Scanning started at %s" %(time.strftime("%I:%M:%S %p")))
    starting_time = time.time()
    try:
        if verbose:
            print(O+" [*] Scan in progress..")
            time.sleep(0.8)
        portrange = range(start_port, end_port+1)
        prtlst = listsplit(portrange, round(len(portrange)/processes))
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(portloop, args=(l,host,verbose,)) for l in prtlst]
            #res1 = pool.apply_async(portloop, )
            for i in res:
                j = i.get()
                open_ports += j[0]
                closed_ports += j[1]

        print(G+"\n [+] Scanning completed at %s" %(time.strftime("%I:%M:%S %p")))
        ending_time = time.time()
        total_time = ending_time - starting_time
        print(G+' [*] Preparing report...\n')
        time.sleep(1)
        print(O+' ——·+-------------+')
        print(O+'    [ SCAN REPORT ]    services')
        print(O+'    +-------------+   -----------')
        print(O+'             ')
        print()
        print(O+'    +--------+----------+-----------+')
        print(O+'    |  '+GR+'PORT  '+O+'|  '+GR+'STATE   '+O+'|  '+GR+'SERVICE  '+O+'|')
        print(O+'    +--------+----------+-----------+')

        if open_ports:
            for i in sorted(open_ports):
                service = get_servicev(i)
                if not service:
                    service = "Unknown"
                m = str(service)
                c = str(i)
                if len(c) == 1:
                    print(O+'    |   '+C+c+O+'    |   '+G+'OPEN   '+O+'|  '+B+m+'')
                    print(O+'    +--------+----------+-----------+')
                    time.sleep(0.2)
                elif len(c) == 2:
                    print(O+'    |   '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                    print(O+'    +--------+----------+-----------+')
                    time.sleep(0.2)
                elif len(c) == 3:
                    print(O+'    |  '+C+c+'   '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                    print(O+'    +--------+----------+-----------+')
                    time.sleep(0.2)
                elif len(c) == 4:
                    print(O+'    |  '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                    print(O+'    +--------+----------+-----------+')
                    time.sleep(0.2)
                elif len(c) == 5:
                    print(O+'    | '+C+c+'  '+O+'|   '+G+'OPEN   '+O+'|   '+B+m+'')
                    print(O+'    +--------+----------+-----------+')
                    time.sleep(0.2)
        else:
            print(R+"\n [-] No open ports found.!!\n")
        print(B+'\n [!] ' + str(len(closed_ports)) + ' closed ports not shown')
        print(G+" [+] Host %s scanned in %s seconds\n" %(host, total_time))

    except KeyboardInterrupt:
        print(R+"\n [-] User requested shutdown... ")
        print(' [-] Exiting...\n')
        quit()


def servicedetect(web):

    print(GR+' [*] Loading up scanner...')
    time.sleep(0.5)
    if 'http://' in web:
        web = web.replace('http://','')
    elif 'https://' in web:
        web = web.replace('https://','')
    else:
        pass
    service0x00(web)

def attack(web):
    servicedetect(web)