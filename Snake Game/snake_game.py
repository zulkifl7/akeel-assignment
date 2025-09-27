import turtle
import random
import time

class SnakeGame:
    def __init__(self):
        # Game setup
        self.screen = turtle.Screen()
        self.screen.title("Snake Game")
        self.screen.bgcolor("black")
        self.screen.setup(width=800, height=600)
        self.screen.tracer(0)
        
        # Game variables
        self.score = 0
        self.level = 1
        self.game_over = False
        self.delay = 0.1
        
        # Snake setup
        self.snake_head = turtle.Turtle()
        self.snake_head.speed(0)
        self.snake_head.shape("square")
        self.snake_head.color("white")
        self.snake_head.penup()
        self.snake_head.goto(0, 0)
        self.snake_head.direction = "stop"
        
        self.snake_body = []
        
        # Food setup
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("green")
        self.food.penup()
        self.place_food()
        
        # Red food setup (Level 4)
        self.red_food = turtle.Turtle()
        self.red_food.speed(0)
        self.red_food.shape("circle")
        self.red_food.color("darkred")
        self.red_food.penup()
        self.red_food.hideturtle()
        self.red_food_active = False
        self.red_food_timer = 0
        self.red_food_timeout = 3  # 3 seconds for red food
        
        # Score display
        self.score_display = turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-390, 260)
        self.update_score_display()
        
        # Level 2 barrier (digit)
        self.barrier = turtle.Turtle()
        self.barrier.speed(0)
        self.barrier.color("yellow")
        self.barrier.penup()
        self.barrier.hideturtle()
        self.barrier_active = False
        
        # Level 3 timer variables
        self.food_timer = 0
        self.food_timeout = 5  # 5 seconds
        self.timer_display = turtle.Turtle()
        self.timer_display.speed(0)
        self.timer_display.color("cyan")
        self.timer_display.penup()
        self.timer_display.hideturtle()
        self.timer_display.goto(300, 260)
        
        # Game over display
        self.game_over_display = turtle.Turtle()
        self.game_over_display.speed(0)
        self.game_over_display.color("red")
        self.game_over_display.penup()
        self.game_over_display.hideturtle()
        
        # Keyboard bindings
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "Up")
        self.screen.onkeypress(self.go_down, "Down")
        self.screen.onkeypress(self.go_left, "Left")
        self.screen.onkeypress(self.go_right, "Right")
        
    def go_up(self):
        if self.snake_head.direction != "down":
            self.snake_head.direction = "up"
    
    def go_down(self):
        if self.snake_head.direction != "up":
            self.snake_head.direction = "down"
    
    def go_left(self):
        if self.snake_head.direction != "right":
            self.snake_head.direction = "left"
    
    def go_right(self):
        if self.snake_head.direction != "left":
            self.snake_head.direction = "right"
    
    def move_snake(self):
        if self.snake_head.direction == "up":
            y = self.snake_head.ycor()
            self.snake_head.sety(y + 20)
        
        if self.snake_head.direction == "down":
            y = self.snake_head.ycor()
            self.snake_head.sety(y - 20)
        
        if self.snake_head.direction == "left":
            x = self.snake_head.xcor()
            self.snake_head.setx(x - 20)
        
        if self.snake_head.direction == "right":
            x = self.snake_head.xcor()
            self.snake_head.setx(x + 20)
    
    def check_screen_wrap(self):
        # Screen wrap-around (no walls)
        if self.snake_head.xcor() > 390:
            self.snake_head.setx(-390)
        
        if self.snake_head.xcor() < -390:
            self.snake_head.setx(390)
        
        if self.snake_head.ycor() > 290:
            self.snake_head.sety(-290)
        
        if self.snake_head.ycor() < -290:
            self.snake_head.sety(290)
    
    def place_food(self):
        x = random.randint(-19, 19) * 20
        y = random.randint(-14, 14) * 20
        
        # Level 2: Ensure food doesn't spawn too close to barrier
        if self.level >= 2 and self.barrier_active:
            barrier_x = self.barrier.xcor()
            barrier_y = self.barrier.ycor()
            while abs(x - barrier_x) < 60 and abs(y - barrier_y) < 60:
                x = random.randint(-19, 19) * 20
                y = random.randint(-14, 14) * 20
        
        self.food.goto(x, y)
        
        # Reset timer for Level 3
        if self.level >= 3:
            self.food_timer = time.time()
    
    def place_red_food(self):
        x = random.randint(-19, 19) * 20
        y = random.randint(-14, 14) * 20
        
        # Ensure red food doesn't spawn on regular food or barrier
        while (x == self.food.xcor() and y == self.food.ycor()) or \
              (self.level >= 2 and self.barrier_active and 
               abs(x - self.barrier.xcor()) < 60 and abs(y - self.barrier.ycor()) < 60):
            x = random.randint(-19, 19) * 20
            y = random.randint(-14, 14) * 20
        
        self.red_food.goto(x, y)
        self.red_food.showturtle()
        self.red_food_active = True
        self.red_food_timer = time.time()  # Start timer for red food
    
    def check_food_collision(self):
        # Regular food collision
        if self.snake_head.distance(self.food) < 20:
            self.place_food()
            self.score += 1
            self.add_body_segment()
            self.check_level_progression()
            
        # Red food collision (Level 4)
        if self.level >= 4 and self.red_food_active and self.snake_head.distance(self.red_food) < 20:
            self.red_food.hideturtle()
            self.red_food_active = False
            self.score = max(0, self.score - 1)  # Don't let score go below 0
    
    def add_body_segment(self):
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        self.snake_body.append(new_segment)
    
    def move_body_segments(self):
        # Move body segments
        for i in range(len(self.snake_body) - 1, 0, -1):
            x = self.snake_body[i - 1].xcor()
            y = self.snake_body[i - 1].ycor()
            self.snake_body[i].goto(x, y)
        
        # Move first segment to head position
        if len(self.snake_body) > 0:
            x = self.snake_head.xcor()
            y = self.snake_head.ycor()
            self.snake_body[0].goto(x, y)
    
    def check_body_collision(self):
        for segment in self.snake_body:
            if self.snake_head.distance(segment) < 20:
                return True
        return False
    
    def check_level_progression(self):
        new_level = 1 + (self.score // 2)
        if new_level != self.level:
            self.level = new_level
            
            # Level 2: Add barrier
            if self.level == 2 and not self.barrier_active:
                self.add_barrier()
                self.check_snake_near_center()
            
            # Level 4: Start spawning red food immediately when level starts
            if self.level == 4 and not self.red_food_active:
                self.place_red_food()
            # Continue spawning red food occasionally at level 4+
            elif self.level >= 4 and not self.red_food_active and random.random() < 0.3:
                self.place_red_food()
        
        # Check for win condition: gain 5 points in Level 4 (score >= 8)
        if self.level == 4 and self.score >= 8:
            self.game_over = True
            self.show_win_message()
    
    def add_barrier(self):
        # Use last digit of index number (E252634)
        digit = "4"
        x = random.randint(-15, 15) * 20
        y = random.randint(-10, 10) * 20
        
        self.barrier.goto(x, y)
        self.barrier.write(digit, align="center", font=("Arial", 24, "bold"))
        self.barrier_active = True
    
    def check_snake_near_center(self):
        # If snake is near center when barrier appears, move to corner
        if abs(self.snake_head.xcor()) < 100 and abs(self.snake_head.ycor()) < 100:
            corners = [(-300, -200), (300, -200), (-300, 200), (300, 200)]
            corner = random.choice(corners)
            self.snake_head.goto(corner[0], corner[1])
    
    def check_barrier_collision(self):
        if self.level >= 2 and self.barrier_active:
            # Only collision from above ends the game
            snake_x = self.snake_head.xcor()
            snake_y = self.snake_head.ycor()
            barrier_x = self.barrier.xcor()
            barrier_y = self.barrier.ycor()
            
            # Check if snake is close to barrier horizontally and approaching from above
            if (abs(snake_x - barrier_x) < 30 and 
                snake_y > barrier_y and 
                snake_y - barrier_y < 30):
                return True
        return False
    
    def update_score_display(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}  Level: {self.level}", 
                               align="left", font=("Arial", 16, "normal"))
    
    def update_timer_display(self):
        if self.level >= 3:
            elapsed = time.time() - self.food_timer
            remaining = max(0, self.food_timeout - elapsed)
            self.timer_display.clear()
            if remaining > 0:
                self.timer_display.write(f"Food Timer: {remaining:.1f}s", 
                                       align="center", font=("Arial", 14, "normal"))
    
    def check_food_timeout(self):
        if self.level >= 3:
            elapsed = time.time() - self.food_timer
            if elapsed >= self.food_timeout:
                self.place_food()
    
    def check_red_food_timeout(self):
        if self.level >= 4 and self.red_food_active:
            elapsed = time.time() - self.red_food_timer
            if elapsed >= self.red_food_timeout:
                self.red_food.hideturtle()
                self.red_food_active = False
                # Respawn red food in a different location after a short delay
                if random.random() < 0.5:  # 50% chance to respawn immediately
                    self.place_red_food()
    
    def show_game_over(self):
        self.game_over_display.goto(0, 0)
        self.game_over_display.write("GAME OVER", align="center", 
                                   font=("Arial", 36, "bold"))
        self.game_over_display.goto(0, -50)
        self.game_over_display.write(f"Final Score: {self.score}  Level: {self.level}", 
                                   align="center", font=("Arial", 18, "normal"))
    
    def show_win_message(self):
        self.game_over_display.goto(0, 0)
        self.game_over_display.color("gold")
        self.game_over_display.write("YOU WON!", align="center", 
                                   font=("Arial", 36, "bold"))
        self.game_over_display.goto(0, -50)
        self.game_over_display.write(f"Congratulations! Final Score: {self.score}", 
                                   align="center", font=("Arial", 18, "normal"))
    
    def run_game(self):
        while not self.game_over:
            self.screen.update()
            
            # Check collisions
            if self.check_body_collision() or self.check_barrier_collision():
                self.game_over = True
                self.show_game_over()
                break
            
            # Move snake
            self.move_body_segments()
            self.move_snake()
            self.check_screen_wrap()
            
            # Check food collision
            self.check_food_collision()
            
            # Check food timeout (Level 3)
            self.check_food_timeout()
            
            # Check red food timeout (Level 4)
            self.check_red_food_timeout()
            
            # Level 4: Occasionally spawn red food
            if self.level >= 4 and not self.red_food_active and random.random() < 0.001:
                self.place_red_food()
            
            # Update displays
            self.update_score_display()
            self.update_timer_display()
            
            time.sleep(self.delay)
        
        # Keep window open after game over
        self.screen.exitonclick()

def main():
    try:
        game = SnakeGame()
        game.run_game()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()