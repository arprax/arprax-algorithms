# Module 3: The Task Manager

**Concept:** File I/O, Sets, and Data Persistence.

Variables die when the program closes. We fix that by saving data to a text file so your progress is never lost.

### 📺 The Build Session
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/xCYtdI1woSY" frameborder="0" allowfullscreen></iframe>
</div>

### 🧠 Key Concepts
* **Context Manager:** Using `with open(...)` is the industrial standard. It ensures the file is closed properly even if the program crashes.
* **Sets:** Unlike lists, **Sets** cannot contain duplicates. Converting a list to a set and back to a list is the fastest way to "clean" data.
* **Persistence:** This is the bridge between temporary memory (RAM) and long-term storage (Disk).



### 💻 The Code Blueprint

```python
# 1. Load Data (Reading from Disk)
try:
    with open("tasks.txt", "r") as file:
        # Strip removes hidden newline characters (\n)
        tasks = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    tasks = []

# 2. Add Task & Remove Duplicates
new_task = input("Add task: ")
tasks.append(new_task)

# The "Set Trick": Industrial way to remove duplicates instantly
tasks = list(set(tasks))

# 3. Save Data (Writing to Disk)
with open("tasks.txt", "w") as file:
    for task in tasks:
        file.write(task + "\n")

print(f"Total active tasks: {len(tasks)}")
```