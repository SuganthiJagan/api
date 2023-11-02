import numpy as np
import trimesh
import pandas as pd
import requests

API_DOMAIN="xxxx"
API_BASE_PATH="xxxx"

with requests.Session() as session:
    # provide authentication data to session, will be sent automatically
    session.auth = ('test', 'test')
   

    # Use the first request, which uses basic authentication, 
    # to set the language using the cookie
    header_response = session.get(API_DOMAIN, 
                                  cookies={'contact.language': 'en'})
    #If the connection request is successful, perform below operations
    if header_response.status_code == 200:        
        token_response = session.get(f"{API_DOMAIN}/{API_BASE_PATH}")
        token = token_response.json()
       # print(token)
        for f in token['targets']:
                 if f['cdbf_type'] == 'STL':
                     stl_file=f["@id"]
        print(stl_file)
        data_response=session.get(stl_file)
        if data_response.status_code == 200:
            with open(r"C:\Users\xxx\Test_Results\test.stl", 'wb') as f:
                f.write(data_response.content)
        mesh = trimesh.load(r"C:\Users\xxx\Test_Results\test.stl")
        mesh.scene
                
                     
       
        
       
        
        


