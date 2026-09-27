import asyncio
from bleak import BleakScanner


def guess_device_type(name):
    if not name:
        return "Unknown"

    name = name.lower()

    if "keyboard" in name:
        return "Keyboard"

    if "mouse" in name:
        return "Mouse"

    if "buds" in name or "airpods" in name:
        return "Headphones"

    if "watch" in name:
        return "Smartwatch"

    if "speaker" in name:
        return "Speaker"

    return "Unknown"


async def main():
    print("Scanning...\n")

    devices = await BleakScanner.discover(return_adv=True)

    for address, (device, advertisement) in devices.items():

        print("=" * 60)

        name = device.name or "Unknown"

        print(f"Name:              {name}")
        print(f"Address:           {address}")
        print(f"RSSI:              {advertisement.rssi} dBm")
        print(f"Local Name:        {advertisement.local_name}")
        print(f"TX Power:          {advertisement.tx_power}")

        # Guess device type
        device_type = guess_device_type(name)
        print(f"Device Type:       {device_type}")

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

        # Platform details deliberately omitted
        # print(device.details)


asyncio.run(main())