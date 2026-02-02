# Module 6: The Data Pipeline

**Concept:** APIs, Pandas, and Matplotlib.

This is the real-world data science workflow. We move from raw web data to actionable visual insights using the "Extract, Transform, Load" (ETL) methodology.

### 📺 The Build Session
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/7RbLMQ8T2fk" frameborder="0" allowfullscreen></iframe>
</div>

### 🧠 Key Concepts
* **Requests:** The library we use to "talk" to the internet. We fetch raw JSON data from an API.
* **Normalization:** Raw data is often "nested" (like a box inside a box). We use `pd.json_normalize` to flatten it into a clean spreadsheet format.
* **Pandas:** The "Excel for Python." It allows us to sort, filter, and calculate statistics on thousands of rows instantly.



### 💻 The Code Blueprint

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. Fetch (Extract)
# We pull user data from a mock REST API
response = requests.get("[https://jsonplaceholder.typicode.com/users](https://jsonplaceholder.typicode.com/users)")
data = response.json()

# 2. Clean & Process (Transform)
# Flatten nested JSON data into a Pandas DataFrame
df = pd.json_normalize(data)

# 3. Visualize (Load/Report)
# We create a bar chart showing the length of company catchphrases
plt.figure(figsize=(10, 6))
plt.bar(df['username'], df['company.catchPhrase'].str.len(), color='teal')

plt.title("User Profile: Catchphrase Complexity")
plt.xlabel("Username")
plt.ylabel("Character Count")
plt.xticks(rotation=45)
plt.tight_layout() # Ensures labels don't get cut off
```