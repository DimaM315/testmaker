import sqlite3


def db_connect(query):
	with sqlite3.connect('db/db_test.db') as db:
		cursor = db.cursor()
		responce = cursor.execute(query)
		db.commit()
	return responce


def drop_table_test():
	query = """ DROP TABLE test """
	db_connect(query)


def create_table_test():
	# создаём таблицу с тестами
	# т.к таблица нужна всего одна для каждого теста, хардкодим ее

	query = """ CREATE TABLE IF NOT EXISTS test(
				id INTEGER,
				title TEXT NOT NULL, 
				question TEXT NOT NULL, 
				answer TEXT NOT NULL, 
				left_answer TEXT NOT NULL,
				last_results TEXT DEFAULT 'None',
				PRIMARY KEY (ID) ) """
	db_connect(query)


def add_test(title, question, answer, left_answer='!!!'):
	query = """ 
				INSERT INTO test (title, question, answer, left_answer) 
				VALUES ('{0}', '{1}', '{2}', '{3}')
			 """.format(title, question, answer, left_answer)
	db_connect(query)


def get_test(test_title='', get_all=False):
	assert len(test_title) > 3 or get_all, 'Передана слишком короткая длинна теста'
	assert isinstance(test_title, str), 'title должно быть строкой'

	if get_all:
		query = """ SELECT * FROM test """
	else:
		query = """ SELECT * FROM test WHERE title='{0}' """.format(test_title)

	responce = db_connect(query)
	
	if responce:
		data = responce.fetchall()
		tests_list = []
		for test in data:
			test = [test[1], test[2].split('--!--'), test[3].split('--!--'), test[4].split('--!--')]
			if test[3][0] == '!!!':
				test[3] = '!!!'
			if not get_all:
				return test
			tests_list.append(test)

		return tests_list

	return 500


def delete_test(test_title):
	if not test_title:
		print('Введите title теста')
		return False

	query = """ DELETE FROM test WHERE title='{0}' """.format(test_title)
	db_connect(query)



if __name__ == '__main__':
	#create_table_test()
	#print(add_test(
	#		'1111', 
	#		'113213--!--hhс2--!--nnс3',
	#		'0000--!--66662--!--113'
	#	))

	delete_test('1111')

	
	#drop_table_test()
	tests = get_test(get_all=True)
	print(tests)