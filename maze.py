import requests
import json
from collections import deque

url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"
s = "/session"
g = "/game?token="
headers = {'content-type': 'application/x-www-form-urlencoded'}
uid = "504988167"

up = "UP"
down = "DOWN"
right = "RIGHT"
left = "LEFT"

success = "SUCCESS"
end = "END"
wall = "WALL"
oob = "OUT_OF_BOUNDS"

size = "maze_size"
loc = "current_location"
status = "status"
levComplete = "levels_completed"
levTotal = "levels_total"

def getToken():
	global token
	payload = {'uid': uid}

	r = requests.post(url+s, data=payload, headers=headers)
	d = json.loads(r.content)
	token = d["token"]

def getGameData():
	global game
	r = requests.get(url+g+token)
	game = json.loads(r.content)

def move(direction):
	global result
	result = "NONE"
	payload = {'action': direction}
	r = requests.post(url+g+token, data=payload, headers=headers)
	result = json.loads(r.content)['result']

def initMaze():
	global curLoc
	global width
	global height
	global maze
	global stack
	getGameData()
	print "Working on Maze " + str(game[levComplete] + 1)
	curLoc = game[loc]
	width = game[size][0]
	height = game[size][1]
	maze = [[0 for x in range(width)] for y in range(height)]
	stack = deque()

# def printMaze():
# 	global maze
# 	for y in maze:
# 		print y
# 	print " "

def makeMove():
	global curLoc
	global width
	global height
	global maze
	global stack
	x = curLoc[0]
	y = curLoc[1]
	maze[y][x] = 1
	if(x + 1 < width and maze[y][x+1] == 0):
		move(right)
		if(result == success):
			curLoc = [x+1,y]
			stack.append(right)
		else:
			maze[y][x+1] = 2
	elif(y + 1 < height and maze[y+1][x] == 0):
		move(down)
		if(result == success):
			curLoc = [x,y+1]
			stack.append(down)
		else:
			maze[y+1][x] = 2
	elif(x - 1 >= 0 and maze[y][x-1] == 0):
		move(left)
		if(result == success):
			curLoc = [x-1,y]
			stack.append(left)
		else:
			maze[y][x-1] = 2
	elif(y - 1 >= 0 and maze[y-1][x] == 0):
		move(up)
		if(result == success):
			curLoc = [x,y-1]
			stack.append(up)
		else:
			maze[y-1][x] = 2
	else:
		undoDir = stack.pop()
		if(undoDir == up):
			move(down)
			curLoc = [x,y+1]
		elif(undoDir == down):
			move(up)
			curLoc = [x,y-1]
		elif(undoDir == left):
			move(right)
			curLoc = [x+1,y]
		elif(undoDir == right):
			move(left)
			curLoc = [x-1,y]

		if(result != success and result != end):
			print("NOOOOOOOO WE BROKE IT")
			# print result
			# print curLoc
			# getGameData()
			# print game
			# printMaze()
			quit()

getToken()
getGameData()
while(game[status] == "PLAYING"):
	initMaze()
	makeMove()
	while(result != end and result != oob):
		makeMove()
	getGameData()

getGameData()
print game[status]
