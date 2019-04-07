import csv
import ZODB, ZODB.FileStorage
import BTrees.OOBTree
import transaction
import persistent
import time
import random
from ZEO.ClientStorage import ClientStorage
from ZODB import DB

server_and_port = ('127.0.0.1', 8090)
storage = ClientStorage(server_and_port)
db = DB(storage)
connection = db.open()

root = connection.root

class Movie(persistent.Persistent):
	def __init__(self,title, genres):
		self.title = title
		self.genres = genres.split("|")
		self.ratings = []
		
	def set_title(self, title):
		self.title = title	

	def set_genres(self, genres):
		self.genres = genres

	def set_ratings(self, ratings):
		self.ratings = ratings
	
	def addRating(self,r):
		self.ratings.append(r)

print("----------------------------------------------------------------------------")

def bestThriller(tree):
	bestScore = 0.0
	bestT = ""
	for i in tree.keys():
		if("Thriller" in tree[i].genres and len(tree[i].ratings) > 20):
			tmp = ave(tree[i].ratings)
			if(tmp > bestScore):
				bestScore = tmp
				bestT = tree[i].title
	print("Best -- " + bestT + " " + str(bestScore))

def randomMovies(tree):
	for i in range (0,250000):
		randomMovie = random.choice(tree.keys())
		print(str(tree[randomMovie].title))

def saveRandomData(tree):
	startIndex=150000
	for i in range(startIndex, 160000):
		movieId = str(i)
		title = "Random Title " + movieId
		genre = "Thriller|Action|Comedy|Horror"
		rating = [1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
		tree[movieId] =  Movie(title, genre)
		tree[movieId].addRating(rating)
		print(str(tree[movieId].title))
		transaction.commit()

def ave(rList):
	if(len(rList) == 0):
		return 0
	s=0.0
	for i in rList:
		s+=float(i)
	return s/len(rList)

def bestThrillerTree(tree):
	bestScore = 0.0
	bestT = ""
	for i in tree.keys():
		tmp = ave(tree[i].ratings)
		if(tmp > bestScore):
			bestScore = tmp
			bestT = tree[i].title
	print("Best -- " + bestT + " " + str(bestScore))


fi = open("20mTestTTree","w")

fi.write("TEST\n")
start = time.time()
bestThrillerTree(root.thriller)
end = time.time()
print("Time: " + str(end-start))
fi.write("Time: " + str(end-start))


fi.write("\nTEST2\n")
print("TEST2")
start = time.time()
randomMovies(root.movies)
end = time.time()
print("Time: " + str(end-start))
fi.write("Time: " + str(end-start))


fi.write("\nTEST3\n")
print("TEST3")
start = time.time()
saveRandomData(root.movies)
end = time.time()
print("Time: " + str(end-start))
fi.write("Time: " + str(end-start))


fi.close()




