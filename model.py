import uuid
import pickle

class Model:

	def __init__(self):
		self.tasks = []

	def add_task(self, task_description, done = False):
		task = Task(task_description, done)
		self.tasks.append(task)

		return task

	def get_list(self):
		return self.tasks

	def delete_all_tasks(self):
		self.tasks.clear()

	def get_list_size(self):
		return len(self.tasks)

	def save(self):

		with open('myList.pkl', 'wb') as file:
			pickle.dump(self, file)

	def load(self):
		with open('myList.pkl', 'rb') as file:
			loaded_model = pickle.load(file)
			self.tasks = loaded_model.tasks

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

