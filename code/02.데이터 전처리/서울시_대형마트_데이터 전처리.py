#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:30:21 2021

@author: nockda
"""

import pandas as pd
import re

#파일 불러오기
input_file = r"/Users/nockda/project/Data-Python/teamProject/대형매장/서울특별시 대규모점포 인허가 정보 v2.csv"
output_file='/Users/nockda/project/Data-Python/teamProject/대형매장/output.csv'

df = pd.read_csv(input_file)

print(df)

#컬럼 수정하기
df2 = df.loc[:,['사업장명', '상세영업상태명', '소재지면적', '지번주소','업태구분명', '점포구분명']]
df3 = df2.rename(columns={'사업장명' : 'name', '상세영업상태명' : 'status', '소재지면적' : 'measure', '지번주소' : 'addr', '업태구분명' : 'kind', '점포구분명': 'kind2'}, inplace = False)

#폐업 삭제하기
for i in range(0, len(df3)):
    if df3['status'][i] == '폐업처리' :
        df3 = df3.drop(i, axis=0)

#결측치 제거
df3 = df3.dropna(subset=['addr'])
        
# 인덱스 재설정
df3=df3.reset_index()

#글자수 적은거 삭제
for i in range(0, len(df3)):
    if len(df3['addr'][i]) < 10:
        df3= df3.drop(i,axis=0)
        
#주소에 구, 동 판별
df3['addr_gu'] = df3['addr'].str.split(" ").str[1]
df3['addr_dong'] = df3['addr'].str.split(" ").str[2]

#결측치 채우기
df3 = df3.fillna("")

#그밖에 대규모 점포 삭제
df3.loc[df3['kind'].str.contains('그 밖의 대규모점포')]
df3.drop(df3.loc[df3['kind']== '그 밖의 대규모점포'].index, inplace=True)

# 인덱스 재설정
df3=df3.reset_index()

#동이름 변경
for i in range(0, len(df3['addr'])):
    pat1 = re.compile("(\D+)([0-9][가])").sub("\g<1>", df3['addr_dong'][i])
    pat2 = re.compile("(\D+)([0-9])([동])").sub("\g<1>\g<3>", pat1)
    df3['addr_dong'][i] = pat2
    
df3=df3.drop(columns=['level_0','index'])
    
#결측치 채우기
df3['measure'] = df3['measure'].replace("",0)

#그룹바이
df4=df3.iloc[:,[2,6,7]].groupby(['addr_gu', 'addr_dong']).agg(['count'])

             
df4.to_csv(output_file, encoding='utf-8')
