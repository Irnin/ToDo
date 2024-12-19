class Model:

	def __init__(self):
		self.tasks = []

	def add_task(self, task, done = False):
		task = Task(task, done)

		self.tasks.append(task)
		print(task)

class Task:
	def __init__(self, task, done = False):
		self.task = task
		self.done = done

	def __str__(self):
		return f'Task: {self.task}, Done: {self.done}'

