# virtual_pet.py
import json
import random
import time

class Pet:
    def __init__(self, name):
        self.name = name
        self.health = 10
        self.happiness = 10
        self.hunger = 5
        self.cleanliness = 10
        self.energy = 10
        self.vaccinated = False
        self.age = 0

    def feed(self):
        self.hunger = max(0, self.hunger - 3)
        self.happiness += 1
        print(f"{self.name} has been fed.")

    def train(self):
        if self.energy >= 2:
            self.energy -= 2
            self.happiness += 2
            self.health += 1
            print(f"{self.name} had a great training session!")
        else:
            print(f"{self.name} is too tired to train.")

    def wash(self):
        self.cleanliness = 10
        self.happiness += 1
        print(f"{self.name} is now clean and happy.")

    def vaccinate(self):
        if not self.vaccinated:
            self.vaccinated = True
            self.health += 2
            print(f"{self.name} has been vaccinated!")
        else:
            print(f"{self.name} is already vaccinated.")

    def sleep(self):
        self.energy = 10
        print(f"{self.name} had a good sleep.")

    def tick(self):
        self.age += 1
        self.hunger += 1
        self.cleanliness = max(0, self.cleanliness - 1)
        self.energy = max(0, self.energy - 1)
        self.happiness = max(0, self.happiness - 1)
        if self.hunger > 7:
            self.health = max(0, self.health - 1)

    def status(self):
        return (
            f"Name: {self.name}\n"
            f"Age: {self.age} days\n"
            f"Health: {self.health}/10\n"
            f"Happiness: {self.happiness}/10\n"
            f"Hunger: {self.hunger}/10\n"
            f"Cleanliness: {self.cleanliness}/10\n"
            f"Energy: {self.energy}/10\n"
            f"Vaccinated: {'Yes' if self.vaccinated else 'No'}"
        )

class PetManager:
    def __init__(self):
        self.pets = {}

    def add_pet(self, name):
        if name in self.pets:
            print("Pet with that name already exists.")
        else:
            self.pets[name] = Pet(name)
            print(f"Added new pet: {name}")

    def get_pet(self, name):
        return self.pets.get(name, None)

    def remove_pet(self, name):
        if name in self.pets:
            del self.pets[name]
            print(f"Removed pet: {name}")

    def list_pets(self):
        if not self.pets:
            print("No pets available.")
        for name in self.pets:
            print(f"- {name}")

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump({k: vars(v) for k, v in self.pets.items()}, f)
        print("Progress saved.")

    def load(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for name, attrs in data.items():
                    pet = Pet(name)
                    pet.__dict__.update(attrs)
                    self.pets[name] = pet
            print("Progress loaded.")
        except FileNotFoundError:
            print("No saved data found.")

def main():
    manager = PetManager()
    manager.load('pets.json')

    while True:
        print("\n--- Virtual Pet System ---")
        print("1. Add Pet\n2. View Pet Status\n3. Feed\n4. Train\n5. Wash\n6. Vaccinate\n7. Sleep\n8. Next Day\n9. List Pets\n10. Save and Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter pet name: ")
            manager.add_pet(name)

        elif choice in {'2','3','4','5','6','7'}:
            name = input("Enter pet name: ")
            pet = manager.get_pet(name)
            if not pet:
                print("Pet not found.")
                continue
            if choice == '2':
                print(pet.status())
            elif choice == '3':
                pet.feed()
            elif choice == '4':
                pet.train()
            elif choice == '5':
                pet.wash()
            elif choice == '6':
                pet.vaccinate()
            elif choice == '7':
                pet.sleep()

        elif choice == '8':
            for pet in manager.pets.values():
                pet.tick()
            print("A day has passed for all pets.")

        elif choice == '9':
            manager.list_pets()

        elif choice == '10':
            manager.save('pets.json')
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
