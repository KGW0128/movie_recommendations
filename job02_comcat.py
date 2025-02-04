import pandas as pd
import glob

data_paths = glob.glob('./review/*')
# print(data_paths)


df = pd.DataFrame()

for path in data_paths:
    df_temp = pd.read_csv(path)
    # print(df_temp)

    #초기화
    titles = []
    reviews = []
    old_title = ''

    for i in range(len(df_temp)):
        title = df_temp.iloc[i, 1]

        # 같은 영화 제목이 아니면
        if title != old_title:
            titles.append(title)
            old_title = title
            df_movie = df_temp[(df_temp.name == title)]

            # 리뷰 간격 띄워주기
            review = ' '.join(df_movie.review)
            reviews.append(review)



    print(titles)
    print(reviews)
    df_batch = pd.DataFrame({'titles': titles, 'reviews': reviews})
    df_batch.info()
    print(df_batch)
    df = pd.concat([df,df_batch], ignore_index=True)
df.info()
df.to_csv('./Merged_Reviews/reciews_kinolights.csv',index=False)