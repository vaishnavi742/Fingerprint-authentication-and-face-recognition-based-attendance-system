#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
import tkinter as tk
from tkinter import * 
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
root1 = tk.Tk()
root1.configure(background="lightblue")
root1.geometry("600x200")
root1.title("Person Identification Using Face Detection & Fingerprint Detection")
## Search for a finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash

print('Waiting for finger...')

## Wait that finger is read
while ( f.readImage() == False ):
    pass

## Converts read image to characteristics and stores it in charbuffer 1
f.convertImage(0x01)

## Searchs template
result = f.searchTemplate()

positionNumber = result[0]
accuracyScore = result[1]

if ( positionNumber == -1 ):
    print('No match found!')
    label_2 = tk.Label(root1, text="Opps!!!Fingerprint Not authenticated.",font=("bold", 20),bg="Red",fg="Black")
    label_2.place(x=10,y=50)
else:
    print("Fingerprinbt Successfully authenticated")
    print('Found template at position #' + str(positionNumber))
    print('The accuracy score is: ' + str(accuracyScore))
    label_2 = tk.Label(root1, text="Fingerprint authenticated Successfully...",font=("bold", 20),bg="Green",fg="Black")
    label_2.place(x=10,y=50)
## OPTIONAL stuff
##

## Loads the found template to charbuffer 1
f.loadTemplate(positionNumber, 0x01)

## Downloads the characteristics of template loaded in charbuffer 1
characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

## Hashes characteristics of template
print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

