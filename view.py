import tkinter as tk
from tkinter import ttk

class View(tk.Tk):

	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.title('ToDo')

		# Tkinter Variables
		self.tkNewTask = tk.StringVar()

		# creating interface
		self._create_menu()
		self._create_list()
		self._create_form()

	# Creating menus
	def _create_menu(self):
		menu_bar = tk.Menu()

		debug_menu = tk.Menu(menu_bar, tearoff=False)
		debug_menu.add_command(label='Print Array', command=lambda: self.controller.print_task_array())

		menu_bar.add_cascade(label='Debug', menu=debug_menu)
		self.config(menu=menu_bar)

	# Create frame to put ToDos inside
	def _create_list(self):
		self.task_list = tk.Frame(self)
		self.task_list.pack(expand=True, fill='both', padx=20, pady=20)

	# Create Input box with text area and button
	def _create_form(self):
		frame = tk.Frame(self, bg='pink')

		tk.Entry(frame, textvariable=self.tkNewTask).pack(side='left', expand=True, fill='x')
		tk.Button(frame, text='Add task', command=lambda: self.controller.add_task(self.tkNewTask.get())).pack(side='left')

		frame.pack(side='bottom', expand=True, fill='x', padx=20, pady=20)

	# add item to frame created in _create_list()
	def add_task_to_table(self, task):
		task_status = tk.BooleanVar(value=task.done)
		task_description = task.task_description

		frame = tk.Frame(self.task_list)
		tk.Checkbutton(frame, text=task_description, variable=task_status, command=lambda: self.controller.swap_task_status(task)).pack(side='left')
		frame.pack(expand=True, fill='x')

	def main(self):
		self.mainloop()