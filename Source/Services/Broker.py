import asyncio
import random

from pydantic import BaseModel
from typing import Dict, Optional

from Source.Services.Singleton import Singleton

class Message(BaseModel):
    key: Optional[str] = None
    payload: dict

class Topic:
    def __init__(self, name: str, partitions: int = 1):
        self.name = name
        self.partitions = partitions

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
        message = await self.queue[partition].get()
        return message


class Broker(metaclass=Singleton):
    def __init__(self):
        self.topics: Dict[str, Topic] = {}

    def create_topic(self, name: str, partitions: int = 1):
        if name in self.topics:
            raise ValueError(f"Topic with name '{name}' already exists.")
        self.topics[name] = Topic(name, partitions)
        return self.topics[name]

