#!/usr/bin/env python
# coding: utf-8

# # 파이썬데이터분석 기말 프로젝트
# ## 산업데이터사이언스학부
# ## 201904199 김윤오
# ###### 5/14 기준 갱신된 데이터로 재수집 후 진행시작.(csv로 다운받은 데이터 한정, xml은 기간별로 사이트 내 갱신중.)

# # 데이터 불러오기
# #### 데이터출처
# #### 1. 서울 열린데이터광장(서울시 유기동물보호 현황 통계, 서울입양대기동물현황, 반려동물 유무 및 취득경로)
# #### 2. 공공데이터포털(동물보호센터, 유기동물보호수)
# 
# 
# ###### 서울시 유기동물보호 현황 통계
# ###### https://data.seoul.go.kr/dataList/369/S/2/datasetView.do
# ###### 서울입양대기동물현황
# ###### https://data.seoul.go.kr/dataList/OA-21088/S/1/datasetView.do
# ###### 반려동물 유무 및 취득경로
# ###### https://kosis.kr/statHtml/statHtml.do?orgId=611&tblId=DT_611003_2016013&vw_cd=&list_id=&seqNo=&lang_mode=ko&language=kor&obj_var_id=&itm_id=&conn_path=
# ###### 동물보호센터
# ###### https://www.data.go.kr/iim/api/selectAPIAcountView.do
# ###### 유기동물보호수
# ###### https://www.data.go.kr/iim/api/selectAPIAcountView.do
# 

# In[1]:


#데이터 불러오기를 위해 필요한 라이브러리 불러오기
import pandas as pd
import numpy as np


# In[2]:


add=pd.read_csv("C:/Users/dbsdh/Desktop/파이썬데이터분/반려동물유무및취득경로.csv",encoding='UTF-8',header=None)
S_wait=pd.read_csv("C:/Users/dbsdh/Desktop/파이썬데이터분/서울입양대기동물현황.csv",encoding='UTF-8',header=None)
info_wait=pd.read_csv("C:/Users/dbsdh/Desktop/파이썬데이터분/유기동물보호현황.csv",encoding='UTF-8',header=None)


# #### 결측치 확인

# In[3]:


add.info()


# In[4]:


S_wait.info()


# In[5]:


info_wait.info()


# ### 유기동물현황 데이터에서 필요한 부분만 추출

# In[6]:


info_wait.iloc[[0,2,3,4],2:]


# In[7]:


info_wait=info_wait.iloc[[0,2,3,4],2:]


# In[8]:


info_wait


# In[9]:


info_wait.reset_index(inplace=True, drop=True)


# ### 필요한 부분 연도에 따라 범위를 나눈뒤, 합치기

# In[10]:


#2018년 유기동물 현황
a2018=info_wait.iloc[:,0:11]
a2018


# In[11]:


#2019년 유기동물 현황
a2019=info_wait.iloc[:,16:27]
a2019


# In[12]:


#2020년 유기동물 현황
a2020=info_wait.iloc[:,32:43]
a2020


# In[13]:


#2021년 유기동물 현황
a2021=info_wait.iloc[:,48:59]
a2021


# In[14]:


#2022년 유기동물 현황
a2022=info_wait.iloc[:,64:75]
a2022


# In[15]:


#합치기
info_wait=pd.concat([a2018,a2019,a2020,a2021], axis = 1)
info_wait


# In[16]:


add


# ### 연령별, 성별로 반려동물 유무 각각 나눈뒤, 합치기

# In[17]:


#서울시, 연령별 반려동물 유뮤
add.iloc[[0,2,3,6,7,8,9,10],0:4]


# In[18]:


#성별에 따른 반려동물 여부
#2019
b1=add.iloc[0:6,[0,1,4,5]]
b1


# In[19]:


#2020
b2=add.iloc[0:6,12:14]
b2


# In[20]:


#2021
b3=add.iloc[0:6,21:23]
b3


