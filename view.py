import tkinter as tk

class View(tk.Tk):

	def __init__(self, controller):
		super().__init__()
		self.controller = controller