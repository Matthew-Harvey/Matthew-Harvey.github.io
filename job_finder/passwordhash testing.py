import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
import pickle
import random
from tkinter import *
import time
import sys
import io
import re
from bs4 import BeautifulSoup
import requests
from lxml import html
import urllib3
import hashlib
import os
import my_module
import binascii

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

password = "test"
password = hash_password(password)
print(password)

print(verify_password(password, "test"))