# In[21]:


#합치기
add_ox=pd.concat([b1,b2,b3], axis = 1)


# In[22]:


add_ox


# In[23]:


#연령대별 반려동물여부
#2019
bb1=add.iloc[[0,1,2,3,6,7,8,9,10],[0,1,4,5]]
bb1


# In[24]:


#2020
bb2=add.iloc[[0,1,2,3,6,7,8,9,10],12:14]
bb2


# In[25]:


#2021
bb3=add.iloc[[0,1,2,3,6,7,8,9,10],21:23]
bb3


# In[26]:


#합치기
add_age=pd.concat([bb1,bb2,bb3], axis = 1)
add_age


# In[27]:


S_wait
#입양상태 N=입양대기 P=입양진행중 C=입양완료
#임시보호 N=센터보호중 C=임시보호중


# ## XML형식의 데이터 불러오기

# In[28]:


#유기동물 보호센터 조회
import requests
import pprint
import xml

url="http://apis.data.go.kr/1543061/animalShelterSrvc/shelterInfo?numOfRows=1000&pageNo=&serviceKey=WIr9ZWurlrwI5%2FNEHGoobKkOzOZPjryI8D16Pf2dryNJSfF5Glr3PZABl14yQnwPOVaNxdhLknbAJw%2F75PMSRg%3D%3D"

response=requests.get(url)

contents=response.text


# In[29]:


pp=pprint.PrettyPrinter(indent=1000)
print(pp.pprint(contents))


# In[30]:


from os import name
import xml.etree.ElementTree as ET
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote


# In[31]:


xml_obj = bs4.BeautifulSoup(contents,'lxml-xml')
rows_h = xml_obj.findAll('item')
print(rows_h)


# In[32]:


# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows_h)):
    columns = rows_h[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]


# In[33]:


df_house = pd.DataFrame(row_list,columns=name_list)
print(df_house.head(19))


# In[34]:


df_house


# In[35]:


#유기동물 정보 조회 서비스
url="http://apis.data.go.kr/1543061/abandonmentPublicSrvc/sido?numOfRows=1000&pageNo=&serviceKey=WIr9ZWurlrwI5%2FNEHGoobKkOzOZPjryI8D16Pf2dryNJSfF5Glr3PZABl14yQnwPOVaNxdhLknbAJw%2F75PMSRg%3D%3D"
response=requests.get(url)

contents=response.text


# In[36]:


pp=pprint.PrettyPrinter(indent=1000)
print(pp.pprint(contents))


# In[37]:


#유기동물 정보 조회 서비스
#url불러오기
url="http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic?numOfRows=1000&pageNo=&serviceKey=WIr9ZWurlrwI5%2FNEHGoobKkOzOZPjryI8D16Pf2dryNJSfF5Glr3PZABl14yQnwPOVaNxdhLknbAJw%2F75PMSRg%3D%3D"
response=requests.get(url)

contents=response.text
#확인하기
pp=pprint.PrettyPrinter(indent=1000)
print(pp.pprint(contents))
#xml->DF로 바꾸기
xml_obj = bs4.BeautifulSoup(contents,'lxml-xml')
rows = xml_obj.findAll('item')
print(rows)
# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]
    


# In[38]:


df_inf_loc = pd.DataFrame(row_list, columns=name_list)
print(df_inf_loc.head(19))


# In[39]:


df_inf=pd.DataFrame(row_list)


# In[40]:


df_inf=df_inf.loc[:,0:21]


# In[41]:


df_inf.columns=name_list


# In[42]:


df_inf.head()


# In[43]:


df_house.info()


# In[44]:


df_inf.info()


# In[45]:


df_inf.columns.tolist()


# ### 유기동물 정보 필요한 컬럼만 선택한뒤, 컬럼의 영문이름을 한국이름으로 변경하고 데이터프레임에 적용하기

# In[46]:


