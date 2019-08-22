import pandas as pd
list1 = [3,4,5,6]
list2 = ['第一個','第二個','第三個']
dict1 = []
new_list = []
for i in range(2):
	new_list.append([])
	for dim in range(2):
		new_list[i].append(list1[i])
index = 0
lot_list=[[3,4,5],[6,7,8]]
for i in lot_list:
	dict1.append(dict(zip(list2,i)))
df1= pd.DataFrame(dict1)
print(dict1)
print(df1)
print(list1[1])
# print(df1)
print('---')
print(new_list)