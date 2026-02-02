# Module 5: The Smart Home

**Concept:** Object-Oriented Programming (OOP).

We model a Smart Home to master the 4 pillars. **OOP is A PIE**. In this module, we transition from writing "scripts" to building "architectures."

### 📺 The Build Session
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/YMNSBsjbO4E" frameborder="0" allowfullscreen></iframe>
</div>

### 🥧 The 4 Pillars (A PIE)


1.  **Abstraction:** Hiding complex details. We define *what* a device does, but not *how* until we build it.
2.  **Polymorphism:** Many forms. A `Light` and a `Speaker` both have a `turn_on()` button, but they do different things when pressed.
3.  **Inheritance:** Reusing code. All smart devices "inherit" the ability to connect to Wi-Fi from a single parent class.
4.  **Encapsulation:** Protecting data. We hide sensitive settings (like `__temperature`) so they can't be set to 500 degrees by mistake.

### 💻 The Code Blueprint

```python
from abc import ABC, abstractmethod

# 1. Abstraction & Inheritance (The Parent)
class SmartDevice(ABC):
    @abstractmethod
    def turn_on(self):
        """Every device MUST implement this."""
        pass

# 2. Polymorphism (The Children)
class SmartLight(SmartDevice):
    def turn_on(self):
        print("💡 Let there be light!")

# 3. Encapsulation (Protecting Data)
class Thermostat(SmartDevice):
    def __init__(self):
        self.__temp = 72  # Private variable (Double Underscore)
    
    def turn_on(self):
        print("🌡️ Thermostat activated.")

    def set_temp(self, t):
        # Industrial Safety Check
        if 60 <= t <= 80: 
            self.__temp = t
            print(f"Temperature set to {t}")
        else:
            print("Error: Temperature out of safe range!")
```