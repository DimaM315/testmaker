from tkinter import *
from tkinter import messagebox

from controllers.BaseController import BasePage
from models import save_test, prepare_save
from settings import YELLOW, BLUE, RED


class TestCreatePage(BasePage):
	"""docstring for TestCreatePage
	   Класс отвечает за создание нового теста, добавление его в
	   test_storage.txt
	   first act - когда пользователь заполняет поля "Вопрос-ответ"
	   second act - пользователь добавляет "побочные ответы"
	"""
	
	def __init__(self, root, to_menu_page):
		super().__init__(root)
		self.to_menu_page = to_menu_page
		self.second_act_txt = 'Enter via ";" side answers that might answer the questions you entered'
		
		self.wdg_first_act = []
		self.wdg_sec_act = []

		self.widgets_setup()	


	def widgets_setup(self):
		self.widgets.append(
			(Button(self.root, text='<= back', bg=YELLOW, command=self.to_menu_page), 20, 20))
		self.setup_first_act_frm()
		self.setup_sec_act_frm()

	# коллбеки кнопок. имя функции - название кнопки
	def create_test(self): # first act
		# функция собирает все введённые пользователем значения из Entry.
		# Cохраняет функцией save_test, которая вернёт текст ошибки, либо сохранит тест. 
		# Если валидация не пройдена вызывает пользователю сообщение об ошибке

		inputs = []
		for widget in self.wdg_first_act:
			if widget[0].__class__ == Entry:
				inputs.append(widget[0].get())
		
		# проверка что поля не пустые
		if not self.check_fill(inputs):
			messagebox.showinfo('Error', 'Все поля должны быть заполнены минимум на 3 симв.')
			return False
		self.inputs = inputs
		self.move_to_sec_act()


	def add_new_field(self):
		# добавляет новое поле, перемещает кнопку "del" на это поле,
		# если это первое добавленное поле, создаёт эту кнопку.
		# "del" - даёт возможность удалить поле и находится всегда на последнем добавленном поле.	
		y = self.wdg_first_act[-1][2] + 40 # такой отступ будет от верхней границы
		frm = self.widgets[-1][0] # frm - first act
		num =  str(len(self.wdg_first_act) // 4) # номер вопроса в тесте

		if y >= 500:
			messagebox.showinfo('Warning', 'Добавочных полей слишком много')
			return False
		
		# проверяем - это первое доп.поле или нет, если да то создаём кнопку "del"
		if self.wdg_first_act[-1][0].__class__ != Button:
			btn = Button(frm, text='del', bg=RED)
			btn.bind('<Button-1>', self.del_field)
		else:
			btn = self.wdg_first_act.pop()[0] # берём инстанс

		self.wdg_first_act.append((
			Label(frm, text=f"Ques#{num}: "), 20, y))
		self.wdg_first_act.append((
			Entry(frm, width=15), 90, y))
		self.wdg_first_act.append((
			Label(frm, text=f"Ans#{num}: "), 200, y))
		self.wdg_first_act.append((
			Entry(frm, width=15), 260, y))
		self.wdg_first_act.append([
			btn, 360, y]) # добавляем list !!! т.к координаты придётся менять

		for widget in self.wdg_first_act[-5:]:
			widget[0].place(x=widget[1], y=widget[2])


	def del_field(self, e):
		for widget in self.wdg_first_act[-5:-1]:
			widget[0].place_forget()

		# удаляем field из памяти класса 
		if len(self.wdg_first_act) == 22: # если остались только обязательные поля
			self.wdg_first_act[-1][0].place_forget()
			self.wdg_first_act = self.wdg_first_act[:-5]
		else:
			self.wdg_first_act = self.wdg_first_act[:-5] + [self.wdg_first_act[-1]]
			self.wdg_first_act[-1][2] -= 40
			self.wdg_first_act[-1][0].place(x=self.wdg_first_act[-1][1], y=self.wdg_first_act[-1][2])


	def done(self):
		left_answer = self.wdg_sec_act[1][0].get().replace(' ', '').split(';') # Entry inst
		left_answer = self.validate_left_ans(left_answer)

		if left_answer == '!!!' or self.check_fill(left_answer):
			result = save_test(self.inputs[0], self.inputs[1::2], self.inputs[2::2], left_answer)
			if not (result is True):
				messagebox.showinfo('Error', result)
			# clear Entry and hidden sec_act_frm
			self.sec_act_frm[0].place_forget()
			for wdg in self.wdg_first_act + self.wdg_sec_act:
				if wdg[0].__class__ == Entry:
					wdg[0].delete(0, END)

			messagebox.showinfo('Success', 'Test "{0}" was created'.format(self.inputs[0]))
			self.to_menu_page()
		else:
			messagebox.showinfo('Error', 'Сторонние ответы > 3 символов и через ;')

	# move an acts
	def move_to_sec_act(self):
		# Когда вопросы с ответами уже введены, просим пользрвателя 
		# добавить побочные ответы, для варинтов ответа		
		self.widgets[0][0]['command'] = self.back_to_first_act

		self.widgets[-1][0].place_forget()
		self.sec_act_frm[0].place(x=self.sec_act_frm[1], y=self.sec_act_frm[2])


	def back_to_first_act(self):
		self.widgets[0][0]['command'] = self.to_menu_page

		self.sec_act_frm[0].place_forget()
		self.widgets[-1][0].place(x=self.widgets[-1][1], y=self.widgets[-1][2])

	# саппорт функции
	def check_fill(self, values_fields):
		# принимает list значений полей, возвращает true если поля не пустые
		# иначе false
		for value in values_fields:
			if len(value) < 3:
				return False
		return True


	def validate_left_ans(self, left_ans):
		# if left_ans ';;;;'
		for ans in left_ans:
			if ans == '':
				left_ans.remove(ans)
		return left_ans if len(left_ans) > 0 else '!!!'


	def setup_first_act_frm(self):
		frm = Frame(self.root, width=400, height=440, bg='#AAAAAA')
		self.widgets.append((frm, 0, 60))
		
		self.wdg_first_act.append((
			Label(frm, text="Title: "), 20, 0))		
		self.wdg_first_act.append((
			Entry(frm, width=20), 70, 0))
		self.wdg_first_act.append((
			Button(frm, text='Create!', bg=YELLOW, command=self.create_test), 210, 0))
		self.wdg_first_act.append((
			Button(frm, text='add new field', bg=BLUE, command=self.add_new_field), 270, 0))
		self.wdg_first_act.append((
			Label(frm, text="3 requirement fields", bg=RED), 20, 40))

		# Добавляем 3 поля
		for i in range(3):
			self.wdg_first_act.append((
				Label(frm, text="Quesction#{0}: ".format(i+1)), 20, 80+i*40))
			self.wdg_first_act.append((
				Entry(frm, width=15), 110, 80+i*40))
			self.wdg_first_act.append((
				Label(frm, text="Answer#{0}: ".format(i+1)), 220, 80+i*40))
			self.wdg_first_act.append((
				Entry(frm, width=15), 290, 80+i*40))

		for widget in self.wdg_first_act:
			widget[0].place(x=widget[1], y=widget[2])


	def setup_sec_act_frm(self):
		frm = Frame(self.root, width=400, height=440, bg='#AAAAAA')
		self.sec_act_frm = (frm, 0, 60)

		self.wdg_sec_act.append((Label(frm, text=self.second_act_txt), 20, 0))
		self.wdg_sec_act.append((Entry(frm, width=40), 20, 30))
		self.wdg_sec_act.append((Button(frm, text='Done!', bg=YELLOW, command=self.done), 320, 30))

		for wdg in self.wdg_sec_act:
			wdg[0].place(x=wdg[1], y=wdg[2])

		