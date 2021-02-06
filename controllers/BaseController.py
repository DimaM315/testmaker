class BasePage:

	def __init__(self, root):
		self.root = root # tk main instance

		# показывает активна страница или нет. Две позиции off/on
		self.status = 'off'
	
		# все виджиты странивы, включяет в себя списки виджитов 
		# для каждого фрейма, где фрейм на позиции 0
		# каждый виджит представляет собой кортеж (tk_inst, x_coor:int, y_coor:int)
		self.widgets = [] 


	def widgets_setup(self):
		raise NotImplementedError


	def __hidden(self):
		# функция скрывает все виджеты старницы. "страница сварачивается"
		for widget in self.widgets:
			widget[0].place_forget()


	def __active(self):
		# функция отображает все виджеты старницы. "страница разварачивается"
		for widget in self.widgets:
			widget[0].place(x=widget[1], y=widget[2])


	def __setattr__(self, key, value):
		if key == 'status' and 'status' in self.__dict__:
			if value == 'on' and self.status == 'off':
				self.__dict__['status'] = value
				self.__active()
			elif value == 'off' and self.status == 'on':
				self.__dict__['status'] = value
				self.__hidden()
		else:
			self.__dict__[key] = value
