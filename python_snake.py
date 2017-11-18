import random
import string
from Tkinter import *

# Specify the snake & the characters it uses
HEAD_CHAR = "O"
FOOD_CHARS = string.ascii_letters

# Application
class Application:
  # Basic setup variables
  TITLE = "Snake"
  SIZE = 300, 300

  def __init__(self, master):
    # Initializing the variables
    self.master = master
    self.head = None
    self.head_position = None
    self.segments = []
    self.segments_positions = []
    self.food = None
    self.food_position = None
    self.direction = None
    self.moved = True
    self.running = False

    # Run the init function
    self.init()

  def init(self):
    self.master.title(self.TITLE)

    # Creating the canvas
    self.canvas = Canvas(self.master)
    self.canvas.grid(sticky=NSEW)

    # Creating the start button
    self.start_button = Button(self.master, text="Start", command=self.on_start)
    self.start_button.grid(sticky=EW)

    # Bind the movements keys to the canvas
    self.master.bind("w", self.on_up)
    self.master.bind("a", self.on_left)
    self.master.bind("s", self.on_down)
    self.master.bind("d", self.on_right)

    # Configure the size of the canvas
    self.master.columnconfigure(0, weight=1)
    self.master.rowconfigure(0, weight=1)
    self.master.resizable(width=False, height=False)
    self.master.geometry("%dx%d" % self.SIZE)

  # When start button is clicked
  def on_start(self):
    # Reset Everything
    self.reset()
    # Check if the game is already running
    if self.running:
      self.running = False
      # Changing the text displayed on the button
      self.start_button.configure(text="Start")
    else:
      self.running = True
      # Changing the text displayed on the button
      self.start_button.configure(text="Stop")
      # Starting the game
      self.start()

  # Reset function for the game
  def reset(self):
    # Delete all the snake's body
    del self.segments[:]
    del self.segments_positions[:]
    self.canvas.delete(ALL)

  # Start function for the game
  def start(self):
    # Taking in the info of the canvas (width & height)
    width = self.canvas.winfo_width()
    height = self.canvas.winfo_height()

    # Draw the game screen
    self.canvas.create_rectangle(10, 10, width - 10, height - 10)
    self.direction = random.choice('wasd')
    head_position = [round(width / 2, -1), round(height / 2, -1)]
    self.head = self.canvas.create_text(tuple(head_position), text=HEAD_CHAR)
    self.head_position = head_position

    # Calling the functions to start the game - spawning food & updating
    self.spawn_food()
    self.tick()

  # Function for spawning the food
  def spawn_food(self):
    # get the width & height of canvas
    width = self.canvas.winfo_width()
    height = self.canvas.winfo_height()

    # check if the food is spawned on the snake's body
    positions = [tuple(self.head_position), self.food_position] + self.segments_positions
    position = round(random.randint(20, width - 20), -1), round(random.randint(20, height - 20), -1)

    # if the newly generated food is overlapping, generate until it is not
    while position in positions:
      position = round(random.randint(20, width - 20), -1), round(random.randint(20, height - 20), -1)

    # pick a random character to be generated
    character = random.choice(FOOD_CHARS)
    self.food = self.canvas.create_text(position, text=character)

    # store the previously generated character
    self.food_position = position
    self.food_character = character

  # When the timer ticks (updating the game)
  def tick(self):
    # get the canvas' width & height
    width = self.canvas.winfo_width()
    height = self.canvas.winfo_height()
    previous_head_position = tuple(self.head_position)

    # move the snake
    if self.direction == "w":
      self.head_position[1] -= 10
    elif self.direction == "a":
      self.head_position[0] -= 10
    elif self.direction == "s":
      self.head_position[1] += 10
    elif self.direction == "d":
      self.head_position[0] += 10

    # check if the game is over
    head_position = tuple(self.head_position)
    if(head_position[0] < 10 or head_position[0] >= width - 10 or head_position[1] < 10 or head_position[1] >= height - 10 or any(segments_position == head_position for segments_position in self.segments_positions)):
      self.game_over()
      return

    # Check if snake eats the food
    if head_position == self.food_position:
      self.canvas.coords(self.food, previous_head_position)
      self.segments.append(self.food)
      self.segments_positions.append(previous_head_position)
      self.spawn_food()

    # Make the food following the snake's head
    if self.segments:
      previous_position = previous_head_position
      for index, (segment, position) in enumerate(zip(self.segments, self.segments_positions)):
        self.canvas.coords(segment, previous_position)
        self.segments_positions[index] = previous_position
        previous_position = position

    # Put the new head's position into head_position
    self.canvas.coords(self.head, head_position)
    self.moved = True

    # change level (level up according to length of snake)
    speed = 100

    if len(self.segments) > 5:
      speed = 75

    if len(self.segments) > 10:
      speed = 60

    if len(self.segments) > 20:
      speed = 45

    # Call the tick function to update again after a certain time
    if self.running:
      self.canvas.after(speed, self.tick)

    display_speed = 10000 / speed
    self.start_button.configure(text = "Speed: %d" %display_speed)

  # Function for game over screen
  def game_over(self):
    # get tbe canvas' width & height
    width = self.canvas.winfo_width()
    height = self.canvas.winfo_height()

    # stop the game from running
    self.running = False

    # change the button's text to "start"
    self.start_button.configure(text="Start")

    # display the game over message & show the score
    score = len(self.segments) * 10
    self.canvas.create_text(round(width/2), round(height/2), text="Game Over! Your score is: %d" %score)

  # Function for 4 inputs
  def on_up(self, event):
    if self.moved and not self.direction == "s":
      self.direction = "w"
      self.moved = False

  def on_down(self,event):
    if self.moved and not self.direction == "w":
      self.direction = "s"
      self.moved = False

  def on_left(self, event):
    if self.moved and not self.direction == "d":
      self.direction = "a"
      self.moved = False

  def on_right(self, event):
    if self.moved and not self.direction == "a":
      self.direction = "d"
      self.moved = False

# Declaring the main loop (outside of any classes)
def main():
  root = Tk()
  Application(root)
  root.mainloop()

# Running the app
if __name__ == "__main__":
  main()










