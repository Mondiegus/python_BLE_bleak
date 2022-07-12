
import ast
from bleak import BleakScanner, BleakClient
import asyncio
import signal
import sys
dependencies = ['asyncio', 'bleak']


class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BLE():
    def __init__(self, address: str = "00:00:00:00:00", dev_name: str = "") -> None:
        self.address = address
        self.dev_name = dev_name
        self.stay_in_while = True
        self.client = BleakClient("")

    def c_print(self, text: str, color: bcolors) -> None:
        print(f"{color}{text}{bcolors.ENDC}\n")

    def handler(self, signum, frame) -> None:
        self.stay_in_while = False

    def set_address(self, address: str) -> None:
        self.address = address

    def set_name(self, name: str) -> None:
        self.name = name

    async def start_notify(self, characteristic: str, function) -> None:
        await self.client.start_notify(characteristic, ast.literal_eval(function)())

    async def stop_notify(self, characteristic: str) -> None:
        await self.client.stop_notify(characteristic)

    async def send_message(self, characteristic: str, message) -> None:
        await self.client.write_gatt_char(characteristic, message)

    async def connect_device(self) -> bool:
        try:
            self.c_print(f"Connecting", bcolors.OKCYAN)
            self.client = BleakClient(self.address)
            await self.client.connect(timeout=10.0)
            self.c_print(
                f"ECU Connected, name: {self.dev_name}", bcolors.OKGREEN)
            self.c_print(f"MAC address: {self.address}", bcolors.HEADER)
            return True
        except Exception as e:
            self.c_print(
                f"Device with name:{self.dev_name} doesn't exist. Error: {e}", bcolors.FAIL)
            return False

    async def disconnect_device(self) -> None:
        self.stay_in_while = False
        self.c_print(f"Disconnecting", bcolors.OKCYAN)
        await self.client.disconnect()
        self.c_print(f"ECU Disconnected", bcolors.OKGREEN)

    async def scan_for_device(self) -> bool:
        self.c_print(f"Searching for device", bcolors.OKCYAN)
        devices = await BleakScanner.discover(timeout=5.0)
        if(self.address != "00:00:00:00:00" or self.dev_name != ""):
            self.c_print(f"Devices list:", bcolors.OKGREEN)

            for device in devices:
                self.c_print(f"{device}", bcolors.OKGREEN)
                if(self.dev_name in device.name or self.address in device.address):
                    self.dev_name = device.name
                    self.c_print(f"Device found", bcolors.OKGREEN)
                    self.address = device.address
                    return True

            self.c_print(
                f"No device with name: {self.dev_name} or address: {self.address} found", bcolors.FAIL)
            return False

    async def main_(self):
        signal.signal(signal.SIGINT, self.handler)
        self.c_print(f"Started", bcolors.OKCYAN)

        while self.stay_in_while:
            await asyncio.sleep(0.2)

        sys.exit(0)