col=['desertionNo','happenDt','happenPlace','kindCd','colorCd','age','weight','noticeSdt','noticeEdt','sexCd',
    'neuterYn']


# In[47]:


df_inf=df_inf[col]


# In[48]:


df_inf=df_inf.rename(columns={'desertionNo':'유기번호','happenDt':'접수일','happenPlace':'발경장소','kindCd':'품종','colorCd':'색상','age':'나이','weight':'체중','noticeSdt':'공고시작일','noticeEdt':'공고종료일','sexCd':'성별',
    'neuterYn':'중성화여부'})


# In[49]:


df_inf.head()


# # 데이터 불러오기 종료<br>
# ## 불러온 데이터 정리<br>
# 
# 1. S_wait=서울입양대기동물현황<br>
# 2. info_wait=2018-2022년 유기동물 현황<br>
# 3. add_ox=2019-2021서울시 성별에 따른 반려동물 유뮤<br>
# 4. add_age=2019~2021 서울시 연령별 반려동물 유무<br>
# 5. df_house=유기동물 보호센터 현황<br>
# 6. df_inf=유기동물 조회
# 

# ### 분석을 위한 데이터 전처리 시작

# ### 2018~2022년 유기동물 현황 분석을 위한 데이터프레임 전처리

# In[50]:


info_wait


# In[51]:


#-표시된 부분 0으로 교체
info_wait=info_wait.replace('-',0)
df1=info_wait.transpose()
df1
df1.columns=['연도','종','현황','마리수']
df1


# In[52]:


idx11=df1[(df1.종=='개') | (df1.종=='고양이')].index


# In[53]:


df1=df1.loc[idx11,]
df1


# In[54]:


df_situ=df1
df_situ


# In[55]:


df_situ.info()


# In[56]:


df_situ.memory_usage()


# ##### 데이터 타입 변경

# In[57]:


df_situ['종'].unique()


# In[58]:


df_situ['종']=df_situ['종'].astype('category')


# In[59]:


df_situ['현황'].unique()


# In[60]:


df_situ['현황']=df_situ['현황'].astype('category')


# In[61]:


df_situ['마리수']=df_situ['마리수'].astype(np.int16)


# In[62]:


df_situ.info()


# In[63]:


df_situ.memory_usage()


# ### 서울시 성별 반려동물 분석을 위한 데이터프레임 전처리

# In[64]:


add_ox


# In[65]:


df2=add_ox.transpose()
df2


# In[66]:


df2=df2.iloc[2:,[0,2,3,4,5]]
df2.columns=['연도','반려동물유무','남녀평균','남자','여자']


# In[67]:


df_sex=df2
df_sex


# In[68]:


df_sex.info()


# ##### 데이터타입 변경

# In[69]:


df_sex['반려동물유무'].unique()


# In[70]:


df_sex['반려동물유무']=df_sex['반려동물유무'].astype('category')
df_sex['남녀평균']=df_sex['남녀평균'].astype(np.float16)
df_sex['남자']=df_sex['남자'].astype(np.float16)
df_sex['여자']=df_sex['여자'].astype(np.float16)


# In[71]:


df_sex.info()


# In[72]:


df_sex


# ### 서울시 연령대별 반려동물 유무 분석을 위한 데이터프레임 전처리

# In[73]:


add_age


# In[74]:


df3=add_age.transpose()


# In[75]:


df3


# In[76]:


df3=df3.iloc[2:,[0,2,3,4,5,6,7,8]]
df3


# In[77]:


df3.columns=['연도','반려동물유무','평균','20대이하','30대','40대','50대','60대이상']
df3


# In[78]:


df_age=df3
df_age


# In[79]:


df_age.info()


# ##### 데이터타입 변경

# In[80]:


df_age['반려동물유무'].unique()


# In[81]:


