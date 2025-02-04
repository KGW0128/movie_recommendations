
#워드클라우드 띄우기

import pandas as pd
from pygments.styles.dracula import background
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager


#한글폰트 설정
font_path = 'malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic') # 상업적으로 사용 가능한 무료폰트

df= pd.read_csv('./Cleaned_Reviews/cleaned_reviews.csv')
words = df.iloc[0,1].split()
#print(words)
print(df.iloc[0,0])


worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(
    background_color='white',
    font_path=font_path).generate_from_frequencies(worddict)

plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()


