"""Asynchronous client for the LHP API."""
import asyncio

from lhp import LHP_client

async def main():
    """Show example on using the LHP API client."""
    async with LHP_client() as lhp_client:
        currentWaterLevel = await lhp_client.currentWaterLevel(
            pgnr="SH_111015",
        )
        print(currentWaterLevel)


if __name__ == "__main__":
    asyncio.run(main())
