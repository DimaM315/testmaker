import controllers
from models import load_tests

class View:
	"""docstring for View
       класс заниматся управлением перемещения
       по страницам. Работает с объектами страниц,
       передаёт этим объектам необходимые событийные функции.
	"""
	def __init__(self, root):
		self.menu_page = controllers.MenuPage(root, self.to_create_page, self.to_catalog_page)
		self.catalog_page = controllers.TestCatalogPage(root, 
						[test[0] for test in load_tests()], # передаём titl`ы тестов
						self.to_menu_page, self.to_start_test_page)
		self.create_page = controllers.TestCreatePage(root, self.to_menu_page)
		self.start_test_page = controllers.StartTestPage(root, self.to_catalog_page)


	def start(self):
		self.menu_page.status = 'on'
	

	def to_create_page(self):
		self.menu_page.status = 'off'
		self.catalog_page.status = 'off'
		self.start_test_page.status = 'off'
		self.create_page.status = 'on'
		

	def to_catalog_page(self):
		self.menu_page.status = 'off'
		self.create_page.status = 'off'
		self.start_test_page.status = 'off'
		self.catalog_page.status = 'on'


	def to_menu_page(self):
		self.catalog_page.status = 'off'
		self.create_page.status = 'off'
		self.start_test_page.status = 'off'
		self.menu_page.status = 'on'


	def to_start_test_page(self, title):
		self.menu_page.status = 'off'
		self.catalog_page.status = 'off'
		self.create_page.status = 'off'
		self.start_test_page.status = 'on'
		print('Start test - {t}'.format(t=title))