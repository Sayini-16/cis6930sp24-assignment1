
import re
import sys
import nltk
import spacy
from spacy.matcher import Matcher
from spacy_download import load_spacy
from commonregex import CommonRegex
from nltk.corpus import wordnet as wn

nlp = load_spacy("en_core_web_sm")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')

block = '\u2588'

def names(data):
    name_list = []
    doc = nlp(data)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            name = ent.text
            if name not in name_list:
                name_list.append(name)
    #print(name_list)
    return data, name_list

def dates(data):
    doc = nlp(data)
    dates=[]
    for ent in doc.ents:
        if ent.label_ == "DATE":
            #print(ent.text)
            dates.append(ent.text)
            #print(dates)
    return data, dates
    

def addresses(data):
    #print(1)
    matcher = Matcher(nlp.vocab)
    address_pattern = [
        {'SHAPE': 'dddd'},             # 4 digits for house number
        {'IS_ALPHA': True,},           # Street name
        {'IS_ALPHA': True, 'OP': '?'}, # Optional street name part
        {'IS_ALPHA': True, 'OP': '?'}, # Optional street name part
        {'IS_PUNCT': True, 'OP': '?'}, # Optional punctuation
        {'ORTH': 'St', 'OP': '?'},     # Street suffix
        {'ORTH': 'Street', 'OP': '?'}, # Street suffix
        {'ORTH': 'Ave', 'OP': '?'},    # Avenue suffix
        {'ORTH': 'Avenue', 'OP': '?'}, # Avenue suffix
    ]

    # Add the pattern to the matcher
    matcher.add('ADDRESS', [address_pattern])
    doc = nlp(data)
    matches = matcher(doc)
    #print(matches)
    addresses = []
    for match_id, start, end in matches:
        span = doc[start:end]  # The matched span
        addresses.append(span.text)
    #print(addresses)
    return data , addresses

def phones(data):
    parsed_text = CommonRegex(data)
    if not data:  # Check if data is empty
        return data, [] 
    phones_list = parsed_text.phones
    return data, phones_list


def redact(names_list, dates, address_list, phones_list, data):
    for elm in names_list + dates + address_list + phones_list:
        data = re.sub(r'\b' + elm + r'\b', len(elm) * block, data)
    return data

def stats(names_list, dates, address_list, phones_list, f):
    status = f"Status for the file {f}\n"
    total = len(names_list) + len(address_list) + len(phones_list) + len(dates)
    status += f"The following number of names are redacted from the file {len(names_list)} \n"
    status += f"The following number of dates are redacted from the file {len(dates)} \n"
    status += f"The following number of addresses are redacted from the file {len(address_list)} \n"
    status += f"The following number of phones are redacted from the file {len(phones_list)} \n"
    status += f"The total number of redactions in the file are {total} \n"

    return status
