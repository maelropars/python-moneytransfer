import asyncio
from mydefs import Transfer
from datetime import datetime, timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    # Create client connected to server at the given address
    client = await Client.connect("http://localhost:7233")

   
    handle = client.get_workflow_handle(workflow_id="657177fd-bdbd-4151-ad77-2a2291684e5e")
    await handle.signal(Transfer.confirm, True)
    print("signal sent")

if __name__ == "__main__":
    asyncio.run(main())
