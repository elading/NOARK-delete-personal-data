import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

from datetime import datetime
import io

import re
import os


# Logging:

import logging
import sys

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    filename = r"C:\Users\eirlad\OneDrive - Arkivverket\Skrivebord\Python-greier\skript NOARK\logglogg.log",
    level = logging.DEBUG,
    format = LOG_FORMAT,
    filemode = "w")
    
logger = logging.getLogger()


# 

content_folder = r'C:\Users\eirlad\OneDrive - Arkivverket\Skrivebord\Uttrekk eksempler\NOARK-uttrekk\41505334-eb37-41a3-b7c2-fa385342625b\content2'
xml_file = content_folder + r'\arkivstruktur.xml'


root = ET.parse(xml_file).getroot()

arkivstruktur_iter = ET.parse(xml_file).iter()

# 


delete_dicts = []

arkivstruktur_iter = ET.parse(xml_file).iter()
for element in arkivstruktur_iter:
    if str(element.tag) == "{http://www.arkivverket.no/standarder/noark5/arkivstruktur}dokumentbeskrivelse":
        dokumentobjekt = element.find("{*}dokumentobjekt")
        
        if element.find("{*}skjerming"):
            skjerming_data = element.find("{*}skjerming")[0].text
        
            if element.find("{*}skjerming")[0].text == "Personalforvaltning":
                filsti = dokumentobjekt.find("{*}referanseDokumentfil").text
                #delete_dict
                delete_dicts.append({"id":element[0].text, "skjerming":skjerming_data, "filsti":filsti}.copy())
        else:
            skjerming_data = "ikke skjermet"
            filsti = ''

        print((element[0].text, skjerming_data, filsti))
    

# Overwrite personal data

arkivstruktur_iter = ET.parse(xml_file).iter()
for element in arkivstruktur_iter:
    if str(element.tag) == "{http://www.arkivverket.no/standarder/noark5/arkivstruktur}mappe":
            if element.find("{*}skjerming") and ("personal" in element.find("{*}skjerming")[0].text or "Personal" in element.find("{*}skjerming")[0].text):
                element.find("{*}tittel").text = "PERSONALINFORMASJON"
                for registering in element.findall("{*}registrering"):
                    registering.find("{*}tittel").text = "PERSONALINFORMASJON"
                    for dokumentbeskrivelse in registering.findall("{*}dokumentbeskrivelse"):
                        dokumentbeskrivelse.find("{*}tittel").text = "PERSONALINFORMASJON"        
                        for dokumentobjekt in dokumentbeskrivelse.findall("{*}dokumentobjekt"):
                            dokumentobjekt.find("{*}referanseDokumentfil").text = "KASSERES" 
                    for korrespondansepart in registering.findall("{*}korrespondansepart"):
                        for partelement in korrespondansepart:
                            partelement.text = "PARTINFORMASJON"
                ET.dump(element)

#Delete files:


for dict in delete_dicts:
    try:
        os.remove(content_folder + '\\' + dict['filsti'])
        print( dict['id'] + " : " + "Filen " + dict['filsti'] + " ble slettet." + datetime.datetime.now())
        
        logger.info(dict['id'] + " : " + "Filen " + dict['filsti'] + " ble slettet.")
    except FileNotFoundError:
        logger.error(dict['id'] + " : " + "Filen " + dict['filsti'] + " ble ikke funnet.")

