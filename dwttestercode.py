# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 21:13:47 2022

@author: Mrunmay Junagade
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


infile=r'G:\My Drive\Research\Cables\cbra\input.csv'
outfile=r'G:\My Drive\Research\Cables\cbra\out2.xlsx'
inp=pd.read_csv(infile)
out=pd.read_excel(outfile)
inp=inp[1:1000]
inp=inp.fillna(0)
inp=inp.drop(columns=['BaseDateTime','LAT','LON','Heading','COG','Status','CallSign'])

for i in range(0,len(inp)):
    
    import requests
    from bs4 import BeautifulSoup as bs
    inpt=inp.iloc[i]
    MMSI=str(int(inpt.MMSI))
    my_url = 'https://www.myshiptracking.com/vessels/'+MMSI  #webscrape myshiptracking.com
            
    page=requests.get(my_url)
    soup = bs(page.content)
    a=soup.find_all('td',{})
    if len(a)>=7: 
        b=str(a[7])
        if b[5]!='-':
            b=b.replace('<td>','')
            b=b.replace(' <small>Tons</small></td>','')
            b=int(b.replace(',',''))
            source='myshiptracking.com'
        elif inpt.VesselName==0 or inpt.IMO==0:
            b=0
            source='failed'
        elif b[5]=='-':
            name=str(inpt.VesselName)
            headers={'User-Agent': 'LMAO TRICKED YOU'}
            name=name.replace(' ','-')
            IMO=str(inpt.IMO)
            IMO=IMO.replace('IMO','')
            loc='https://www.vesselfinder.com/vessels/'+name+'-IMO-'+IMO+'-MMSI-'+MMSI #webscrape vesselfinder.com
            r = requests.get(loc,headers=headers)
            soup = bs(r.content, 'lxml')
            tags=soup.find_all('td',{'class':'v3'})
            if  len(tags)>=16:
                b=str(tags[16])
                b=b.replace('<td class="v3">','')
                b=b.replace('</td>','')
                if b=='-':
                    b=0
                    source='failed'
                else:
                    b=int(b)
                    source='vesselfinder.com'
            else:
                b=0
                source='failed'
                    
        else: 
            b=0
            source='failed'
        
    else:
        b=0
        source='failed'
    
    l=inpt.IMO
            
    print(i,':',b,':',l, source)
        
            
