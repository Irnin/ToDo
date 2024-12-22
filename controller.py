from model import Model
from view import View

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View(self)

	def main(self):
		self.load()
		self.view.main()

	def add_task(self, task_description):
		if not task_description:
			return

		self.view.clear_input()

		task = self.model.add_task(task_description)
		self.view.add_task_to_table(task)
		self.save()

	def get_amount_of_task(self) -> int:
		return self.model.get_list_size()

	def swap_task_status(self, task):
		task.swap_task_status()
		self.save()

	def save(self):
		self.model.save()

	def load(self):
		self.model.load()

		self.view.clear_list()
		tasks = self.model.get_list()
		self.view.add_tasks(tasks)

	# DEBUG METHODS
	def print_task_array(self):
		self.model.print_task_array()

	def remove_all_task(self):
		self.model.delete_all_tasks()
		self.view.clear_list()
		self.save()

if __name__ == '__main__':
	application = Controller()
	application.main()
