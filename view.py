import tkinter as tk
from tkinter import ttk

class View(tk.Tk):

	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.title('ToDo')
		self.geometry('300x400')
		self.minsize(width=300, height=350)

		# Tkinter Variables
		self.tkNewTask = tk.StringVar()

		# creating interface
		self._create_menu()
		self.task_list_widget = ScrollableFrame(self)
		self.task_list_widget.pack(fill='both', expand=True, padx=20, pady=20)
		self._create_form()

		# Bindings
		self.bind("<Return>", lambda e: self.controller.add_task(self.tkNewTask.get()))

	def _create_menu(self):
		"""
		This method is used to create menu of the program
		"""
		menu_bar = tk.Menu()

		# File menu
		file_menu = tk.Menu(menu_bar, tearoff=False)
		menu_bar.add_cascade(label="File", menu=file_menu)
		file_menu.add_command(label='Save', command=lambda: self.controller.save())
		file_menu.add_command(label='Load', command=lambda: self.controller.load())

		# Debug menu
		debug_menu = tk.Menu(menu_bar, tearoff=False)
		menu_bar.add_cascade(label='Debug', menu=debug_menu)
		debug_menu.add_command(label='Print Array', command=lambda: self.controller.print_task_array())
		debug_menu.add_command(label='Clear tasks', command=lambda: self.controller.remove_all_task())

		self.config(menu=menu_bar)

	def _create_form(self):
		"""
		Create and locate frame with inputs
		"""
		frame = tk.Frame(self)

		tk.Entry(frame, textvariable=self.tkNewTask).pack(side='left', expand=True, fill='x')
		tk.Button(frame, text='Add task', command=lambda: self.controller.add_task(self.tkNewTask.get())).pack(side='left')

		frame.pack(side='bottom', expand=False, fill='x', padx=20, pady=20)

	def clear_list(self):
		self.task_list_widget.clear_frame()

	def clear_input(self):
		self.tkNewTask.set("")

	def add_tasks(self, tasks):
		for task in tasks:
			self.add_task_to_table(task)

	def add_task_to_table(self, task):
		"""
		This method is used to add task to view.
		"""
		task_status = tk.IntVar(value=1 if task.done else 0)
		task_description = task.task_description

		frame = ttk.Frame(self.task_list_widget.scrollable_frame)
		tk.Checkbutton(
			frame,
			text=task_description,
			variable=task_status,
			command=lambda t=task, v=task_status: self._update_task_status(t, v),
			anchor='w'
		).pack(side='top', anchor='w')

		ttk.Separator(frame, orient='horizontal').pack(fill='x')
		frame.pack(expand=False, fill='x')

	def _update_task_status(self, task, task_status):
		task.done = bool(task_status.get())
		self.controller.save()

	def main(self):
		self.mainloop()

class ScrollableFrame(ttk.Frame):
	def __init__(self, container, *args, **kwargs):

		super().__init__(container, *args, **kwargs)

		self.canvas = tk.Canvas(self)
		self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.scrollbar.set)
		self.scrollable_frame = ttk.Frame(self.canvas)
		self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.scrollbar.pack(side="right", fill="y", padx=10)

		self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
		self.canvas.bind("<Configure>", self._on_canvas_configure)
		self.bind_all("<MouseWheel>", self._on_mouse_wheel)

	def _on_frame_configure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def _on_canvas_configure(self, event):
		self.canvas.itemconfig(self.scrollable_window, width=event.width)

	def _on_mouse_wheel(self, event):
		self.canvas.yview_scroll(-1 * event.delta, "units")

	def clear_frame(self):
		for widget in self.scrollable_frame.winfo_children():
			widget.destroy()
