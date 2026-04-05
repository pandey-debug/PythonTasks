#16. Library Management System (Constructor & Inheritance)
#A library stores information about books and digital books. Create a base class Book
#with a constructor to initialize book details. Create a derived class EBook that adds file
#size information.

class Books():
    def __init__(self,author,pages):
      self.pages= pages
      self.author= author
        

class Ebook(Books):
    def __init__(self,author,pages,filesize):
         super().__init__(author,pages)
         self.filesize=filesize
    def details(self):
        print("author of books",self.author)
        print("pages of books",self.pages)
        print("Size of file",self.filesize,"MB")

book_1=Ebook("tarun",200,3)
book_1.details()

