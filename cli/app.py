import os
from .utils import announce, prompt_list, prompt_string
from src import Brain

def main():
    os.system("clear")
    announce("WELCOME TO YOUR BRAIN")

    brain = Brain()

    while True:
        action = prompt_list(
            "What would you like to do?",
            ["Chat", "Add a new memory", "View memories", "Exit"],
        )

        if action == "Exit":
            return

        elif action == "Chat":
            prompt = prompt_string("What would you like to say?")
            brain.chat(prompt)

        elif action == "Add a new memory":
            path = prompt_string("What is the path to the memory?")
            try:
                brain.remember(path)
                announce("Memory added.")
            except Exception as e:
                print(f"Error: {e}")

        elif action == "View memories":
            memories = brain.list_memories()
            if len(memories) == 0:
                announce("You have no memories.")
                continue
            else:
                announce("Your memories are:")
                for memory in memories:
                    announce(memory)
                continue