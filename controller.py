from model import Model
from view import View

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View(self)

	def main(self):
		self.view.main()

	def add_task(self, task_description):
		task = self.model.add_task(task_description)
		self.view.add_task_to_table(task)

	def swap_task_status(self, task):
		task.swap_task_status()

	# DEBUG METHODS
	def print_task_array(self):
		self.model.print_task_array()

if __name__ == '__main__':
	application = Controller()
	application.main()
