from random import randint

from settings import *


def get_root_settings(tk_obj):
	# window settings
	tk_obj.title(prg_title)
	tk_obj.resizable(width=False, height=False)
	tk_obj.geometry(prg_geometry)
	tk_obj.wm_attributes('-alpha', 1)
	tk_obj['bg'] = prg_bg
	#tk_obj.resizable(prg_resizeable)
	
	return tk_obj


# methods for test manipulate

def prepare_save(text):
	# удаление /n
	text = ''.join(text.split('\n'))
	
	# удаляем non_symb с начала и конца коммента,
	# меняем все заглавные буквы на строчные
	non_symb = '/!$%;>-<@#'
	ex = ''
	
	while text[0] in non_symb+" ":
		text = text[1:]
	while text[len(text)-1] in non_symb+" ":
		text = text[:len(text)-1]

	for i in range(len(text)):
		if (text[i] == ' ' and text[i+1] == ' ') or text[i] in non_symb:
			continue
		ex += text[i]

	return ex.lower()


def save_test(title, question_list, answer_list, left_answer='!!!'):
	# question_list - список воросов 
	# answer_list - ответы, причём answer_list[n] отвечает на вопрос question_list[n]
	# left_answer - "левые" ответы, будут использованы как варианты ответа.
	
	if (len(question_list) != len(answer_list) 
		or len(question_list) < 3 
		or len(question_list) > 20):
		return 'Ошбика в количестве элем. массива question_list. >3 <20 ==answer_list'
	if len(title) < 2 or len(title) > 30 or not isinstance(title, str):
		return 'Ошбика в названии тест. >3 <30 str'
	
	# обработка текста перед сохранением
	for i in range(len(question_list)):
		question_list[i] = prepare_save(question_list[i])
		# если последний символ каждого вопроса не ?, добавляем его в конец 
		if question_list[i][len(question_list[i])-1] != '?':
			question_list[i] += '?'
		answer_list[i] = prepare_save(answer_list[i])
		
	if left_answer != '!!!':
		for i in range(len(left_answer)):
			left_answer[i] = prepare_save(left_answer[i])
	
	# превращаем эти массивы в текст для БД
	q_str = '--!--'.join(question_list)
	a_str = '--!--'.join(answer_list)
	l_str = '--!--'.join(left_answer) if left_answer != '!!!' else '!!!'
	
	test_str = '{title}\n{question}\n{answer}\n{left_answer}'.format(
		title=title, question=q_str, answer=a_str, left_answer=l_str
	)

	#with open(FILE_DB, 'a', encoding='utf-8') as file:
	#	file.write('\n\n\n'+test_str)

	return True


def load_tests(title='none'):
	assert isinstance(title, str), 'title должно быть строкой'

	# если title='none' вернёт все тесты, 
	# если конкретный будет путаться найти и вернуть только его
	with open(FILE_DB, 'r', encoding='utf-8') as file:
		data = file.read()
	
	tests_list = []
	for test in data.split('\n\n\n'):
		tests_list.append([*test.split('\n')])

	for i in range(len(tests_list)):
		tests_list[i][1] = tests_list[i][1].split('--!--')
		tests_list[i][2] = tests_list[i][2].split('--!--')
		if tests_list[i][3] != '!!!':
			tests_list[i][3] = tests_list[i][3].split('--!--')
		if title == tests_list[i][0]:
			return tests_list[i]

	if title != 'none':
		return 'Тест - {name} не найден'.format(name=title)

	return tests_list	
	
	

if __name__ == '__main__':
	print(load_tests('g'))
	#print(save_test('New_Test', 
				#	['How are\n\n yo\nu?', '  Where are you from?  ', '  How!!! long you jump?', 'What did you read?'], 
				#	['18 years old!', 'I am from PS!', '  My jump is 20m    long!', 'I wa  s read book!'],
				#	['In PSJ??>', 'WTF?']))
	