from tkinter import *

from controllers.BaseController import BasePage
from settings import YELLOW, BLUE, RED


class StartTestPage(BasePage):
	"""docstring for StartTestPage"""
	def __init__(self, root, to_catalog_page):
		super().__init__(root)
		self.to_catalog_page = to_catalog_page

		self.widgets_setup()


	def widgets_setup(self):
		self.widgets.append(
			(Button(self.root, text='<= back', bg=YELLOW, command=self.to_catalog_page), 20, 20))
