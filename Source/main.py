from fastapi import FastAPI, HTTPException, responses
from typing_extensions import Optional

from Source.Services.Broker import Broker, Message

app = FastAPI()
message_broker = Broker()

@app.post("/topics")
def create_topic(topic: str, partitions: int = 1):

    try:
        message_broker.create_topic(topic, partitions)
        return {"message": f"Topic {topic} with {partitions} partitions created."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/topics")
def read_topics():
    try:
        topics = message_broker.get_topic_names()
        return {"message": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/topics/{topic_name}/produce")
async def produce_message(topic_name: str, message: Message, partition: Optional[int] = 1):

    if topic_name not in message_broker.topics:
        raise HTTPException(status_code=404, detail=f"Topic {topic_name} not found.")
    try:
        await message_broker.topics[topic_name].produce(message.model_dump(), partition)
        return {"message": f"Message sent to topic {topic_name}."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/topics/{topic_name}/consume/{partition}")
async def consume_message(topic_name: str, partition: int):
    if topic_name not in message_broker.topics:
        raise HTTPException(status_code=404, detail=f"Topic {topic_name} not found.")
    try:
        message = await message_broker.topics[topic_name].consume(partition)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/echo")
async def echo():
    return responses.Response(status_code=200)




