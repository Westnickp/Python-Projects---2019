from tkinter import *
import random
import time
import numpy as np

# root = Tk()
# root.title('Pong!')
# root.resizable(0,0)
# root.wm_attributes('-topmost', 1)
# canvas = Canvas(root, width=500, height=400, bd = 0, highlightthickness=0)
# canvas.config(bg='black')
# canvas.pack()
# root.update()
#
# canvas.create_line(250,0, 250, 400, fill='white')

class Board(object):
    def __init__(self, title, width, height, background):
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(0,0)
        self.root.wm_attributes('-topmost', 1)
        self.canvas = Canvas(self.root, width=width, height=height, bd=0, highlightthickness=1)
        self.canvas.config(bg=background)
        self.canvas.pack()
        self.root.update()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.create_line(self.canvas_width/2,0,self.canvas_width/2,self.canvas_height,fill='white')

    def xcollision(self, object1, object2):
        pos1 = self.canvas.coords(object1.id)
        pos2 = self.canvas.coords(object2.id)
        mid1 = [(pos1[0]+pos1[2])/2, (pos1[1]+pos1[3])/2]
        mid2 = [(pos2[0]+pos2[2])/2, (pos2[1]+pos2[3])/2]
        if pos2[1] <= pos1[3] and pos2[3] >= pos1[1]:
            if mid1[0] >= pos2[2] and object1.x < object2.x:
                if pos1[0] <= pos2[2]:
                    object1.x *= -1
            elif mid1[0] <= pos2[0] and object1.x > object2.x:
                if pos1[2] >= pos2[0]:
                    object1.x *= -1


class Ball(object):
    def __init__(self, board, color):
        self.counter = 0
        self.board = board
        self.canvas = board.canvas
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.id = self.canvas.create_oval(0,0,15,15,fill=color)
        self.canvas.move(self.id, self.canvas_width/2-7.5, self.canvas_height/2-7.5)
        self.y = random.choice([np.random.uniform(-2,-1.6),np.random.uniform(1.6,2)])
        self.x = random.choice([np.random.uniform(-2,-1),np.random.uniform(1,2)])


    def draw(self):
        # print(self.counter)
        self.counter += 1
        if self.counter > 100:
            self.canvas.move(self.id, self.x, self.y)
            pos = self.canvas.coords(self.id) ## [x1, y1, x2, y2]
            if pos[1] <= 0:
                self.y = -self.y
            if pos[3] >= self.canvas_height:
                self.y = -self.y
            if pos[0] <= 0:
                self.respawn()
            if pos[2] >= self.canvas_width:
                self.respawn()

    def respawn(self):
        pos = self.canvas.coords(self.id)
        width = pos[2] - pos[0]
        height = pos[3] - pos[1]
        deltax = (self.canvas_width-width)/2 - pos[0]
        deltay = (self.canvas_height-height)/2 - pos[1]
        self.canvas.move(self.id, deltax, deltay)
        self.counter = 0
        self.y = random.choice([np.random.uniform(-3,-2),np.random.uniform(2,3)])
        self.x = random.choice([np.random.uniform(-2,-1),np.random.uniform(1,2)])


class Paddle(object):
    def __init__(self, board, ball, color, side='left', mode='computer'):
        self.board = board
        self.canvas = board.canvas
        self.ball = ball
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.side = side
        self.mode = mode
        self.x = 0
        self.y = 0
        if self.side == 'left':
            self.id = self.canvas.create_rectangle(0,0,10,self.canvas_height/5, fill=color)
            self.canvas.move(self.id, 5,self.canvas_height*2/5)
            if self.mode != 'computer':
                self.board.root.bind('w', self.move_up)
                self.board.root.bind('s', self.move_down)
        if self.side == 'right':
            self.id = self.canvas.create_rectangle(0,0,10,self.canvas_height/5, fill=color)
            self.canvas.move(self.id, self.canvas_width-15,self.canvas_height*2/5)
            if self.mode != 'computer':
                self.board.root.bind('<KeyPress-Up>', self.move_up)
                self.board.root.bind('<KeyPress-Down>', self.move_down)

    def draw(self):
        if self.mode == 'computer':
            paddlepos = self.canvas.coords(self.id)
            ballpos = self.canvas.coords(ball.id)
            padmid = (paddlepos[1] + paddlepos[3])/2
            ballmid = (ballpos[1] + ballpos[3])/2
            if padmid <= ballmid:
                self.y = 1.5
                if paddlepos[3] >= self.canvas_height:
                    self.y = 0
            elif padmid >= ballmid:
                self.y = -1.5
                if paddlepos[1] <= 0:
                    self.y = 0
            self.canvas.move(self.id, self.x, self.y)
            if self.ball.counter >= 1000 and self.side == 'left':
                self.x = 0.1
            if self.ball.counter >= 1000 and self.side == 'right':
                self.x = -0.1
            if self.ball.counter == 0 and self.side == 'right':
                self.x = 0
                self.canvas.move(self.id, -paddlepos[0], 0)
                self.canvas.move(self.id, self.canvas_width-15, 0)
            if self.ball.counter == 0 and self.side == 'left':
                self.x = 0
                self.canvas.move(self.id, -paddlepos[0], 0)
                self.canvas.move(self.id, 5, 0)
        else:
            paddlepos = self.canvas.coords(self.id)
            if self.y < 0 and paddlepos[1] <= 0:
                self.y = 0
            if self.y > 0 and paddlepos[3] >= self.canvas_height:
                self.y= 0
            self.canvas.move(self.id, self.x, self.y)
            if self.ball.counter >= 1000 and self.side == 'left':
                self.x = 0.1
            if self.ball.counter >= 1000 and self.side == 'right':
                self.x = -0.1
            if self.ball.counter == 0 and self.side == 'right':
                self.x = 0
                self.canvas.move(self.id, -paddlepos[0], 0)
                self.canvas.move(self.id, self.canvas_width-15, 0)
            if self.ball.counter == 0 and self.side == 'left':
                self.x = 0
                self.canvas.move(self.id, -paddlepos[0], 0)
                self.canvas.move(self.id, 5, 0)

    def move_up(self, event):
        if self.mode == 'computer':
            pass
        else:
            self.y = -1


    def move_down(self, event):
        if self.mode == 'computer':
            pass
        else:
            self.y = 1


board = Board('Pong!', 700, 400, 'black')
ball = Ball(board, 'orange')
paddle1 = Paddle(board, ball, 'grey')
paddle2 = Paddle(board, ball, 'grey', side='right', mode='man')
while True:
    ball.draw()
    paddle1.draw()
    paddle2.draw()
    board.xcollision(ball, paddle1)
    board.xcollision(ball, paddle2)
    board.root.update_idletasks()
    board.root.update()
    # time.sleep(0.01)
