import asyncio
from bleak import BleakScanner


async def main():
    print("Scanning...\n")

    devices = await BleakScanner.discover(return_adv=True)

    for address, (device, advertisement) in devices.items():

        print("=" * 60)

        print(f"Name:              {device.name or 'Unknown'}")
        print(f"Address:           {address}")
        print(f"RSSI:              {advertisement.rssi} dBm")
        print(f"Local Name:        {advertisement.local_name}")
        print(f"TX Power:          {advertisement.tx_power}")
        
        print("\nService UUIDs:")
        for uuid in advertisement.service_uuids:
            print(f"  {uuid}")

        print("\nManufacturer Data:")
        for company_id, data in advertisement.manufacturer_data.items():
            print(f"  Company ID: {company_id}")
            print(f"  Data:       {data.hex()}")

        print("\nService Data:")
        for uuid, data in advertisement.service_data.items():
            print(f"  UUID: {uuid}")
            print(f"  Data: {data.hex()}")

        print("\nPlatform Details:")
        print(device.details)


asyncio.run(main())