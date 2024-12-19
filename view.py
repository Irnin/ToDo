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
		self._create_list()
		self._create_form()

	def _create_list(self):
		frame = tk.Frame(self)
		self.table = ttk.Treeview(frame, columns=('Done', 'Task'), show='headings')
		self.table.heading('Done', text='Done')
		self.table.heading('Task', text='Task')

		self.table.pack(fill='both', expand=True)

		frame.pack(expand=True, fill='both')

	def _create_form(self):
		frame = tk.Frame(self, bg='pink')

		tk.Entry(frame, textvariable=self.tkNewTask).pack(side='left', expand=True, fill='x')
		tk.Button(frame, text='Add task', command=lambda: self.controller.add_task(self.tkNewTask.get())).pack(side='left')

		frame.pack(side='bottom', expand=True, fill='x', padx=20, pady=20)

	def add_task_to_table(self, task, done):

		done = 'Yep' if done else 'Nope'

		self.table.insert(parent='', index=0, values=(done, task))

	def main(self):
		self.mainloop()