from model import Model
from view import View

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View(self)

	def main(self):
		print("Hello World!")

if __name__ == '__main__':
	application = Controller()
	application.main()