import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import time
import random

engine = create_engine('mysql+pymysql://root:haslo@localhost/filmy_oceny')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Movie(Base):
	__tablename__ = 'movies'
	movieId = Column(Integer, primary_key=True)
	title = Column(String(255))
	genres = Column(String(255))
	rel = relationship("Rating")
	def __repr__(self):
		return "<Movie(movieId='%i', title='%s', genres='%s')>" % (self.movieId, self.title, self.genres)

class Rating(Base):
	__tablename__ = 'ratings'
	rating = Column(String(255))
	movieId = Column(Integer, ForeignKey('movies.movieId'),primary_key = True)
	def __repr__(self):
		return "<Rating(rating='%i', movieId='%i')>" % (self.rating, self.movieId)

def bestThriller():
	result = session.execute('SELECT title, AVG(ratings.rating) as average, COUNT(ratings.rating) as numb FROM (SELECT * FROM movies where genres like "%Thriller%") as tharray JOIN ratings on ratings.movieId = tharray.movieId  group by title having numb > 20 order by average desc limit 1;').fetchall()
	print("Best -- " + str(result[0][0]) + " " + str(result[0][1]))

def random1Mmovies(m, movieList = []):
	if(m==1):
		idList = movieList
		#1
		for i in range (0,250000):
			randomMovie = random.choice(idList)
			resultsql2 = session.execute('SELECT title from movies where movieId = :randomMovie;',{'randomMovie':randomMovie}).fetchone()
			print(str(resultsql2[0]))
	if(m==2):
		#2
		for i in range (0,100):
			resultsql = session.execute('SELECT movieId from movies;')
			idList = []
			for i in resultsql:
				idList.append(i[0])
			randomMovie = random.choice(idList)
			resultsql2 = session.execute('SELECT  title  from movies where movieId = :randomMovie;',{'randomMovie':randomMovie}).fetchone()
			print(str(resultsql2[0]))
	if(m==3):
		#3
		for i in range(0,25000):
			resultsql = session.execute('SELECT title from movies order by Rand() limit 1;').fetchone()
			print(str(resultsql[0]))

def saveRandomData():
	startIndex=150000
	for i in range(startIndex, 160000):
		sqlAdd = session.execute('INSERT INTO movies(movieId,title,genres) VALUES(:movieId,:title,:genres);',{'movieId':i,'title':"Random Title " +str(i),'genres':"Thriller|Action|Comedy|Horror"})
		for j in range(0,3):
			for k in range(1,6):
				sqlAddRating = session.execute('INSERT INTO ratings(movieId,rating) VALUES(:movieId,:rating);',{'movieId':i,'rating':k})
		session.commit()
		sqltitle = session.execute('SELECT title from movies where movieId = :id;',{'id':i}).fetchone()
		print(str(sqltitle[0]))




resultList = session.execute('SELECT movieId from movies')
movieList = []
for i in resultList:
	movieList.append(i[0])
print(movieList)



fi = open("5mTestSQL","w")

print("TEST")
fi.write("TEST\n")

start = time.time()
bestThriller()
end = time.time()
print("Time: " + str(end-start))
fi.write("Time: " + str(end-start))


fi.write("\nTEST2A\n")
print("TEST2A")
start = time.time()
random1Mmovies(1,movieList)
end = time.time()
print("Time: " + str(end-start))
fi.write("Time: " + str(end-start))


fi.write("\nTEST2C\n")
print("TEST2C")
start = time.time()
random1Mmovies(3)
end = time.time()
print("Time: " + str(end-start))
fi.write("Time: " + str(end-start))




fi.write("\nTEST3\n")
print("TEST3")
start = time.time()
saveRandomData()
end = time.time()
print("Time: " + str(end-start))
fi.write("Time: " + str(end-start))


fi.close()






'''
newMovie = Movie(movieId=i, title = "Random Title " + str(i), genres = "Thriller|Action|Comedy|Horror")
session.add(newMovie)
for j in range(0,3):
for k in range(1,6):
session.add(Rating(rating = k, movieId = i))
session.commit()
print(str(session.query(Movie).filter_by(movieId=i).first()))
'''