df_age['반려동물유무']=df_sex['반려동물유무'].astype('category')
df_age['평균']=df_age['평균'].astype(np.float16)
df_age['20대이하']=df_age['20대이하'].astype(np.float16)
df_age['30대']=df_age['30대'].astype(np.float16)
df_age['40대']=df_age['40대'].astype(np.float16)
df_age['50대']=df_age['50대'].astype(np.float16)
df_age['60대이상']=df_age['60대이상'].astype(np.float16)


# In[82]:


df_age.info()


# ### 서울시 유기동물 현황 분석을 위한 데이터프레임 전처리

# In[83]:


S_wait=S_wait.rename(columns=S_wait.iloc[0])
S_wait=S_wait.drop(S_wait.index[0])
S_wait


# In[84]:


S_wait['입소날짜']=pd.to_datetime(S_wait['입소날짜'])
S_wait['입소날짜']=S_wait['입소날짜'].dt.year
S_wait['나이']=S_wait.나이.str.split('(',expand=True)[0]
S_wait=S_wait.rename(columns={'나이':'(만)나이'})
S_wait=S_wait.rename(columns={'입소날짜':'입소연도'})
S_wait


# In[85]:


df_orglist1=S_wait
df_orglist1


# In[86]:


df_orglist1.info()


# #### 전국 유기동물 현황 분석을 위한 데이터프레임 전처리

# In[87]:


df_inf.head(5)


# In[88]:


df4=df_inf
df4


# In[89]:


len(df4)


# In[90]:


df4.info()


# In[91]:


dro=[]

for i in range(len(df4)):
    if '개' in df4.loc[i,'품종']:
        df4.loc[i,'품종']='개'
    elif '고양이' in df4.loc[i,'품종']:         
        df4.loc[i,'품종']='고양이'
    else:
        print(i,'번째 동물의 품종',df4.loc[i,'품종'],'은/는 개/고양이 이외의 품종입니다.')


# In[92]:


#변경확인
df4


# In[93]:


#개와 고양이만 선택
df4=df4[df4['품종'].str.contains('개')|df4['품종'].str.contains('고양이')]
df4


# In[94]:


df4['나이']=df4.나이.str.split('(',expand=True)[0]
df4.rename(columns={'나이':'출생연도'})
df4['체중']=df4.체중.str.split('(',expand=True)[0]
df4


# In[95]:


df4['체중']=df4.체중.str.split('~',expand=True)[0]
df4['체중']=df4.체중.str.split('-',expand=True)[0]
df4


# In[96]:


df4.info()


# In[97]:


df4['성별'].unique() #M=남성 F= 여성 Q=미상


# In[98]:


df4['중성화여부'].unique() #N=아니오 U=미상 Y=네


# In[99]:


df4['성별']=df4['성별'].astype('category')
df4['중성화여부']=df4['중성화여부'].astype('category')
df4['나이']=df4['나이'].astype('category')


# In[100]:


df4.info()


# In[101]:


df4['체중'].describe()
df4['체중']=df4['체중'].astype(np.float16)


# In[102]:


df4['체중'].describe()


# In[103]:


df4.loc[10,'체중']


# In[104]:


df_Norglist=df4


# In[105]:


df_Norglist


# In[106]:


df_Norglist['성별'].unique()


# In[107]:


df_Norglist['중성화여부'].unique()


# In[108]:


df_Norglist['성별']=df_Norglist['성별'].astype('category')
df_Norglist['중성화여부']=df_Norglist['중성화여부'].astype('category')


# In[109]:


df_Norglist.info()


# ### 서울내의 유기동물 vs 전국 유기동물 현황 비교시
# ### 전국 유기동물 현황의 데이터가 더 많음
# ### 서울내의 유기동물 데이터 사용X

# ##### 전국 유기동물 보호소 현황 분석을 위한 데이터프레임 전처리

# In[110]:


df5=df_house
df5


# In[111]:


df5.iloc[1,2]


