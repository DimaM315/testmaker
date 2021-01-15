from tkinter import *
from tkinter import messagebox

from controllers.BaseController import BasePage
from models import load_tests, del_test
from settings import YELLOW, BLUE, RED


class TestCatalogPage(BasePage):
	"""docstring for TestCatalogPage
	   отображает страницу каталога всех тестов,
	   предоставляет методы управления каждым из них.
	"""

	def __init__(self, root, to_menu_page, to_start_test_page):
		super().__init__(root)
		self.tests_name = [test[0] for test in load_tests()]
		# подсказка в верхней части страницы
		self.prompt_text = 'Click to test-name for start test'

		self.to_menu_page = to_menu_page
		self.to_start_test_page = to_start_test_page

		self.widgets_setup()


	def widgets_setup(self):
		self.widgets.append(
			(Button(self.root, text='<= back', bg=YELLOW, command=self.to_menu_page), 20, 20))# x, y
		self.widgets.append(
			(Label(self.root, text=self.prompt_text), 100, 20))

		for i, title in enumerate(self.tests_name):
			y = 70 * (i + 1.5)
			self.add_new_row(title, y)
	

	def clicked_action(self, e):
		btn_text = e.widget['text']
		btn_y = int(e.widget.place_info()['y'])
		
		if btn_text == 'change':	
			# ищим title теста который нужно поменять - текст кнопки
			for widget in self.widgets:
				if widget[2] == btn_y:
					print('Change - ' + widget[0]['text'])
					break
		elif btn_text == 'delete':
			for widget in reversed(self.widgets):
				# удаляем с конца все виджеты ряда(виджеты теста по которому кликнули)
				if widget[2] == btn_y:
					self.del_widget(widget)
					
					if widget[0]['text'] in self.tests_name:
						test_title = widget[0]['text']
						self.delete_test(test_title)
			
			self.page_rander()

		elif btn_text in self.tests_name:
			self.to_start_test_page(btn_text)
		

	def delete_test(self, title):
		# удаляем title из памяти объекта
		self.tests_name.remove(title)
		del_test(title)


	def page_rander(self):
		# при удалении теста, тесты находящиеся под ним, нужно сдвинуть вверх
		for widget, i in enumerate(self.widgets[2:]):
			# update y
			y = 70 * (i//3 + 1.5)
			widget[2] = y 
			widget[0].place(x=widget[1], y=y)


	def check_new_test(self):
		# если пользователь до перехода в Каталог, создал тест. Он уже должен отображаться
		new_titles =  [test[0] for test in load_tests()]
		if len(self.tests_name) < len(new_titles):
			# появился новый тестs
			for title in new_titles:
				if title not in self.tests_name:
					y = 70 * (len(self.tests_name) + 1.5)
					self.add_new_row(title, y)
					self.tests_name.append(title)


	def add_new_row(self, title, y):
		btn_test = Button(self.root, text=title, bg=YELLOW, width=20)
		btn_change = Button(self.root, text='change', bg=BLUE, width=10)
		btn_del = Button(self.root, text='delete', bg=RED, width=5)
					
		for btn, x in (btn_test, 20), (btn_change, 200), (btn_del, 320):
			btn.bind('<Button-1>', self.clicked_action)	
			self.widgets.append([btn, x, y])

	# вспомогательные функции
	def del_widget(self, widget_data):
		# widget_data - tuple from self.widgets
		assert len(widget_data) == 3 , 'Неправильная widget_data в func: del_widget'
		
		widget_data[0].place_forget()
		self.widgets.remove(widget_data)