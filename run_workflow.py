import asyncio
import uuid
from mydefs import Transfer
from datetime import datetime, timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("http://localhost:7233")

    id=str(uuid.uuid4())
    await client.start_workflow(Transfer.run, args=["myaccount", "friendaccount", "ID", 1500], id=id, task_queue="moneytransfer-python")

    print("workflow executed " + id)

if __name__ == "__main__":
    asyncio.run(main())
