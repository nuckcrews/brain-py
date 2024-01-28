import os
from openai import OpenAI
from .memory import Memory
from .chat import ChatBot

__all__ = ["Brain"]


class Brain:
    def __init__(self):
        client = OpenAI()
        client.api_key = os.getenv("OPENAI_API_KEY")
        self._memory = Memory(
            "You are a highly intelligent brain. Respond to the user based on the content from the files and websites in your memory. Users can also add these resources to your memory.",
            client
        )
        self._chat = ChatBot(self._memory, client)

    def chat(self, prompt):
        return self._chat.send(prompt)

    def remember(self, memory):
        self._memory.add_memory(memory)

    def list_memories(self):
        return []
