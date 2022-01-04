from tkinter import *
from PIL import Image, ImageTk
import random


MOVE_INCREMENT = 20
MOVE_PER_SEC = 9
GAME_SPEED = 1000 // MOVE_PER_SEC


class Snake(Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background='black', highlightthickness=0)

        self.reset = [(100, 100), (80, 100), (60, 100)]
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]  # Positionsแรกของงู หัวคือ(100,100)
        self.food_positions = self.set_new_food_positions()  # Positionsแรกของอาหาร
        self.score = 0  # คะแนน
        self.loop = None
        self.direction = 'Right'

        self.bind_all('<Key>', self.on_key_press)
        self.bind('<F1>', self.rungame)

        self.load_assets()
        self.create_objects()
        self.rungame()
        self.start = True

    def load_assets(self):
        self.snake_body_image = Image.open('./assets/Body.png')  # โหลดรูปตัวงู
        self.snake_body = ImageTk.PhotoImage(self.snake_body_image)  # เอาลงในtk

        self.food_image = Image.open('./assets/Food.png')  # โหลดรูปตัวอาหาร
        self.food = ImageTk.PhotoImage(self.food_image)  # เอาลงในtk

    def create_objects(self):
        # สร้างคะแนน
        FONT = ("Bebas Neue", 14)
        self.create_text(45, 12, text='Score: {}'.format(self.score), tag='score', fill='red', font=FONT)
        # สร้างงู
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag='snake')
        # สร้างอาหาร
        self.create_image(self.food_positions[0], self.food_positions[1], image=self.food, tag='food')
        self.create_rectangle(7, 27, 593, 613, outline='#FFF')

    def move_snake(self):
        head_x, head_y = self.snake_positions[0]
        if self.direction == 'Right':
            new_head_position = (head_x + MOVE_INCREMENT, head_y)
        elif self.direction == 'Left':
            new_head_position = (head_x - MOVE_INCREMENT, head_y)
        elif self.direction == 'Up':
            new_head_position = (head_x, head_y - MOVE_INCREMENT)
        elif self.direction == 'Down':
            new_head_position = (head_x, head_y + MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        findsnake = self.find_withtag('snake')  # หาposition เก่า
        for segment, position in zip(findsnake, self.snake_positions):
            self.coords(segment, position)

    def rungame(self):
        if self.check_collisions() and self.start==True:
            self.after_cancel(self.loop)
            self.start = False
            self.delete('all')
            self.create_text(300, 300, justify=CENTER,
                             text=f'GAME OVER\n\nSCORE: {self.score}\n\nNEW GAME PRESS <F1>', fill='white', font=("Sukhumvit Set Text", 30))
        elif self.check_collisions() and self.start == False:
            self.delete('all')
            self.snake_positions = self.reset
            self.food_positions = self.set_new_food_positions()
            self.create_objects()
            self.start = True
            self.direction = 'Right'
            self.score = 0
            self.loop = self.after(GAME_SPEED, self.rungame)
        else:
            self.food_collisions()
            self.move_snake()
            self.loop = self.after(GAME_SPEED, self.rungame)  # loopให้เดินตลอด

    def on_key_press(self, e):
        new_direction = e.keysym  # ดูว่าเรากดปุ่มอะไร
        all_direction = ('Up', 'Down', 'Left', 'Right')
        opposites = ({'Up', 'Down'}, {'Left', 'Right'})
        if new_direction in all_direction and {new_direction,self.direction} not in opposites:
            self.direction = new_direction
        elif new_direction == 'F1':
            self.rungame()
        print('KEY:', self.direction)

    def check_collisions(self):
        head_x, head_y = self.snake_positions[0]
        return (head_x in (0,600) or head_y in (20, 620) or (head_x, head_y) in self.snake_positions[1:])

    def food_collisions(self):
        if self.snake_positions[0] == self.food_positions:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag='snake')
            score = self.find_withtag('score')
            self.itemconfigure(score, text='Score: {}'.format(self.score),tag='score')
            self.food_positions = self.set_new_food_positions()
            self.coords(self.find_withtag('food'), self.food_positions)

    def set_new_food_positions(self):
        while True:
            x_position = random.randint(1, 29) * MOVE_INCREMENT
            y_position = random.randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)
            if food_position not in self.snake_positions:
                return food_position


GUI = Tk()
GUI.title('SNAKE GAME 101')
GUI.resizable(False, False)

game = Snake()
game.pack()

GUI.mainloop()
