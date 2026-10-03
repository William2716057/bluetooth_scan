import asyncio
from bleak import BleakScanner
from datetime import datetime

KNOWN_COMPANIES = {
    0x004C: "Apple, Inc.",
    0x0006: "Microsoft",
    0x00E0: "Google",
    0x0075: "Samsung Electronics Co. Ltd.",
    0x000F: "Broadcom Corporation",
    0x0002: "Intel Corp.",
    0x008C: "Nordic Semiconductor ASA",
    0x0087: "Garmin International, Inc.",
    0x0059: "Nordic Semiconductor ASA",  
    0x004D: "Motorola",
    0x0157: "Anhui Huami Information Technology (Amazfit/Xiaomi ecosystem)",
    0x038F: "Xiaomi Inc.",
    0x0171: "Amazon.com Services, Inc.",
    0x00D2: "AbTemp",
    0x0499: "Ruuvi Innovations Ltd.",
    0x0301: "Fitbit, Inc.",
    0x000D: "Texas Instruments Inc.",
    0x01DA: "Bose Corporation",
    0x0025: "Plantronics, Inc. (Poly)",
    0x0078: "Harman International",
    0x03DA: "OPPO Mobile Telecommunications",
}

def lookup_company(company_id):
    return KNOWN_COMPANIES.get(company_id, "Not found")

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

    devices = await BleakScanner.discover(timeout=8.0, return_adv=True)
    

    for address, (device, advertisement) in devices.items():

        print("=" * 60)

        name = device.name or "Unknown"
        print(f"Time of detection: {datetime.now()}")
        print(f"Name:              {name}")
        print(f"Address:           {address}")
        print(f"RSSI:              {advertisement.rssi} dBm")
        print(f"Local Name:        {advertisement.local_name}")
        print(f"TX Power:          {advertisement.tx_power}")
        
    if advertisement.tx_power is not None:
        n = 2.5  # adjust for environment
        distance = 10 ** ((advertisement.tx_power - advertisement.rssi) / (10 * n))
        print(f"Estimated Distance:     {distance:.2f} m")
    else:
        print("Estimated Distance:     N/A (no TX power broadcast)")
        
        # Guess device type
        device_type = guess_device_type(name)
        print(f"Device Type:       {device_type}")

        print("\nService UUIDs:")
        for uuid in advertisement.service_uuids:
            print(f"  {uuid}")

        print("\nManufacturer Data:")
        for company_id, data in advertisement.manufacturer_data.items():
            company_name = lookup_company(company_id)
            print(f"  Company ID: 0x{company_id:04X} ({company_name})")
            print(f"  Data:       {data.hex()}")

        print("\nService Data:")
        for uuid, data in advertisement.service_data.items():
            print(f"  UUID: {uuid}")
            print(f"  Data: {data.hex()}")

        # Platform details deliberately omitted
        # print(device.details)


asyncio.run(main())

#add csv file saving features

"""
Device
??? Advertised name
??? Observed address
??? Address type
?   ??? Public
?   ??? Random Static
?   ??? RPA
?   ??? NRPA
??? Manufacturer
??? Service UUIDs
??? RSSI
??? First/last observed
"""

"""
Bleak - application-level BLE scanning
BlueZ  bluetoothctl - Linux Bluetooth management
btmon - Bluetooth HCI packet capture on Linux
Wireshark - detailed BLE packet analysis
Kismet - wireless/Bluetooth discovery and monitoring
"""