"""
Created on Sat Dec 10 12:34:24 2022

@author: Suganthi
"""

# -*- coding: utf-8 -*-
import requests
import pandas as pd
import json

API_DOMAIN="http://ai-marketplace-3.uni-paderborn.de"
API_BASE_PATH="api/v1/collection/specification"

with requests.Session() as session:
    # provide authentication data to session, will be sent automatically
    session.auth = ('caddok', '')
    identifier_key = list()

    # Use the first request, which uses basic authentication, 
    # to set the language using the cookie
    header_response = session.get(API_DOMAIN, 
                                  cookies={'contact.language': 'en'})
    #If the connection request is successful, perform below operations
    if header_response.status_code == 200:        
        token_response = session.get(f"{API_DOMAIN}/{API_BASE_PATH}")
        token = token_response.json()
        
        identifier_key = list()
        requirement_df = list()
        for item in token["objects"]:
            responses=list()
            identifier_key.append(item["spec_id"])
            #print(item["spec_id"])
            print(item['system:relships']['relships']['Requirements'])
            data_response=session.get(item['system:relships']
                                      ['relships']['Requirements'], 
                                      headers={'Accept': 
                                               'multipart/form-data'})
            data=data_response.json()
            data_target=data.get('targets')
            for item in data_target:
                data_from_api=json.loads(session.get(item).text)
                responses.append(data_from_api)
            requirement_df.append(pd.DataFrame(responses))
            #print(requirement_df[-1].head())        
        df = pd.concat(requirement_df, keys=identifier_key).reset_index().drop(
            ['level_1'], axis=1).rename(columns = {'level_0':'SPEC_ID_KEY'})
        #print(df.head())
        print(df.shape)
        df
session.get('http://localhost/server/__quit__')      