# ### 컬럼에 맞지않는 데이터가 있음을 확인
# ### 데이터들이 적절한 컬럼에 포함되어있지않고, n칸씩 앞으로 당겨져 있는 모습을 확인
# ### 컬럼 중간중간 이상치로 인한 문제로 확인
# ## -> xml을 통해 불러온 결과과정 재확인

# In[112]:


print(rows_h)
#csv로 저장하여 확인한 결과, 한 행에서 중간에만 NA값이 있었던 경우, 그 행의 결측값을 :로 대체한 모습을 확인할 수 있었음
#예를 들어, 1,2,3열에 데이터가 있고 그 뒤의 열에는 데이터가 없는경우, item내에서 컬럼 이름과 값 자체를 확인할 수 없었음
#그러나, 1,2,8,9,...열에 데이터가 존재한다면, 3,4,5,6,7열에 :값을 na값으로 표시하였음을 확인.


# In[113]:


#:가 포함된 행 추출
a=[]
for i in range(len(df5)):
    for j in range(len(df5.columns)):
        if df5.iloc[i,j]==":":
            a.append(i)
        else:
            print(a)


# In[114]:


#중복 값 제거
b = []
for v in a:
    if v not in b:
        b.append(v)
print(b)


# In[115]:


df5=df5.iloc[b]
df5

##해결안됨


# In[116]:


df5.info()


# In[117]:


#사용할 컬럼 지정
col_df5=['careNm','divisionNm','saveTrgtAnimal']


# In[118]:


df5_1=df_house[col_df5]
df5_1


# In[119]:


df5_1=df5_1.rename(columns={'careNm':'보호소이름','divisionNm':'유형','saveTrgtAnimal':'보호동물'})


# In[120]:


df5_1.head(3)


# In[121]:


df5_1.info()


# In[122]:


df5_1


# In[123]:


ani=[]
for i in range(len(df5_1)):
    if '개' in df5_1.loc[i,'보호동물']:
        ani.append(i)
    elif '고양이' in df5_1.loc[i,'보호동물']:         
        ani.append(i)
    else:
        print(i,'번째 데이터는 이상치.')
print(ani)


# In[124]:


bb = []
for v in ani:
    if v not in bb:
        bb.append(v)
print(bb)


# In[125]:


df5_1=df5_1.iloc[bb]
df5_1


# In[126]:


df5_1.info()


# In[127]:


df5_1['유형'].unique()


# In[128]:


df5_1['유형']=df5_1['유형'].astype('category')


# In[129]:


df5_1.info()


# In[130]:


df_secure=df5_1


# ### 전처리된 데이터프레임 목록
# #### df_situ=2018~2022 유기동물 현황
# #### df_sex=성별 반려동물 유무
# #### df_age=연령별 반려동물 유무
# #### df_Norglist=전국 유기동물 현황
# #### df_secure=전국 보호소 유형

# #### 전처리 종료, 분석을 위한 시각화 시작.

# In[131]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[132]:


import matplotlib
import matplotlib.font_manager as fm

fm.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/NanumGothic.ttf' # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)


# In[133]:


df_sex


# In[134]:


df_sex_o=df_sex.iloc[[0,2,4]]
df_sex_o
df_sex_x=df_sex.iloc[[1,3,5]]


# In[135]:


#성별에 따른 발려동물 유무

fig,ax=plt.subplots(figsize=(20,6),ncols=2)

plt.xlabel('연도')
sns.barplot(data=df_sex_o,x='연도',y='남자',ax=ax[0])
sns.barplot(data=df_sex_o,x='연도',y='여자',ax=ax[1])


# ### 2019년 이후의 남녀 반려동물 유무 평균을 확인결과, 남성이 반려동물을 갖는 경우가 많았으며, 생각보다 여성의 반려동물 유무 평균이 낮았음을 확인

# In[136]:


fig,ax=plt.subplots(figsize=(5,5))
plt.title('남녀평균')
sns.barplot(data=df_sex_o,x='연도',y='남녀평균')


