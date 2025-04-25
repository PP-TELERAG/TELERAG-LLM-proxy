import asyncio
import random

from pydantic import BaseModel
from typing import Dict, Optional

from Source.Services.Singleton import Singleton


class Message(BaseModel):
    key: Optional[str] = None
    payload: dict


class Topic:
    def __init__(
        self, name: str,
        partitions: int = 1,
        listener_url: Optional[str] = None
    ):
        self.name = name
        self.partitions = partitions
        self.listener_url = listener_url

        self.queue = [asyncio.Queue() for _ in range(partitions)]

    async def produce(self, message: dict, partition: Optional[int] = None):
        if partition is None:
            partition = random.randint(1, self.partitions - 1)

        elif partition < 0 or partition > self.partitions:
            raise ValueError("Incorrect partition number.")

        await self.queue[partition].put(message)

    async def consume(self, partition: int):
        if partition < 0 or partition > self.partitions:
            raise ValueError("Incorrect partition number.")
        if self.queue[partition].empty():
            raise ValueError(
                f"Partition {partition} is empty. No messages to consume."
            )
        message = await self.queue[partition].get()
        return message


class Broker(metaclass=Singleton):
    def __init__(self):
        self.topics: Dict[str, Topic] = {}

    def create_topic(
        self,
        name: str,
        partitions: int = 1,
        listener_url: Optional[str] = None
    ):
        if name in self.topics:
            raise ValueError(f"Topic with name '{name}' already exists.")
        self.topics[name] = Topic(name, partitions, listener_url)
        return self.topics[name]

    def get_topic_names(self):
        return list(self.topics.keys())
