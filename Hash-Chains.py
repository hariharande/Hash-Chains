#! /usr/bin/python
import socket
import sys
import json
import time
import random, base64
import binascii
import ast
import crypt
from hashlib import sha1


def reducer(pw):
        r = pw[::-1][:8]
        red = ""
        for i in range (0, len(r)):
                red = red + chr((ord(r[i]) % 26) + 97)
        return red

def find_start(pw):
        count = 0
        while True:
                r = reducer(pw)
                if hash_dict.has_key(r):
                        return hash_dict[r], pw
                if count == 65536:
                        break
                else:
                        pw = crypt.crypt(r, '$1$HUSKIES!$')
                count += 1

def find_pwd(start, pw):
        count = 0
        while True:
                password = crypt.crypt(start, '$1$HUSKIES!$')
                if password == pw:
                        return start
                if count == 65536:
                        break
                else:
                        start = reducer(password)
                count += 1

try:
        f = open("/home/hash-chain/table.json", "r")
        contents = f.read()
        table1 = contents.split("[")[1]
        table = table1.split("]")[0]
        entries = table.split('"},{"')
        hash_dict = {}
        count = 0
        for entry in entries:
                count += 1
                se = entry.split('","')
                s = se[0].split('":"')[1]
                e = se[1].split('":"')[1]
                if count == len(entries):
                        e = e.replace('"}', '')
                hash_dict[e] = s

        hash_list = ['$1$HUSKIES!$v/mh7SBLm8/3SBL6w0Z9M1', '$1$HUSKIES!$xk2VnxpJYAGOxEl0W8uEP0','$1$HUSKIES!$R9bstTQ9eG2Pzql0cq7kd/']
        for pw  in hash_list:
                count = 0
                start, red = find_start(pw)
                password = find_pwd(start, pw)
                print "password = ", password

        password_set = set()
        count = 0
        for end,start in hash_dict.items():
                #count = 0
                while start != end:
                        start = reducer(crypt.crypt(start, '$1$HUSKIES!$'))
                        if start in password_set:
                                break
                        password_set.add(start)
                print count, len(password_set)
                count += 1

        print len(password_set)
finally:
        print "end"
