import sqlite3,csv,os
def execute_db(file_name, sql_cmd):
	conn = sqlite3.connect(file_name)
	c = conn.cursor()
	c.execute(sql_cmd)
	conn.commit()
	conn.close()
def select_db(file_name, sql_cmd):
	conn = sqlite3.connect(file_name)
	c = conn.cursor()
	c.execute(sql_cmd)
	rows = c.fetchall()
	conn.close()
	return rows
def main():
	os.remove('db.sqlite')  # 因為資料庫存在就不能覆蓋，因此用os手動移除
	db_name= 'db.sqlite'
	sql_cmd = 'CREATE TABLE record (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, price INTEGER, platform TEXT)'
	print('建立資料庫')
	execute_db(db_name,sql_cmd)
	# 練習插入資料
	sql_cmd = 'INSERT INTO record (item, price, platform) VALUES ("oppo_phone", 1000 ,"TEST")'
	execute_db(db_name,sql_cmd)
	# 練習更改資料
	sql_cmd = 'UPDATE record SET platform="EZ Seller" where platform ="TEST" '
	execute_db(db_name,sql_cmd)
	# 寫入資料
	with open('ezprice.csv', 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			sql_cmd= 'INSERT INTO record(item, price, platform) VALUES \
			         ("%s", %d, "%s")' %(row['name'], int(row['price']), row['platform'])
			execute_db(db_name, sql_cmd)
	# 從 SQLite 資料庫抓出資料
	sql_cmd = 'SELECT * FROM record WHERE price < 400'
	data_rows = select_db(db_name, sql_cmd)
	for row in data_rows:
		print(row)
if __name__ == '__main__':
	main()
