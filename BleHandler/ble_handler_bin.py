from python_BLE_bleak.BleHandler.src.bleHandler import BLE
import asyncio

async def func():
    BLE_ = BLE(dev_name="WH-1000XM3")
    await BLE_.scan_for_device()
    await BLE_.connect_device()
    await asyncio.sleep(2)
    await BLE_.disconnect_device()

if __name__ == "__main__":
    asyncio.run(func())
   
