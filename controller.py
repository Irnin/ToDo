from model import Model, Task
from view import View

from colorama import Fore

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View(self)

	def main(self):
		self.load()
		self.view.main()

	def add_task(self, task_heading):
		"""
		Add task to model and view
		"""

		if not task_heading:
			return

		task = self.model.add_task(task_heading)
		Controller.print_debug(f'Adding new task to list:\n{task}')

		self.view.clear_input()
		self.view.add_task_to_table(task)
		self.save()

	def delete_task(self, task: Task):
		Controller.print_debug("Deleting task")
		self.model.delete_task(task)

		tasks = self.model.get_list()
		self.view.clear_list()
		self.view.add_tasks(tasks)

	def get_amount_of_task(self) -> int:
		return self.model.get_list_size()

	def swap_task_status(self, task):
		task.swap_status()
		Controller.print_debug(f'Updated task status:\n{task}')
		self.save()

	def update_task_description(self, task: Task, description: str):
		task.update_description(description)
		Controller.print_debug(f'Updated task:')
		print(task)
		self.save()

	def display_tasks(self, kind: str):
		"""
		Method is used to display tasks in view
		"""
		tasks = self.model.get_list(kind)
		self.view.add_tasks(tasks)

	def save(self):
		Controller.print_debug("Saving tasks")
		self.model.save()

	def load(self):
		try:
			self.model.load()
		except Exception:
			Controller.print_error('Was not able to read data from file myList.pkl')

		self.view.clear_list()
		tasks = self.model.get_list()
		self.view.add_tasks(tasks)

	# DEBUG METHODS
	@staticmethod
	def print_debug(text):
		print(Fore.YELLOW + 'DEBUG: ' + Fore.RESET + text)

	@staticmethod
	def print_error(text):
		print(Fore.RED + 'ERROR: ' + Fore.RESET + text)

	def print_task_array(self):
		Controller.print_debug("Tasks array:")
		self.model.print_task_array()

	def remove_all_task(self):
		self.model.delete_all_tasks()
		self.view.clear_list()
		self.save()

if __name__ == '__main__':
	application = Controller()
	application.main()
