# Module 1: The Age Calculator

**Concept:** Variables, Input, and Type Casting.

We build a simple app that asks for your name and age, then calculates the exact year you will turn 100.

### 📺 The Build Session
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/770xemnXhDU" frameborder="0" allowfullscreen></iframe>
</div>

### 🧠 Key Concepts
* **Input:** `input()` always returns a **string** (text), even if you type a number.
* **Casting:** We use `int()` to convert text into numbers for math.
* **F-Strings:** The clean way to combine text and variables: `f"Hello {name}"`.



### 💻 The Code Blueprint

```python
# 1. Ask for input
name = input("What is your name? ")
age_str = input("How old are you? ")   # This is text: "25"
age = int(age_str)                     # This is a number: 25

# 2. The Logic
current_year = 2026
years_left = 100 - age
turn_100_year = current_year + years_left

# 3. Output
print(f"{name}, you will turn 100 in the year {turn_100_year}")
```