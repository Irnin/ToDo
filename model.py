import pickle
import time
import uuid
import os

from colorama import Fore

class Model:

	def __init__(self):
		self.tasks = []

		directory = os.path.expanduser("~/myApp/toDo")
		os.makedirs(directory, exist_ok=True)
		self.save_file_path = os.path.join(directory, "myList.pkl")

	def add_task(self, task_description, done = False):
		"""
		Add task to tasks array
		"""
		task = Task(task_description, done)
		self.tasks.append(task)

		return task

	def get_list(self, kind: str='All'):
		"""
		 This method returns array of task depending on kind parameter:
		 - All - returns all tasks
		 - Unfinished - returns only tasks with finished property set to False
		 - Finished - returns only tasks with finished property set to True
		"""

		match kind:
			case 'All':
				return self.tasks
			case 'Unfinished':
				return [task for task in self.tasks if not task.finished]
			case 'Finished':
				return [task for task in self.tasks if task.finished]

		return self.tasks

	def delete_all_tasks(self):
		"""
		Clear array of tasks
		"""
		self.tasks.clear()

	def delete_task(self, task):
		"""
		Remove task sent as parameter from array
		"""
		self.tasks.remove(task)

	def get_list_size(self) -> int:
		"""
		Returns size of list
		"""
		return len(self.tasks)

	def save(self):
		"""
		Save data from model to file
		"""
		with open(self.save_file_path, 'wb') as file:
			pickle.dump(self, file)

	def load(self):
		"""
		Load model data from file
		"""
		with open(self.save_file_path, 'rb') as file:
			loaded_model = pickle.load(file)
			self.tasks = loaded_model.tasks

	# DEBUG METHODS
	def print_task_array(self):
		for task in self.tasks:
			print(task)

class Task:
	def __init__(self, heading, finished = False):
		self.uuid = uuid.uuid4()
		self.finished: bool = finished
		self.heading: str = heading
		self.description: str = ""
		self.created_at: int = int(time.time())
		self.updated_at: int = -1 # -1 means that task was not updated

	def __str__(self):
		formated_updated_at = "None" if self.updated_at is None else f'{self.updated_at}'
		return f'{Fore.RESET}ID: {self.uuid}\n\tDone: {self.finished}\n\tTask: {self.heading}\n\tDescription: {self.description}\n\tCreated: {self.created_at}\n\tUpdated: {formated_updated_at}'

	def __eq__(self, other):
		if not isinstance(other, Task):
			# don't attempt to compare against unrelated types
			return NotImplemented

		return self.uuid == other.uuid

	def swap_status(self):
		self.updated_at = int(time.time())
		self.finished = not self.finished

	def update_description(self, description):
		self.description = description
