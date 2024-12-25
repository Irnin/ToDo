import pickle
import time
import uuid
import os

from colorama import Fore

class Model:

	def __init__(self):
		self.tasks = []

	def add_task(self, task_description, done = False):
		heading = Task(task_description, done)
		self.tasks.append(heading)

		return heading

	def get_list(self, kind: str='All'):
		match kind:
			case 'All':
				return self.tasks
			case 'Unfinished':
				return [task for task in self.tasks if not task.finished]
			case 'Finished':
				return [task for task in self.tasks if task.finished]

		return self.tasks

	def delete_all_tasks(self):
		self.tasks.clear()

	def delete_task(self, task):
		self.tasks.remove(task)

	def get_list_size(self):
		return len(self.tasks)

	def save(self):
		directory = os.path.expanduser("~/myApp/toDo")
		os.makedirs(directory, exist_ok=True)
		file_path = os.path.join(directory, "myList.pkl")

		with open(file_path, 'wb') as file:
			pickle.dump(self, file)

	def load(self):
		directory = os.path.expanduser("~/myApp/toDo")
		os.makedirs(directory, exist_ok=True)
		file_path = os.path.join(directory, "myList.pkl")

		with open(file_path, 'rb') as file:
			loaded_model = pickle.load(file)
			self.tasks = loaded_model.tasks

	# DEBUG METHODS
	def print_task_array(self):
		for task in self.tasks:
			print(task)

class Task:
	def __init__(self, heading, done = False):
		self.uuid = uuid.uuid4()
		self.finished: bool = done
		self.heading: str = heading
		self.descriptaion: str = ""
		self.created_at: int = int(time.time())
		self.updated_at: int = -1 # -1 means that task was not updated

	def __str__(self):
		formated_updated_at = "None" if self.updated_at is None else f'{self.updated_at}'
		return f'{Fore.RESET}ID: {self.uuid}\n\tDone: {self.finished}\n\tTask: {self.heading}\n\tDescription: {self.descriptaion}\n\tCreated: {self.created_at}\n\tUpdated: {formated_updated_at}'

	def __eq__(self, other):
		if not isinstance(other, Task):
			# don't attempt to compare against unrelated types
			return NotImplemented

		return self.uuid == other.uuid

	def swap_status(self):
		self.updated_at = int(time.time())
		self.finished = not self.finished

	def update_description(self, description):
		self.descriptaion = description
