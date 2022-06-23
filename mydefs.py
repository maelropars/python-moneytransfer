import asyncio
from datetime import datetime, timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

@activity.defn
async def withdraw(accountId: str, referenceId: str, amountCents: int):
    print('in activity withdraw ' + str(amountCents))

@activity.defn
async def deposit(accountId: str, referenceId: str, amountCents: int):
    print('in activity deposit ' + str(amountCents))


@workflow.defn
class Transfer:
    def __init__(self) -> None:
        self._isconfirmed = True
        self._confirmation_update = asyncio.Event()

    @workflow.signal
    async def confirm(self, response: bool) -> None:
        self._isconfirmed = response
        self._confirmation_update.set()
        workflow.logger.debug("transfer confirmed")

    @workflow.run
    async def run(self, fromAccountId: str, toAccountId: str, referenceId: str, amountCents: int):
        if amountCents > 1000:
            self._isconfirmed = False
            workflow.logger.debug("waiting 30s")
            try:
                await asyncio.wait_for(self._confirmation_update.wait(), timeout=30)
            except asyncio.TimeoutError:
                 workflow.logger.debug("timeout! Transfer won't be executed")
        if self._isconfirmed:
            await workflow.execute_activity(
                    withdraw, args=[fromAccountId, referenceId, amountCents], schedule_to_close_timeout=timedelta(seconds=5)
                )
            await workflow.execute_activity(
                    deposit, args=[toAccountId, referenceId, amountCents], schedule_to_close_timeout=timedelta(seconds=5)
                )