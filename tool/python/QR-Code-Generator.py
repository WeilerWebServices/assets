#!/usr/bin/python3

# QR-Code Generator - Install qrcode module -> pip install qrcode

import qrcode as qr
img= qr.make("https://raw.githubusercontent.com/WeilerWebServices/assets/master/docs/licences/FaceGasTHCa/FaceGasTHCa_95794946-f4b2-4396-9084-bf12a06a3015.png")
img.save("/Users/air/Desktop/FaceGasTHCa.png")