# ### 각각의 평균으로 보았을땐, 남자의 경우 매년 증가하는 수치를 보엿으나, 둘을 합쳐서 본 결과, 반려동물을 갖지 않은 인구는 매년 증가하고 있음을 확인할 수 있었다. (남성의 경우, 심슨의 역설로 볼 수 있다.)

# In[137]:


df_situ


# In[138]:


df_situ_agg=df_situ.iloc[[0,5,10,15,20,25,30,35]]
df_situ_agg


# In[139]:


df_situ_agg_dog=df_situ_agg.iloc[[0,2,4,6]]
df_situ_agg_cat=df_situ_agg.iloc[[1,3,5,7]]


# In[140]:


fig,ax=plt.subplots(figsize=(20,6),ncols=2)

plt.xlabel('연도')
sns.barplot(data=df_situ_agg_dog,x='연도',y='마리수',ax=ax[0])
sns.barplot(data=df_situ_agg_cat,x='연도',y='마리수',ax=ax[1])


# ### 분석 전 예상했던 결과와 정반대의 결과
# ### 매년 개의 유기사례가 증가할 줄 알았으나, 생각외로 매년 유기사례는 감소하고 있었다.
# ### 하지만 고양이의 경우 약 2500마리 정도의 수준으로 매년 유기사례가 발생하고 있었다.

# In[141]:


df_age_o=df_age.iloc[[0,2,4]]
df_age_o


# In[142]:


fig,ax=plt.subplots(figsize=(20,6),ncols=5)

plt.xlabel('연도')
sns.barplot(data=df_age_o,x='연도',y='20대이하',ax=ax[0])
sns.barplot(data=df_age_o,x='연도',y='30대',ax=ax[1])
sns.barplot(data=df_age_o,x='연도',y='40대',ax=ax[2])
sns.barplot(data=df_age_o,x='연도',y='50대',ax=ax[3])
sns.barplot(data=df_age_o,x='연도',y='60대이상',ax=ax[4])


# ### 20대이하의 경우, 매년 반려동물을 갖는 인구의 수가 계속해서 감소하는 추세를 보임, 그 외의 연령대에서는 특이한 변화를 확인할 수 없었다.

# In[143]:


fig,ax=plt.subplots(figsize=(10,10))
plt.xlabel('연도')
sns.barplot(data=df_age_o,x='연도',y='평균')


# ### 미세한 차이이긴 하지만, 모든 연령에 대하여 평균적으로 반려동물을 갖는 수는 감소하고 있다.

# In[144]:


df_situ_2=df_situ.iloc[[31,32,33,34]]
df_situ_2


# In[145]:


fig,ax=plt.subplots(figsize=(10,10))

plt.title('2021년 유기동물(개)의 현황')
plt.pie(df_situ_2['마리수'],labels=df_situ_2['현황'],autopct='%.1f%%')


# ### 가장 최근이었던 2021년, 유기동물 중 개의 현황을 확인결과, 약 45%는 주인에게 인도되고, 약 40%는 입양분양이 진행되었으나, 그 외의 개들은 폐사안락사 혹은 계류기증 상황이었음을 확인하였다.

# In[146]:


df_Norglist


# In[147]:


fig, ax = plt.subplots(figsize=(10, 8),ncols=2)
plt.title('유기동물 특징(중성화여부, 성별)')
sns.countplot(
    x='중성화여부', 
    hue='중성화여부', 
    data=df_Norglist, 
    dodge=False,
    ax=ax[0]
)
sns.countplot(
    x='성별', 
    hue='성별', 
    data=df_Norglist, 
    dodge=False,
    ax=ax[1]
    
)


# ### 유기동물의 경우, 중성화가 되어있지 않은 경우가 대부분이었으며, 성별에서는 특이한 차이점을 확인할 수 없었다.

# In[148]:


fig, ax = plt.subplots(figsize=(10, 8))

