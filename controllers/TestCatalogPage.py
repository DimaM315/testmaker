from tkinter import *
from tkinter import messagebox

from controllers.BaseController import BasePage
from settings import YELLOW, BLUE, RED


class TestCatalogPage(BasePage):
	"""docstring for TestCatalogPage
	   отображает страницу каталога всех тестов,
	   предоставляет методы управления каждым из них.
	"""

	def __init__(self, root, tests_name, to_menu_page, to_start_test_page):
		super().__init__(root)
		self.tests_name = tests_name
		# подсказка в верхней части страницы
		self.prompt_text = 'Click to test-name for start test'

		self.to_menu_page = to_menu_page
		self.to_start_test_page = to_start_test_page

		self.widgets_setup()


	def widgets_setup(self):
		# создаём необходимые инстенцы виджетов и их координаты
		# добавляем их в self.widgets
		self.widgets.append(
			(Button(self.root, text='<= back', bg=YELLOW, command=self.to_menu_page), 20, 20))# x, y
		self.widgets.append(
			(Label(self.root, text=self.prompt_text), 100, 20))
		
		for i in range(len(self.tests_name)):
			y = 70 * (i + 1.5)
			btn_test = Button(self.root, text=self.tests_name[i], bg=YELLOW, width=20)
			btn_change = Button(self.root, text='change', bg=BLUE, width=10)
			btn_del = Button(self.root, text='delete', bg=RED, width=5)
			
			for btn in btn_test, btn_change, btn_del:
				btn.bind('<Button-1>', self.clicked_action)
			
			self.widgets.append([btn_test, 20, y])
			self.widgets.append([btn_change, 200, y])
			self.widgets.append([btn_del, 320, y])
	

	def clicked_action(self, e):
		btn_text = e.widget['text']
		btn_y = e.widget.place_info()['y']
		
		if btn_text == 'change':
			# ищим title теста который нужно поменять
			# он находится в btn, стоящей первой в ряду
			for widget in self.widgets:
				if int(widget[2]) == int(btn_y):
					print('Change - ' + str(widget[0]['text']))
					return False
		elif btn_text == 'delete':
			for widget in self.widgets[::-1]: # [::-1] - обход с конца(т.к удаляем эл-ты)
				# удаляем все виджеты ряда(виджеты теста по которому кликнули)
				if int(widget[2]) == int(btn_y):
					widget[0].place_forget()
					self.widgets.remove(widget)
			self.page_rander()
		else:
			# btn_text здесь - имя теста
			self.to_start_test_page(btn_text) 
		

	def page_rander(self):
		# при удалении теста, тесты находящиеся под ним, нужно сдвинуть вверх
		# функция отвечает за обработку self.widgets и сдвиг эл-ов
		for i in range(len(self.widgets[2:])):
			# !!!!!!
			# рендерим обсолютно все виджеты тестов, а нужно только те которые ниже удалённого!!!
			y = 70 * (i//3 + 1.5)
			self.widgets[i+2][2] = y # +2 т.к в widgets первые два эл-та не относятся к текстам
			self.widgets[i+2][0].place(x=self.widgets[i+2][1], y=y)
