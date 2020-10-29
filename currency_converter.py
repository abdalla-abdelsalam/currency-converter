import json
import requests
import os
from dotenv import load_dotenv
from pathlib import Path


def load_env():
        env_path=Path('.')/'.env'
        load_dotenv(dotenv_path=env_path)
        print(API_ACCESS_KEY)
        

def get_help():
    with open('currency_code.txt','r') as file:
        print(file.read())
    exit()


def start():
    print(" if you want to get some help about currency code type help ")
    from_currency=input(" enter currency code that you want to convert from ")
    if from_currency.lower()=='help':
        get_help()
    to_currency=input(" enter currency code that you want to convert from ")

    if to_currency.lower()=='help':
        get_help()

    return from_currency.upper(),to_currency.upper()


def api_request(from_currency,to_currency):
    
    try:
        API_ACCESS_KEY=os.environ.get("API_ACCESS_KEY")
        res=requests.get(f"https://v6.exchangerate-api.com/v6/{API_ACCESS_KEY}/latest/{from_currency}")
        if res.status_code!=200:
            raise Exception("invalid-key")
        json_obj=json.loads(res.text)
        if(json_obj['result']!='success'):
            raise Exception(json_obj['error-type'])
    except Exception as exc:
        print(exc)
        exit()
    else:
        try:
            result=json_obj['conversion_rates'][to_currency]
            time_last_update=json_obj['time_last_update_utc']
        except Exception:
            print("unsupported-code")
            exit()

    return result,time_last_update
    

def print_result(result,time_last_update,from_currency,to_currency):
    print(f'{from_currency} is equal to {result} {to_currency}')
    print(f'time since last update: {time_last_update}')


if __name__=="__main__":
    load_dotenv()
    from_currency,to_currency=start()
    result,time_last_update=api_request(from_currency,to_currency)
    print_result(result,time_last_update,from_currency,to_currency)

