# usd_conversion.py
# Ref. Development - IMDB Film Details Jupyter Notebook for more details

import requests
import re

def usd_conversion(native_value):
    # Call Exchange Rates API to look up latest USD exchange rates
    r_usd = 'https://api.exchangeratesapi.io/latest?base=USD'
    usd_response = requests.get(r_usd)
    rates = usd_response.json()
    
    # Parse reported value to determine currency used and remove currency code from string
    native_value = native_value.strip()
    if native_value[0] == '$':
        num_value = native_value.replace('$','')
        exchange_rate = 1
    else:
        currency = native_value[:3]
        exchange_rate = rates['rates'][currency]
        num_value = native_value[3:]
    num_value = num_value.replace(',','')
    if num_value.isnumeric() is True:
        usd_value = float(num_value) / exchange_rate
    else:
        usd_value = None
    return usd_value
