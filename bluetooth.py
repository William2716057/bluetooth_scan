import asyncio
from bleak import BleakScanner


async def main():
    print("Scanning...")

    devices = await BleakScanner.discover()

    for device in devices:
        print(f"{device.name}: {device.address}")


asyncio.run(main())