from .utils import announce, prompt_list

def main():
    announce("WELCOME TO YOUR BRAIN")

    action = prompt_list(
        "What would you like to do?",
        ["Chat", "Add a new memory", "View memories", "Exit"],
    )

    if action == "Exit":
        return

    elif action == "Chat":
        pass

    elif action == "Add a new memory":
        pass

    elif action == "View memories":
        pass