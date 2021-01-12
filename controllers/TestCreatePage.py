from tkinter import *
from tkinter import messagebox

from controllers.BaseController import BasePage
from models import save_test
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
		self.widgets_setup()	


	def widgets_setup(self):
		self.widgets.append(
			(Button(self.root, text='<= back', bg=YELLOW, command=self.to_menu_page), 20, 20))
		
		self.widgets.append((
			Label(self.root, text="Title: "), 20, 60))		
		self.widgets.append((
			Entry(self.root, width=20), 70, 60))
		self.widgets.append((
			Button(self.root, text='Create!', bg=YELLOW, command=self.create_test), 210, 60))
		self.widgets.append((
			Button(self.root, text='add new field', bg=BLUE, command=self.add_new_field), 270, 60))
		self.widgets.append((
			Label(self.root, text="3 requirement fields", bg=RED), 20, 100))

		# Добавляем 3 поля
		for i in range(3):
			self.widgets.append((
				Label(self.root, text="Quesction#{0}: ".format(i+1)), 20, 140+i*40))
			self.widgets.append((
				Entry(self.root, width=15), 110, 140+i*40))
			self.widgets.append((
				Label(self.root, text="Answer#{0}: ".format(i+1)), 220, 140+i*40))
			self.widgets.append((
				Entry(self.root, width=15), 290, 140+i*40))

	# коллбеки кнопок. имя функции - название кнопки
	def create_test(self): # first act
		# функция собирает все введённые пользователем значения из Entry.
		# Cохраняет функцией save_test, которая вернёт текст ошибки, либо сохранит тест. 
		# Если валидация не пройдена вызывает пользователю сообщение об ошибке

		inputs = []
		for widget in self.widgets:
			if widget[0].__class__ == Entry:
				inputs.append(widget[0].get())
		
		# проверка что поля не пустые
		if not self.check_fill(inputs):
			messagebox.showinfo('Error', 'Все поля должны быть заполнены минимум на 3 симв.')
			return False
		self.inputs = inputs
		self.please_add_left_answers() 


	def save_test(self):
		result = save_test(self.inputs[0], self.inputs[1::2], self.inputs[2::2], self.left_answer)
		if not (result is True):
			messagebox.showinfo('Error', result)


	def add_new_field(self):
		# добавляет новое поле, перемещает кнопку "del" на это поле,
		# если это первое добавленное поле, создаёт эту кнопку.
		# "del" - даёт возможность удалить поле и находится всегда на последнем добавленном поле.
		
		y = self.widgets[-1][2] + 40 # такой отступ будет от верхней границы
		num = 'N' # номер вопроса в тесте

		if y >= 500:
			messagebox.showinfo('Warning', 'Добавочных полей слишком много')
			return False
		
		# проверяем - это первое доп.поле или нет, если да то создаём кнопку "del"
		if self.widgets[-1][0].__class__ != Button:
			btn = Button(self.root, text='del', bg=RED)
			btn.bind('<Button-1>', self.del_field)
		else:
			btn = self.widgets.pop()[0] # берём инстанс

		self.widgets.append((
			Label(self.root, text="Ques#{0}: ".format(num)), 20, y))
		self.widgets.append((
			Entry(self.root, width=15), 90, y))
		self.widgets.append((
			Label(self.root, text="Ans#{0}: ".format(num)), 200, y))
		self.widgets.append((
			Entry(self.root, width=15), 260, y))
		self.widgets.append([
			btn, 360, y]) # добавляем list !!! т.к координаты придётся менять

		for widget in self.widgets[-5:]:
			widget[0].place(x=widget[1], y=widget[2])


	def del_field(self, e):
		for widget in self.widgets[-5:-1]:
			widget[0].place_forget()

		# удаляем field из памяти класса 
		if len(self.widgets) == 23: # если остались только обязательные поля
			self.widgets[-1][0].place_forget()
			self.widgets = self.widgets[:-5]
		else:
			self.widgets = self.widgets[:-5] + [self.widgets[-1]]
			self.widgets[-1][2] -= 40
			self.widgets[-1][0].place(x=self.widgets[-1][1], y=self.widgets[-1][2])

	# second act
	def please_add_left_answers(self):
		# Когда вопросы с ответами уже введены, просим пользрвателя 
		# добавить побочные ответы, для варинтов ответа
		'''for widget in self.widgets[1:]: # оставляем только кнопку "<=back"
			widget[0].place_forget()
		self.widgets[0][0]['command'] = self.back_to_first_act

		self.widgets.append((Label(self.root, text=self.second_act_txt), 20, 60))
		self.widgets.append((
				Entry(self.root, width=20), 20, 90))
		for widget in self.widgets[-2:]:
			widget[0].place(x=widget[1], y=widget[2])''' #Warning
		pass


	def back_to_first_act(self):
		for widget in self.widgets[:-2]: # восстанавливаем first act. '-2' - эл. second act`a
			widget[0].place(x=widget[1], y=widget[2])
		self.widgets[0][0]['command'] = self.to_menu_page

	# саппорт функции
	def check_fill(self, values_fields):
		# принимает list значений полей, возвращает true если поля не пустые
		# иначе false
		for value in values_fields:
			if len(value) < 3:
				return False
		return True
