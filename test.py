import pandas as pd

# 파일 경로
file_path = './정답지 완성본_최종본.xlsx'
file_path2 = './컨셉구축용.xlsx'

df = pd.read_excel(file_path, sheet_name="이리노텔주")

# 칼럼 정보
# print(df.columns)
# ['품목기준코드', '제품명', '증상', '발생부위구분', '발생부위구분 2', '발생부위구분 3', '임상시험', '시판후조사',
#  '인과관계', '병용여부_1', '병용약물_1', '병용_동시_약물_1', '병용여부_2', '병용약물_2', '병용_동시_약물_2']

# 분류하고자 하는 칼럼 리스트
extract_column_list = ['품목기준코드', '제품명', '증상', '발생부위구분', '발생부위구분 2', '발생부위구분 3']

df2 = df[extract_column_list]
# df3 = df.drop(extract_column_list, axis=1)

df2.to_csv('./필요한 항목.csv')
# df3.to_csv('./불필요한 항목.csv')

# 발생부위구분 2, 발생부위구분 3 -> 발생부위구분
df2_1 = df2[['품목기준코드','제품명', '증상', '발생부위구분']]
df2_2= df2[['품목기준코드','제품명', '증상', '발생부위구분 2']].dropna()
df2_2.rename(columns={'발생부위구분 2': '발생부위구분'}, inplace=True)
df2_3 = df2[['품목기준코드','제품명', '증상', '발생부위구분 3']].dropna()
df2_3.rename(columns={'발생부위구분 3': '발생부위구분'}, inplace=True)
result = pd.concat([df2_1, df2_2], ignore_index=True)
result = pd.concat([result, df2_3], ignore_index=True)
result['발생부위구분'] = result['발생부위구분'].str.strip()
# print(result)
# 원본 발생부위군 -> SOC
df_dict = pd.read_excel(file_path2, sheet_name='발생부위_컨셉')
mapping_dict =  dict([(i,a) for i,a in zip(df_dict['원본_발생부위군'], df_dict['해당_SOC'])])
result['SOC'] = result['발생부위구분'].map(mapping_dict) #.fillna(result['발생부위구분'])
result = result.drop(['발생부위구분'],axis=1)
result = result.drop_duplicates()
result.to_excel('./정답지확인.xlsx', index = False)