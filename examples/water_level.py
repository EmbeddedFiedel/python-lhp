"""Asynchronous client for the LHP API."""
import asyncio

from lhp import LHPClient


async def main():
    """Show example on using the LHP API client."""
    async with LHPClient() as lhp_client:
        current_water_level = await lhp_client.currentwaterlevel(
            pgnr="SH_111015",
        )
        print(current_water_level)


if __name__ == "__main__":
    asyncio.run(main())