plt.scatter(df_Norglist['나이'],df_Norglist['체중'])


# ### 산점도 확인결과, 비교적 최근에 태어난 아이들과 체중이 적게 나가는 아이들의 경우, 유기되는 사례가 많았음을 확인할 수 있었다.

# In[149]:


df_secure


# In[150]:


fig,ax=plt.subplots(figsize=(10,10))

plt.title('2023년 현재 보호소의 유형(개와 고양이를 취급하는 보호소중)')
sns.countplot(
    x='유형', 
    hue='유형', 
    data=df_secure, 
    dodge=False
)


# ### 현재 법인이 가장 높은 수치로 확인되었으나, 동물의 치료만을 담당해야하는 동물병원과 비교 하였을때, 치료만을 담당하는 동물병원에서의 유기동물 보호를 하는 경우가 많았다.
# ### 또한, 개인과 단체로 이루어지는 유기동물보호소의 형태도 확인할 수 있었다.
# ### 동물병원에서의 유기동물 보호를 줄이고, 법인으로 지정된 보호소들의 수가 증가해야 함을 확인하였다.

# # 데이터 분석결과 정리
# ## 1. 2019년 이후 여성에 비해 남성이 반려동물을 기르는 경우가 평균적으로 많았다.
# ## 2. 성별 전체로 확인했을 경우, 반려동물을 갖지 않은 인구는 매년 증가하는 것을 확인하였다.(남성의 경우 심슨의 역설에 빠질 수 있는 결과)
# ## 3. 분석 전 기대했던 결과와 달리, 개의 유기사례는 감소하고 있는 추세였고 고양이는 기대와 같이 매년 평균 2500마리 정도의 유기사례가 발생하였다. 하지만 개의 경우에도 유기사례 수치가 꽤 큰 것을 확인하였다.
# ## 4. 모든 연령에 대하여 평균적으로 반려동물을 기르는 사례가 줄고 있다.
# ## 5. 2021년 유기동물(개) 현황에 대한 분석결과, 약 45%는 주인에게 인도되고 약 40%는 입양분양이 진행되었으나, 그 외의 경우에는 폐사안락사 혹은 계류기증이 진행되었다.
# ## 6. 최근에 태어나고 체중이 적게 나가는 동물들의 경우, 유기가능성이 증가하였다.
# ## 7. 현재 법인으로 지정된 보호소가 가장 많았으나, 동물 치료를 주로 해야하는 동물병원에서의 보호사례가 두번째로 법인으로 지정된 보호소와 별로 차이나지 않는 수치를 보였다.

# # 분석결과 활용방안
# ## 1. 반려동물에 대한 인식 개선
# ## 현재 반려동물을 기르는 인구수가 감소하는 것을 확인.
# ## ->반려동물 권장 캠페인등의 사람들에게 반려동물에 대한 좋은 인식을 주는 캠페인 실행.
# ## 2. 반려동물 유기에 대한 처벌 시급
# ## -> 반려동물의 유기사례는 고양이의 경우 약 2500마리로 많았으며, 개의 경우 감소하였으나 아직 꽤나 높은 수치를 기록하고 있다. 이러한 유기에 대한 법적 처벌의 강화가 시급.
# ## 3. 유기동물의 현황 공개
# ## 현재 유기동물의 현황이 어떤지에 대해서 모르는 사람들이 많음. 이러한 사람들에게 유기동물의 현황에 대하여 자세히 공개하여 사람들에게 있어 분양이 아닌 유기동물 입양을 권장.
# ## 4. 법인으로 지정된 보호소 수 증가
# ## -> 동물의 치료가 주가 되어야 하는 동물병원에서의 유기동물 보호 사례가 너무 많은것을 확인. 동물병원에서는 치료를 주로 진행할 수 있도록 보호를 주로 하는 법인으로 지정된 보호소의 수를 증가해야할 필요 확인.

# ###### END

# In[ ]:




