from tkinter import *
from tkinter import messagebox

from controllers.BaseController import BasePage
from settings import YELLOW, BLUE, RED


class MenuPage(BasePage):
	"""docstring for TestCatalogPage"""

	def __init__(self, root, to_create_page, to_catalog_page):
		super().__init__(root)
		# функции перехода между страницами
		self.to_create_page = to_create_page
		self.to_catalog_page = to_catalog_page
		
		self.widgets_setup()

	
	def widgets_setup(self):
		# создаём необходимые инстенцы виджетов и их координаты
		# добавляем их в self.widgets
		self.widgets.append(
			(Button(self.root, text='Create test', bg=YELLOW, command=self.to_create_page), 140, 100))# x, y
		self.widgets.append(
			(Button(self.root, text='Chose test', bg=YELLOW, command=self.to_catalog_page), 140, 200)) 
		self.widgets.append(
			(Button(self.root, text='Exit', bg=RED, command=self.root.destroy), 140, 300))
		# set common attr
		for widget in self.widgets:
			widget[0]['font'] = 'Consolas 13'
			widget[0]['width'] = 15