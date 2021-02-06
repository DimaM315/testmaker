import sqlite3


def create_table_test():
	# создаём таблицу с тестами
	# т.к таблица нужна всего одна для каждого теста, хардкодим ее

	with sqlite3.connect('db/db_test.db') as db:
		cursor = db.cursor()
		query = """ CREATE TABLE IF NOT EXISTS test(
				id INTEGER,
				title TEXT, 
				question TEXT, 
				answer TEXT, 
				left_answer TEXT,
				last_results TEXT) """

		cursor.execute(query)


def add_test(title, question, answer, left_answer='!!!'):
	with sqlite3.connect('db/db_test.db') as db:
		cursor = db.cursor()
		query = """ 
				INSERT INTO test ( id, title, question, answer, left_answer, last_results) 
				VALUES ( 2, '{0}', '{1}', '{2}', '{3}', 'None')
				 """.format(title, question, answer, left_answer)

		cursor.execute(query)
		# cursor.executemany(
		#		"INSERT INTO test VALUES (?,?,?, ?,?,?)", 
		#	 	[(2, title, question, answer, left_answer, 'None')]
		# ) функция принимает запрос и список картежей с данными, где картеж - строка в таблице
		db.commit()


def get_test():
	with sqlite3.connect('db/db_test.db') as db:
		cursor = db.cursor()
		query = """ SELECT * FROM test """
		data = cursor.execute(query)
		print(data.fetchall())
		db.commit()


def delete_test(test_title):
	if not test_id:
		print('Введите title теста')
		return False

	with sqlite3.connect('db/db_test.db') as db:
		cursor = db.cursor()
		query = """ DELETE FROM test WHERE title={0}""".format(test_title)
		cursor.execute(query)
		db.commit()



if __name__ == '__main__':
	#add_test(
	#		'Main test', 
	#		'Вопрос1--!--Вопрос2--!--Вопрос3--!--Вопрос4--!--Вопрос5--!--Вопрос6',
	#		'Ответ1--!--Ответ2--!--Ответ3--!--Ответ4--!--Ответ5--!--Ответ6'
	#	)

	#delete_test(1)

	get_test()