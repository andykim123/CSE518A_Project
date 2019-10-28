#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 17:48:08 2019

@author: dohoonkim
"""
import csv

class Comment:
	def __init__(self, content, timestamp = "000000"):
		self.content = content
		self.timestamp = timestamp
        
# class about a single user
class User:
	def __init__(self, inputName, inputComments = []):
		self.name = inputName
		self.comments = inputComments

	# add comments in a proper way
	# with regards to the class of inputComments
	def addComments(self, inputComments):
		if(isinstance(inputComments, list)):
			self.__addComments(inputComments)
		else:
			self.__addComment(inputComments)

	def __addComment(self, inputComment):
		self.comments.append(inputComment)

	def __addComments(self, inputComments):
		self.comments.extend(inputComments)
        
# class which includes the dictionary of users with comments.
# used in chatbot directly.
class UserDictionary:

	def __init__(self):
		self.userDict = dict()

	def addComment(self, user, content, timestamp = 0):
		self.__addCommentToUserDict(user, Comment(content = content, timestamp = timestamp))

	def __addCommentToUserDict(self, user, comment):
		if(self.userDict.get(user)==None):
			self.userDict[user] = User(inputName = user, inputComments = [comment])
		else:
			self.userDict[user].addComments(comment)
            
class UserFactory:

	# public function that will be used to get dictionary of users
	def getUsersFromFile(self, fileName):
		return self.__buildUserDicts(self.__getRawComments(fileName))

	# private function to build user dictionary
	# out of list of tuples, (username, comment)
	def __buildUserDicts(self, inputList):
		userDict = dict()
		for comment in inputList:
			if(userDict.get(comment[0])==None):
				userDict[comment[0]] = User(inputName = comment[0], inputComments = [comment[1]])
			else:
				userDict[comment[0]].addComments(Comment(content = comment[1].content))
		return userDict


	# private function to build list of tuples, (username, comment)
	# from the given csv file path, if the path is a proper one.
	def __getRawComments(self, fileName):
		sentences = list()
		try:
#			file = open(fileName, 'rb') # Python 2 version
			file = open(fileName, 'r') # Python 3 version
			with file as csvfile:
				reader = csv.reader(csvfile, delimiter="\n") # read per line
				for row in reader:
					if(len(row)!=1): # only one full comment per line in csv file --> may change later on.
						raise ValueError('input csv file is not formatted correctly')
					line = row[0].split("\t")
					comment = (line[0], Comment(content = line[1]))
					sentences.append(comment)
			file.close()
		except FileNotFoundError: # in python3, use FileNotFoundError
			print(fileName + " does not exist.")
		return sentences