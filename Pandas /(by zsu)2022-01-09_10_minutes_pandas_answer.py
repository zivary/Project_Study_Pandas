#!/usr/bin/env python
# coding: utf-8

# ---
# ### 10 Minutes Pandas
# * Object Creation
# * Viewing Data
# * Selection
# * Missing Data
# * Operation
# * Merge
# * Grouping
# * Reshaping
# * Time Series
# * Categoricals
# * Plotting
# * Getting Data In / Out
# * Gotchas
# 
# ---

# In[1]:


# 필요한 패키지 불러오기
import numpy as np
import pandas as pd


# ### Categoricals

# * Q) 아래의 데이터프레임이 존재한다. '국가' 데이터(열)을 범주형 데이터로 변환하시오. 이떄 열 이름을 '대륙_카테고리'로 하시오.

# In[56]:


df = pd.DataFrame({"기업":["현대","삼성","벤츠","애플","테슬라"], "국가":["한국","한국","독일","미국","미국"]})


# In[57]:


df["대륙_카테고리"] = df["국가"].astype("category")


# In[61]:


# 확인
df["대륙_카테고리"]


# * Q) 생각해보니 대륙 카테고리입니다. 대륙_카테고리를 대륙별로 새롭게 범주화하시오(유럽/아메리카/아시아).

# In[62]:


df["대륙_카테고리"].cat.categories = ["유럽","아메리카","아시아"]


# In[63]:


# 확인
df


# * Q) 대륙 카테고리에 빠진 대륙들을 추가해주시오. 빠진 대륙은 (아프리카, 오세아니아) 입니다.

# In[76]:


df["대륙_카테고리"] = df["대륙_카테고리"].cat.set_categories(["유럽","아메리카","아시아","아프리카","오세아니아"])


# In[77]:


# 확인
df["대륙_카테고리"]


# * Q) 대륙 카테고리를 기준으로 데이터프레임을 정렬하시오(유럽, 아메리카, 이시아, 아프리카, 오세아니아 순으로).

# In[78]:


df.sort_values(by="대륙_카테고리")


# * Q) 대륙 카테고리 별 기업의 숫자를 구하시오.

# In[79]:


df.groupby("대륙_카테고리").size()


# ### Getting Data In / Out

# * Q) 공유한 happiness_data.csv 파일을 읽고 df 이름의 객체로 저장하시오.

# In[79]:


df = pd.read_csv("/Users/jisu/Desktop/happiness_data.csv")


# * Q) df에서 country_name이 "South Korea"인 데이터만 필터(filter)한 후 happiness_data_korea.csv 파일(index가 없는 상태)로 저장하시오.

# In[65]:


df[df["country_name"] == "South Korea"].to_csv("/Users/jisu/Desktop/happiness_data_korea.csv", index=False)


# * Q) happiness_data_korea.csv 파일을 읽고 df2 이름의 객체로 저장하시오.

# In[66]:


df2 = pd.read_csv("/Users/jisu/Desktop/happiness_data_korea.csv")


# * df2 데이터프레임에서 social_support가 0.79 이상이며 동시에 freedom_to_make_life_choices가 0.65 이상인 데이터를 필터링한 후 high_happiness.h5 파일의 df3로 저장하시오.

# In[67]:


df2[(df2.social_support >= 0.79) & (df2.freedom_to_make_life_choices >= 0.65)].to_hdf("/Users/jisu/Desktop/high_happiness.h5", "df3")


# * high_happiness.h5파일의 df3을 읽고 df3 이름의 객체로 저장하시오.

# In[70]:


df3 = pd.read_hdf("/Users/jisu/Desktop/high_happiness.h5", "df3")


# * df3의 2번째와 3번째 행(index가 4,5번인 행)을 subsetting 한후 df4.xlsx 파일(Sheet 이름은 "Sheet1", index가 없는 상태)으로 저장하시오.

# In[71]:


df3.iloc[1:3].to_excel("/Users/jisu/Desktop/df4.xlsx", sheet_name="Sheet1", index=None)


# * df4.xlsx 파일을 읽고 df4 이름의 객체로 저장하시오.

# In[73]:


df4 = pd.read_excel("/Users/jisu/Desktop/df4.xlsx", sheet_name="Sheet1")


# ### Plotting

# * 공유한 happiness_data.csv 파일을 읽고 df 이름의 객체로 저장하시오.
# * df에서 country_name이 "South Korea"인 데이터만 필터(filter)한 후 df_korea로 저장하시오.
# * df_korea에서 "year"과 "happiness" column만을 select 한 뒤, index을 "year"로 설정한 후 그래프로 그려보시오.

# In[162]:


df = pd.read_csv("/Users/jisu/Desktop/happiness_data.csv")
df_korea = df[df.country_name == "South Korea"]
df_korea[["year", "happiness"]].set_index("year").plot()


# * matplotlib의 pyplot을 활용하여 다음을 구하시오.
# * 년도별 regional_indicator 별 평균 행복을 도표로 구하시오.

# In[210]:


import matplotlib.pyplot as plt


df_by_regional_indicator = df[["regional_indicator","year","happiness"]].groupby(["regional_indicator", "year"]).agg(["mean"])
df_pivoted = df_by_regional_indicator.pivot_table(index="year", columns="regional_indicator")

plt.figure()
df_pivoted.plot()
plt.legend(loc="best")


# ### Gotchas(Using if/truth statements with pandas)

# * 아래 코드의 Pandas Series는 False도 포함하고 있으며 False도, 또한 길이가 1 이상 이기에 True가 될 수 있는 상황이여서 에러가 발생합니다.

# In[ ]:


if pd.Series([False, True, False]):
    print("I was true")


# * Pandas Series 중 하나라도 True인 경우를 만족하고 싶은 경우 `.any()`를 사용하면 됩니다.

# In[86]:


if pd.Series([False, True, False]).any():
    print("At least one True included")
else:
    print("No True included")


# * Pandas Series가 모두 True인 경우를 만족하고 싶은 경우 `.all()`을 사용하면 됩니다.

# In[89]:


if pd.Series([True, True]).all():
    print("Everything is True")
else:
    print("At least one False included")


# * Pandas Series가 비어있는지 확인하고 싶은 경우 `.empty`나 is None을 사용하면 됩니다.

# In[100]:


if pd.Series(["1"]) is None:  
    print("No element is included")
else:
    print("At least one element included")

# 위와 같음
# if pd.Series(["1"]).empty:
#     print("No element is included")
# else:
#     print("At least one element included")
    

