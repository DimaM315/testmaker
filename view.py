import controllers as c


class View:
	"""docstring for View
       класс заниматся управлением перемещения
       по страницам. Работает с объектами страниц,
       передаёт этим объектам необходимые событийные функции.
	"""

	def __init__(self, root):
		self.menu_page = c.MenuPage(root, self.to_create_page, self.to_catalog_page)
		self.catalog_page = c.TestCatalogPage(root, self.to_menu_page, self.to_start_test_page)
		self.create_page = c.TestCreatePage(root, self.to_menu_page)
		self.start_test_page = c.StartTestPage(root, self.to_catalog_page)


	def start(self):
		self.menu_page.status = 'on'
	

	def to_create_page(self):
		self.__all_off()
		self.create_page.status = 'on'
		

	def to_catalog_page(self):
		self.__all_off()
		self.catalog_page.check_new_test()
		self.catalog_page.status = 'on'


	def to_menu_page(self):
		self.__all_off()
		self.menu_page.status = 'on'


	def to_start_test_page(self, test_title):
		self.__all_off()
		self.start_test_page.status = 'on'
		self.start_test_page.start_test(test_title)


	def __all_off(self):
		for attr in self.__dict__:
			self.__dict__[attr].status = 'off'