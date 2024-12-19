from model import Model
from view import View

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View(self)

	def main(self):
		self.view.main()

	def add_task(self, task_description):
		self.model.add_task(task_description)
		self.view.add_task_to_table(task_description, False)

if __name__ == '__main__':
	application = Controller()
	application.main()
