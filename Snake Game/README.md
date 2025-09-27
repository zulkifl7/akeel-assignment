# Snake Game – AI Builder Instructions

This document provides the complete instructions to develop the **Snake Game** using Python and the `turtle` library. The AI builder must strictly follow the assignment scope and **not add any extra features beyond what is specified here**.

---

## 📋 Assignment Scope

The game must include all the following features and levels.

### 1. Basic Gameplay (Level 1)

* The snake moves continuously on the display.
* The snake’s direction is controlled using **keyboard input (arrow keys)**.
* Food appears randomly on the screen.
* When the snake eats food:

  * The food **must disappear immediately**.
  * The snake’s length increases by **1 unit**.
* If the snake collides with its own body, the game is over.
* There are **no walls** at the screen’s edges:

  * If the snake exits from one side, it reappears on the opposite side.
* Each food consumed adds **+1 point** to the score, which must be displayed on the screen.
* The game starts at **Level 1**.
* For every **2 points scored**, the level increases by 1.

---

### 2. Level Progression

* **Level 2**

  * A digit (the last digit of the index number) appears on the screen as a barrier.
  * If the snake collides with this digit, the game is over.
  * Food must not spawn too close to this digit (a margin is required).
  * If the snake is near the center when this digit appears, it must automatically shift to a corner.

* **Level 3**

  * Food disappears **5 seconds** after it appears.
  * A countdown timer must be displayed each time food appears.

* **Level 4**

  * Red food must appear occasionally.
  * Eating red food reduces the score.

---

## 📂 Submission Requirements

* **Project Files**

  * All code and related files must be included in one well-organized folder.
* **Video Demonstration**

  * A short video must demonstrate the game simulation, showing progress up to Level 4.
* **File Naming**

  * The project folder and all files must include the index number in their filenames.
  * Example: `1234567_SnakeGame.zip`.

---

## 🕹️ Controls

* **Arrow Keys** → Change snake direction.

---

## ⚙️ Instructions for AI Builder

1. **Setup**

   * Use **Python 3.x**.
   * Use the built-in `turtle` library for graphics.

2. **Game Initialization**

   * Create a game window using `turtle.Screen()`.
   * Set up the snake head and body using turtle objects.
   * Create a score display in the top corner of the screen.

3. **Food Handling**

   * Generate food at random positions on the screen.
   * Ensure food disappears immediately once eaten.
   * Update score by **+1** for each food eaten.
   * At Level 3, add logic for food timeout (5 seconds) with countdown timer.
   * At Level 4, add red food that decreases score.

4. **Snake Movement**

   * Use keyboard event listeners (`onkeypress`) for arrow keys.
   * Snake should keep moving in the last chosen direction until changed.
   * Implement screen wrap-around (no walls).

5. **Collision Handling**

   * Detect collision with food.
   * Detect collision with snake’s own body → End game.
   * From Level 2 onward, detect collision with the barrier digit → End game.

6. **Level Progression**

   * Start at Level 1.
   * Increase level by **1 for every 2 points scored**.
   * Implement barrier at Level 2.
   * Implement disappearing food with timer at Level 3.
   * Implement red food at Level 4.

7. **Game Over**

   * Display a game over message when the snake collides with itself or with the barrier.

---

## 🏆 Evaluation Criteria

The AI builder must implement the project according to the grading scheme:

| Criteria                       | Marks   |
| ------------------------------ | ------- |
| Basic Gameplay Mechanics       | 20      |
| Level Progression & Complexity | 25      |
| Display & Keyboard Interfacing | 15      |
| User Interface                 | 15      |
| Code Quality                   | 25      |
| **Total**                      | **100** |

---

## ✅ Notes

* Food must always disappear as soon as it is eaten.
* Only the features described in this document must be implemented.
* No extra enhancements or modifications are allowed.
* The index number must be included in all file names.

---
