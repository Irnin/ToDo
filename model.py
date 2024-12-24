import pickle
import time

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
		for task in self.tasks:
			print(task)

class Task:
	def __init__(self, heading, done = False):
		self.finished: bool = done
		self.heading: str = heading
		self.descriptaion: str = ""
		self.created_at: int = int(time.time())
		self.updated_at: int = -1 # -1 means that task was not updated

	def __str__(self):
		formated_updated_at = "None" if self.updated_at is None else f'{self.updated_at}'
		return f'{Fore.RESET}Done: {self.finished}\t\tTask: {self.heading}\t\tDescription: {self.descriptaion}\t\tCreated: {self.created_at}\t\tUpdated: {formated_updated_at}'

	def swap_status(self):
		self.updated_at = int(time.time())
		self.finished = not self.finished

	def update_description(self, description):
		self.descriptaion = description
