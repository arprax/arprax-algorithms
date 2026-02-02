# Module 2: The Casino Game

**Concept:** Loops, Logic, and Libraries.

We build a "Guess the Number" game. First in the console, then with a GUI.

### 📺 The Build Session
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/pje1Z49zj-8" frameborder="0" allowfullscreen></iframe>
</div>

### 🧠 Key Concepts
* **Libraries:** We import `random` to generate a secret number that changes every game.
* **While Loop:** This is a "conditional loop"—it keeps running as long as the player hasn't guessed the right number.
* **Turtle GUI:** We repurpose the Python drawing library to create interactive pop-up windows.



### 💻 The Code Blueprint (GUI Version)

```python
import turtle
import random

# 1. Setup the Game
secret_number = random.randint(1, 10)
guess = 0

# 2. The Game Loop
while guess != secret_number:
    # Pop-up input box
    guess = turtle.numinput("Casino Game", "Guess 1-10", minval=1, maxval=10)
    
    # 3. Decision Logic
    turtle.clear() # Clear previous text
    if guess < secret_number:
        turtle.write("Too Low!", align="center", font=("Arial", 16, "normal"))
    elif guess > secret_number:
        turtle.write("Too High!", align="center", font=("Arial", 16, "normal"))
    else:
        turtle.write("🏆 You Won!", align="center", font=("Arial", 20, "bold"))

turtle.done()
```