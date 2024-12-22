import tkinter as tk
from tkinter import ttk

from model import Task

class View(tk.Tk):

	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.title('ToDo')
		self.minsize(width=300, height=200)

		# Tkinter Variables
		self.tkNewTask = tk.StringVar()

		# creating interface
		self._create_menu()
		self.task_list_widget = TaskListWidget(self) # <---
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

	# Create Input box with text area and button
	def _create_form(self):
		frame = tk.Frame(self)

		inner_frame = tk.Frame(frame)

		tk.Entry(frame, textvariable=self.tkNewTask).pack(side='left', expand=True, fill='x')
		tk.Button(frame, text='Add task', command=lambda: self.controller.add_task(self.tkNewTask.get())).pack(
			side='left')

		#inner_frame.pack(fill='x', padx=20, pady=20)

		frame.pack(side='bottom', expand=False, fill='x', padx=20, pady=20)
		#frame.place(rely=1, relx=0, relwidth=1, anchor='sw')

	def clear_list(self):
		pass
		#for widget in self.task_list_view.winfo_children():
		#	widget.destroy()

	def clear_input(self):
		self.tkNewTask.set("")

	def add_tasks(self, tasks):
		for task in tasks:
			self.add_task_to_table(task)

	# add item to frame created in _create_list()
	def add_task_to_table(self, task):
		self.task_list_widget.add_item(task)

	def _update_task_status(self, task, task_status):
		task.done = bool(task_status.get())
		self.controller.save()

	def main(self):
		self.mainloop()

# This class is responsible for displaying task in main view
# Needed to separate this code, because tkinker doesn't support this functionality
class TaskListWidget(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.view = parent

		self.pack(expand=True, fill='both', padx=20, pady=20)
		#self.place(relx=0, rely=0, relwidth=1, relheight=0.9)
		self.list_height = 0

		self.list_height = 25 * self.view.controller.get_amount_of_task()
		print(self.list_height)

		# LAYOUT
		self.task_view = tk.Canvas(self, scrollregion=(0, 0, self.winfo_width(), self.list_height))
		self.task_frame = ttk.Frame()
		self.scroll_bar = ttk.Scrollbar(self, orient='vertical', command=self.task_view.yview)
		self.task_view.configure(yscrollcommand=self.scroll_bar.set)

		self.task_view.pack(side='left', expand=True, fill='both')
		self.scroll_bar.pack(side='right', expand=False, fill='y', padx=10)

		#EVENTS
		self.bind('<Configure>', self._update_size)

	def add_item(self, task: Task):
		task_status = tk.IntVar(value=1 if task.done else 0)
		task_description = task.task_description

		frame = ttk.Frame(self.task_frame)
		tk.Checkbutton(
			frame,
			text=task_description,
			variable=task_status,
			command=lambda t=task, v=task_status: lambda: print("TO DO Update Status"), # <=== TODO update status on clic
			anchor='w'
		).pack(side='top', anchor='w')

		ttk.Separator(frame, orient='horizontal').pack(fill='x')
		frame.pack(expand=False, fill='x')

	def on_mouse_wheel(self, e):
		if e.state == 1:
			return
		else:
			self.task_view.yview_scroll(-1 * e.delta, 'unit')

	def _update_size(self, event):
		if self.list_height >= self.winfo_height():
			height = self.list_height
			self.bind_all('<MouseWheel>', lambda e: self.on_mouse_wheel(e))
		else:
			height = self.winfo_height()
			self.unbind_all('<MouseWheel>')

		self.task_view.create_window((0,0), window = self.task_frame, anchor='nw', width=self.task_view.winfo_width(), height=height)
