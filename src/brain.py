from .memory import Memory
from .chat import ChatBot

__all__ = ["Brain"]

class Brain:
    def __init__(self):
        self._memory = Memory("You are a highly intelligent brain. Respond to the user based on the content from the files anf websites your memory.")
        self._chat = ChatBot(self._memory)

    def remember(self, memory):
        memory.add_memory(memory)

    def list_memories(self):
        return []

    def chat(self, prompt):
        return self._chat.send(prompt)