# Module 4: The Car Simulator

**Concept:** Functions, Dictionaries, and Modular Logic.

We build a car dashboard with a GPS, engine startup, and fuel calculator. This lesson teaches you how to break large problems into small, manageable parts.

### 📺 The Build Session
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/wKyePEkzw2E" frameborder="0" allowfullscreen></iframe>
</div>

### 🧠 Key Concepts
* **Dictionary:** Like a Vending Machine—you provide the **Key** (the name) and you get the **Value** (the data).
* **Functions:** `def start_engine():` creates a "module" of code that can be reused infinitely without rewriting it.
* **The Ignition Key:** `if __name__ == "__main__":` is a safeguard. It ensures the car only starts when you turn the key directly, not when another program is just "inspecting" its parts.



### 💻 The Code Blueprint

```python
# 1. Defining the Parts (Functions)
def start_engine():
    """Simulates starting the car's motor."""
    print("Vroom! Engine Started.")

def calculate_fuel(miles):
    """Calculates gallons needed for a trip."""
    return miles / 25  # Returns the value back to the main program

# 2. The Ignition Key (Modular Control)
if __name__ == "__main__":
    # This code only runs if we execute this file directly
    start_engine()
    
    trip_miles = 100
    gallons_needed = calculate_fuel(trip_miles)
    
    print(f"Trip of {trip_miles} miles used {gallons_needed} gallons.")
```