import pandas as pd
import numpy as np
from openai import OpenAI
from .extract import Extractor, File
from .utils import is_token_overflow, cosine_similarity

__all__ = ["Memory"]

session_memory_path = ".memory/session.csv"


class Memory:
    def __init__(self, system_prompt: str, openai_client: OpenAI):
        self.system_message = {"role": "system", "content": system_prompt}
        self.chat_messages = []
        self.openai_client = openai_client

    def context(self):
        memory_prompt = self._create_memory_prompt()
        files_paths = self._find_nearest_paths(memory_prompt)
        content = "\n\n-----\n".join(
            [Extractor(path).extract()[0].content for path in files_paths]
        )
        content_message = {"role": "user", "content": f"Content:\n\n{content}"}

        new_context = [self.system_message, content_message, *self.chat_messages]

        is_overflow = is_token_overflow(
            "".join([message["content"] for message in new_context])
        )
        while is_overflow:
            self._remove_earliest_chat()
            new_context = [
                self.system_message,
                content_message,
                *self.chat_messages,
            ]
            is_overflow = is_token_overflow(
                "".join([message["content"] for message in new_context])
            )

        return new_context

    def add_chat(self, chat_message):
        self.chat_messages.append({"role": "user", "content": chat_message})

    def add_bot_chat(self, bot_chat_message):
        self.chat_messages.append({"role": "assistant", "content": bot_chat_message})

    def add_memory(self, path):
        memories = Extractor(path).extract()
        self._embed(memories)

    def _embed(self, files: list[File]):
        embeddings = []
        for file in files:
            embedding = self.openai_client.embeddings.create(input=file.content, model="text-embedding-3-small").data[0].embedding
            embeddings.append(
                {"path": file.path, "name": file.name, "embedding": embedding}
            )

        new_df = pd.DataFrame(embeddings, columns=["path", "name", "embedding"])
        try:
            existing_df = pd.read_csv(session_memory_path)
            frames = [existing_df, new_df]
            df = pd.concat(frames)
            df.to_csv(session_memory_path)
        except FileNotFoundError:
            new_df.to_csv(session_memory_path)
        except pd.errors.EmptyDataError:
            new_df.to_csv(session_memory_path)

    def _find_nearest_paths(self, prompt: str, k: int = 4):
        try:
            df = pd.read_csv(session_memory_path)
            prompt_embedding = self.openai_client.embeddings.create(input=prompt, model="text-embedding-3-small").data[0].embedding
            df["embedding"] = df.embedding.apply(eval).apply(np.array)
            df["similarity"] = df.embedding.apply(
                lambda x: cosine_similarity(x, prompt_embedding)
            )
            return df.sort_values("similarity", ascending=False).head(k).path.tolist()
        except FileNotFoundError:
            return []
        except pd.errors.EmptyDataError:
            return []

    def _remove_earliest_chat(self):
        self.chat_messages.pop(0)

    def _create_memory_prompt(self):
        response = self.openai_client.completions.create(model="davinci-002",
        prompt=self._memory_context(),
        max_tokens=256,
        temperature=0)

        return response.choices[0].text.strip()

    def _memory_context(self):
        messages = [message["content"] for message in self.chat_messages[-5:]]

        is_overflow = is_token_overflow("; ".join(messages), model="gpt-4")
        while is_overflow:
            messages.pop(0)
            is_overflow = is_token_overflow(
                "; ".join(messages),
                model="gpt-4",
            )

        message_history = "; ".join(messages)

        setup_message = "Write a short prompt for a semantic file search query based on the need of the latest chat message. Output only the prompt."
        return setup_message + f"\n\nMessages:\n\n{message_history}\n\nPrompt:"
