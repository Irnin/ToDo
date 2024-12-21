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

		# Bindings
		self.bind("<Return>", lambda e: self.controller.add_task(self.tkNewTask.get()))

	# Creating menus
	def _create_menu(self):
		menu_bar = tk.Menu()

		file_menu = tk.Menu(menu_bar, tearoff=False)
		file_menu.add_command(label='Save', command=lambda: self.controller.save())
		file_menu.add_command(label='Load', command=lambda: self.controller.load())

		debug_menu = tk.Menu(menu_bar, tearoff=False)
		debug_menu.add_command(label='Print Array', command=lambda: self.controller.print_task_array())

		menu_bar.add_cascade(label="File", menu=file_menu)
		menu_bar.add_cascade(label='Debug', menu=debug_menu)
		self.config(menu=menu_bar)

	# Create frame to put ToDos inside
	def _create_list(self):
		self.task_list = tk.Frame(self)
		self.task_list.pack(expand=False, fill='both', padx=20, pady=20)

	def clear_list(self):
		for widget in self.task_list.winfo_children():
			widget.destroy()

	def clear_input(self):
		self.tkNewTask.set("")

	# Create Input box with text area and button
	def _create_form(self):
		frame = tk.Frame(self, bg='pink')

		tk.Entry(frame, textvariable=self.tkNewTask).pack(side='left', expand=True, fill='x')
		tk.Button(frame, text='Add task', command=lambda: self.controller.add_task(self.tkNewTask.get())).pack(side='left')

		frame.pack(side='bottom', expand=False, fill='x', padx=20, pady=20)

	def add_tasks(self, tasks):
		for task in tasks:
			self.add_task_to_table(task)

	# add item to frame created in _create_list()
	def add_task_to_table(self, task):
		task_status = tk.IntVar(value=1 if task.done else 0)
		task_description = task.task_description

		frame = tk.Frame(self.task_list)
		tk.Checkbutton(
			frame,
			text=task_description,
			variable=task_status,
			command=lambda t=task, v=task_status: self._update_task_status(t, v),
			anchor='w'
		).pack(side='top', anchor='w')

		ttk.Separator(frame, orient='horizontal').pack(fill='x')
		frame.pack(side='top', expand=True, fill='x')

	def _update_task_status(self, task, task_status):
		task.done = bool(task_status.get())
		self.controller.save()

	def main(self):
		self.mainloop()