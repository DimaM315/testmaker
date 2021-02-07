from random import randint

from settings import *
import db


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
	# удаляем non_symb с начала и конца, меняем все заглавные буквы на строчные
	assert isinstance(text, str) and len(text) > 2, 'Uncorrectable arguments got prepare_save'

	text = text.replace('\n', '').strip()
	
	non_symb = '/!$%;>\'\"-<@#'
	prepared_text = ''
	
	for i in range(len(text)):
		if (text[i] == ' ' and text[i+1] == ' ') or text[i] in non_symb:
			continue
		prepared_text += text[i]

	return prepared_text.lower()


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
		answer_list[i] = prepare_save(answer_list[i])
		question_list[i] += '?' if question_list[i][-1] != '?' else ''
		
		
	if left_answer != '!!!':
		for i in range(len(left_answer)):
			left_answer[i] = prepare_save(left_answer[i])
	
	# превращаем эти массивы в строки для БД
	q_str = '--!--'.join(question_list)
	a_str = '--!--'.join(answer_list)
	l_str = '--!--'.join(left_answer) if left_answer != '!!!' else '!!!'
	
	db.add_test(title, q_str, a_str, l_str)

	return True
	

# methods for test copmilete
def get_variants_list(answer, from_choose):
	assert isinstance(answer, str) and len(answer) > 2,\
					"Функция get_variants_list, вызвана без корректного ответа"
	assert isinstance(from_choose, list) and len(from_choose) > 3, \
					"Функция get_variants_list, вызвана без корректного from_choose"
	
	variants_answer = [answer] + [0]*2 

	while 0 in variants_answer:
		for i in (1,2):
			rand_pos = randint(0, len(from_choose)-1)	
			variants_answer[i] = from_choose[rand_pos] if from_choose[rand_pos] not in variants_answer else 0

	# MIXing of List
	rand_pos = randint(0, 2)
	variants_answer[0], variants_answer[rand_pos] = variants_answer[rand_pos], variants_answer[0]

	return variants_answer

if __name__ == '__main__':
	pass
	#print(save_test('title', ['que1','que2','que3'], ['ans1','ans2','ans3']))