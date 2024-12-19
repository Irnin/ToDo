import uuid

class Model:

	def __init__(self):
		self.tasks = []

	def add_task(self, task_description, done = False):
		task = Task(task_description, done)
		self.tasks.append(task)

		return task

	# DEBUG METHODS
	def print_task_array(self):
		print("Task array:")
		for task in self.tasks:
			print(task)

class Task:
	def __init__(self, task_description, done = False):
		self.id = uuid.uuid4()
		self.task_description = task_description
		self.done = done

	def __str__(self):
		return f'Done: {self.done}\t\tTask: {self.task_description}'

	def swap_task_status(self):
		self.done = not self.done

