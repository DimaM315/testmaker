from tkinter import *


from models import get_root_settings
from view import View


if __name__ == '__main__':
	root = get_root_settings(Tk())
	
	app = View(root)
	app.start()


	root.mainloop()