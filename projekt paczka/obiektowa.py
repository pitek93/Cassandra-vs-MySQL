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
root.movies = BTrees.OOBTree.BTree()

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

with open('movies.csv', 'rt') as filmy:
	wszystkieFilmy = csv.reader(filmy)
	for row1 in wszystkieFilmy:
		movieId = row1[0]
		#print(movieId)
		title = row1[1]
		genre = row1[2]

		root.movies[movieId] =  Movie(title, genre)
        	#print (row1)

with open('ratings_pierwsze20m.csv', 'rt') as oceny:
	wszystkieOceny = csv.reader(oceny, delimiter=',', quotechar='|')
	i=0
	for row2 in wszystkieOceny:
		i=i+1
		print(i)
		movieId = row2[1]
		rating = row2[2]
		root.movies[movieId].addRating(rating)

print("----------------------------------------------------------------------------")

root.thriller = BTrees.OOBTree.BTree()

for i in root.movies.keys():
	if("Thriller" in root.movies[i].genres and len(root.movies[i].ratings) > 20):
		root.thriller[i] = Movie(root.movies[i].title,"1|2")
		root.thriller[i].set_genres(root.movies[i].genres)
		for r in root.movies[i].ratings:
			root.thriller[i].addRating(r)

for i in root.thriller.keys():
	print(root.thriller[i].title)

transaction.commit()



