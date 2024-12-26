import tkinter as tk
from tkinter import ttk
from model import Task

class View(tk.Tk):

	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.title('ToDo')
		self.geometry('300x400')
		self.minsize(width=400, height=350)

		# Tkinter Variables
		self.tkNewTask = tk.StringVar()
		self.tkDisplayedTask = tk.StringVar(value='All')

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

		# View menu
		view_menu = tk.Menu(menu_bar, tearoff=False)
		menu_bar.add_cascade(label='View', menu=view_menu)
		view_menu.add_radiobutton(label='All', variable=self.tkDisplayedTask, command=lambda: self.controller.display_tasks(self.tkDisplayedTask.get()))
		view_menu.add_radiobutton(label='Unfinished tasks', variable=self.tkDisplayedTask, value='Unfinished', command=lambda: self.controller.display_tasks(self.tkDisplayedTask.get()))
		view_menu.add_radiobutton(label='Finished tasks', variable=self.tkDisplayedTask, value='Finished', command=lambda: self.controller.display_tasks(self.tkDisplayedTask.get()))

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
		"""
		Method clears all elements in task list view. It does nothing with model data
		"""
		self.task_list_widget.clear_frame()

	def displayed_task(self) -> str:
		kind = self.tkDisplayedTask.get()
		return kind

	def clear_input(self):
		"""
		Clear input after user insert element
		"""
		self.tkNewTask.set("")

	def display_task_details(self, task: Task):
		"""
		Opens new window to display details about selected task
		"""
		top_window = tk.Toplevel(self)
		top_window.title(task.heading)
		top_window.minsize(width=400, height=300)

		frame = DetailsFrame(top_window, self.controller, task)
		frame.pack(padx=20, pady=20)

	def add_tasks(self, tasks: [Task]):
		"""
		Add tasks from list to task list
		"""
		self.clear_list()

		for task in tasks:
			self.add_task_to_table(task)

	def add_task_to_table(self, task: Task):
		"""
		This method is used to add task to view.
		"""

		task_status = tk.IntVar(value=1 if task.finished else 0)
		task_heading = task.heading

		# I don't know why i need to pass task_status in command to properly load view from file
		# it just work so future me, don't remove it

		task_frame = ttk.Frame(self.task_list_widget.scrollable_frame)
		action_frame = ttk.Frame(task_frame)
		tk.Checkbutton(
			action_frame,
			text=task_heading,
			variable=task_status,
			onvalue=1,
			offvalue=0,
			command=lambda t=task, v=task_status: self._update_task_status(t, v),
			anchor='w'
		).pack(side='left', anchor='w')

		tk.Button(action_frame, text='Details', command=lambda t=task: self.display_task_details(t)).pack(side='right')
		action_frame.pack(fill='x')

		ttk.Separator(task_frame, orient='horizontal').pack(fill='x')
		task_frame.pack(side='bottom', expand=False, fill='x')

	def _update_task_status(self, task: Task, task_status: int):
		# I don't know why i need to pass task_status in command to properly load view from file
		# it just work so future me, don't remove it

		self.controller.swap_task_status(task)

	def main(self):
		self.mainloop()

class DetailsFrame(ttk.Frame):
	def __init__(self, parent, controller, task: Task):
		super().__init__(parent)
		self.task = task
		self.controller = controller

		ttk.Label(self, text='Description:').pack(fill='x')
		self.text = tk.Text(self, height=10)
		self.text.insert(tk.END, task.description)
		self.text.pack()

		update_description_button = ttk.Button(self, text='Update description', command=self._update_description)
		update_description_button.pack(fill='x')

		ttk.Separator(self, orient='horizontal').pack(fill='x', pady=20)

		delete_task_button = ttk.Button(self, text='Delete this task', command=lambda: self.controller.delete_task(task))
		delete_task_button.pack(fill='x')

	def _update_description(self):
		description = self.text.get('1.0', tk.END)
		self.controller.update_task_description(self.task, description)

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
