class student:
    def __init__(self, first_name, last_name, age, GPA):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.GPA = GPA

    def display(self):
        print("hello my name is " + self.first_name + " " +  str(self.last_name) + " and my GPA is " + str(self.GPA))

def main():
    Student_luke = student("Luke", "Frey", 24, 3.97)
    Student_luke.display()





if __name__=="__main__":
    main()
