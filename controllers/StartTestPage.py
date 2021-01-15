from tkinter import *
from tkinter import messagebox

from controllers.BaseController import BasePage
from models import load_tests, get_variants_list
from settings import YELLOW, BLUE, RED, prg_bg


class StartTestPage(BasePage):
	"""docstring for StartTestPage
		cople = (ques, answ) change by step
		mode: write(wr) and choose(ch)/ write upon left_answer == '!!!'
		Structure self.frm_widgets:
		[0] - Lable - quesction
		[1] - Entry - wr
		[2] - Button - wr
		[3:6] - Button - ch
	"""

	def __init__(self, root, to_catalog_page):
		super().__init__(root)
		self.to_catalog_page = to_catalog_page

		self.step = 0
		self.greats = 0
		self.test = None
		self.cople = ()

		self.frm_widgets = []
		self.widgets_setup()


	def widgets_setup(self):
		self.widgets.append(
			(Button(self.root, text='<= back', bg=YELLOW, command=self.to_catalog_page), 20, 20))
		
		self.frm = Frame(self.root, width=400, height=440, bg=prg_bg)
		self.widgets.append((self.frm, 0, 60))

		self.frm_widgets.append((Label(self.frm), 10, 10))
		self.frm_widgets[0][0].place(x=10, y=10)

		# write(wr) mode`s wdg
		self.frm_widgets.append((Entry(self.frm, width=25), 10, 70))
		self.frm_widgets.append((Button(self.frm, text='Done!', bg=YELLOW, command=self.handler_wr_btn), 210, 70))

		# choose(ch) mode`s wdg
		for i in range(3):
			self.frm_widgets.append((Button(self.frm, bg=YELLOW), 20 + 130*i, 70))
			self.frm_widgets[3+i][0].bind('<Button-1>', self.handler_ch_btn)


	def start_test(self, title_test):
		# если юзер стартовал какой-то тест, потом перешёл в каталог и начал новый
		if self.test and title_test != self.test['title']:	
			messagebox.showinfo('Error', 'В начале пройдите тест {0}'.format(self.test['title']))
			self.to_catalog_page()
			return True
		
		test_data = load_tests(title_test)
		self.test = {'title': test_data[0], 'questions': test_data[1], 
					'answers': test_data[2], 'left': test_data[3]}

		self.sub_widget_visible('on')
		self.step_up()


	def finish_test(self):
		messagebox.showinfo('Results', "Game over, right answer: {0}/{1}".format(self.greats, self.step))
		self.sub_widget_visible('off')

		self.step = 0
		self.greats = 0
		self.test = None	


	def step_up(self):
		if self.step >= len(self.test['questions']):
			self.finish_test()
			self.to_catalog_page()
			return True

		self.cople = self.get_cople()
		self.frm_widgets[0][0]['text'] = '{0}. Ans#{1} {2}'.format(self.test['title'], self.step+1, self.cople[0])

		if self.test['left'] != '!!!': 
			self.ch_mode_func()


	def ch_mode_func(self):
		# mode ch. Must do create left_ans for self.frm_widgets[3:]
		tmp_answer = self.cople[1]
		from_choose = self.test['answers'] + self.test['left']
		
		for i, possible_answer in enumerate(get_variants_list(tmp_answer, from_choose)):
			self.frm_widgets[3+i][0]['text'] = possible_answer


	# вспомогательные функции
	def sub_widget_visible(self, status):
		# status : 'on' - active or 'off' - hidden
		if self.test['left'] == '!!!':
			for widget in self.frm_widgets[1:3]:
				if status == 'on':
					widget[0].place(x=widget[1], y=widget[2])
				elif status == 'off':
					widget[0].place_forget()
			return True
		for widget in self.frm_widgets[3:]:
			if status == 'on':
				widget[0].place(x=widget[1], y=widget[2])
			elif status == 'off':
				widget[0].place_forget()


	def get_cople(self):
		ques = self.test['questions'][self.step]
		ans = self.test['answers'][self.step]
		return (ques, ans)


	# функции - обработчики кнопок
	def handler_wr_btn(self):
		user_answer = self.frm_widgets[1][0].get().replace(' ', '')
		self.frm_widgets[1][0].delete(0, END)

		self.step += 1
		self.greats += 1 if self.cople[1] == user_answer else 0
		self.step_up()


	def handler_ch_btn(self, e):	
		user_answer = e.widget['text']

		self.step += 1
		self.greats += 1 if self.cople[1] == user_answer else 0
		self.step_up()