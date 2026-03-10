class Person:
	def __init__(self, firstName, lastName, idNumber):
		self.firstName = firstName
		self.lastName = lastName
		self.idNumber = idNumber
	def printPerson(self):
		print("Name:", self.lastName + ",", self.firstName)
		print("ID:", self.idNumber)

class Student(Person):
	#class Constructor
	def __init__(self, firstName, lastName, idNumber, scores):
		super().__init__(firstName, lastName, idNumber)
		self.scores = scores
	def calculate(self):
		promedio = sum(self.scores) / len(self.scores)
		#return promedio
		if promedio >= 90 and promedio <= 100:
			return 'O'
		elif promedio >= 80 and promedio < 90:
			return 'E'
		elif promedio >= 70 and promedio < 80:
			return 'A'
		elif promedio >= 55 and promedio < 70:
			return 'P'
		elif promedio >= 40 and promedio < 55:
			return 'D'
		else:
			return 'T'         
	
line = input().split()
firstName = line[0]
lastName = line[1]
idNum = line[2]
numScores = int(input()) # not needed for Python
scores = list( map(int, input().split()) )
s = Student(firstName, lastName, idNum, scores)
s.printPerson()
print("Grade:", s.calculate())