
import hatpologoyMessage_pb2 as pb
from hatpologoyMessage_pb2 import GeneratorMessage, StopMessage
from bleak import BleakScanner, BleakClient
import math
import asyncio
import signal
import sys
import subprocess
import os
dependencies = ['asyncio', 'bleak',
                'protobuf']


def install():
    for dependency in dependencies:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", dependency])


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
    def __init__(self):
        self.status_val = False
        self.stopped = False
        self.stay_in_while = True
        self.self.client = BleakClient()
        asyncio.run(self.main_())

    def c_print(self, text: str, color: bcolors):
        os.system('color')
        print(f"{color}{text}{bcolors.ENDC}\n")

    async def send_message(self, characteristic: str, message):
        await self.client.write_gatt_char("10000002-0000-0000-0000-98e65417a192", message.SerializeToString())

    async def vibrate(self, amplitude: float = 0.2, update: bool = False):
        message = GeneratorMessage()
        message.Channel = pb.Stream
        message.Env.Amplitude = amplitude
        message.Base.Waveform = pb.Sine
        message.AM.Waveform = pb.Square
        if not update:
            self.stopped = True
            message.Base.Frequency = 70
            message.AM.Frequency = 0
            message.AM.Depth = 0
            message.Env.AttackTime = 0.3
            message.Env.AttackWindow = pb.Lin

            # To w streamie do olania
            message.Base.Duration = 1
            message.Env.ReleaseTime = 0.1
            message.Env.ReleaseWindow = pb.Hann

            # To w singlu do olania
            message.Base.SemitonesPerSecond = 72
            message.Env.AmplitudePerSecond = 72
        else:
            message.Base.Frequency = 0
            message.AM.Frequency = 0
            message.AM.Depth = 0
            message.Env.AttackTime = 0.3
            message.Env.AttackWindow = pb.Lin

            # To w streamie do olania
            message.Base.Duration = 1
            message.Env.ReleaseTime = 0.1
            message.Env.ReleaseWindow = pb.Hann

            # To w singlu do olania
            message.Base.SemitonesPerSecond = 72
            message.Env.AmplitudePerSecond = 72

        await self.send_message("10000002-0000-0000-0000-98e65417a192", message)

    def handler(self, signum, frame):
        self.stay_in_while = False

    async def main_(self, address: str = "00:00:00:00:00", dev_name: str = ""):
        signal.signal(signal.SIGINT, self.handler)
        self.c_print(f"Started", bcolors.OKCYAN)
        self.c_print(f"Searching for devices", bcolors.OKCYAN)
        devices = await BleakScanner.discover(timeout=5.0)
        if(address != "00:00:00:00:00" or dev_name != ""):
            for device in devices:
                if(dev_name in device.name or address in device.address):
                    dev_name = device.name
                    self.c_print(f"Device found", bcolors.OKGREEN)
                    address = device.address
                    break
            try:
                self.c_print(f"Connecting", bcolors.OKCYAN)
                self.client = BleakClient(address)
                await self.client.connect(timeout=5.0)
                self.c_print(
                    f"ECU Connected, name: {dev_name}", bcolors.OKGREEN)
            except Exception as e:
                self.c_print(
                    f"Device with name:{dev_name} doesn't exist", bcolors.FAIL)
                return

        stop = StopMessage()
        stop.Channel = pb.Stream
        stop.Type = pb.soft
        while self.stay_in_while:
            avr_value = round(math.sqrt(
                math.pow(state.x, 2)+math.pow(state.y, 2)+math.pow(state.z, 2)), 2)
            if(avr_value > 1.0):
                avr_value = 1.0
            self.c_print(
                f"Average value of displacement {avr_value}", bcolors.OKCYAN)
            if(avr_value < 0.01):
                if self.stopped == True:
                    self.stopped = False
                    await self.client.write_gatt_char("70000002-0000-0000-0000-98e65417a192", stop.SerializeToString())
            else:
                await self.vibrate(self.client, amplitude=avr_value, update=self.stopped)
            await asyncio.sleep(0.2)
        self.c_print(f"Disconnecting", bcolors.OKCYAN)
        await self.client.write_gatt_char("70000002-0000-0000-0000-98e65417a192", stop.SerializeToString())
        await self.client.disconnect()
        self.c_print(f"ECU Disconnected", bcolors.OKGREEN)
        sys.exit(0)


# install()
BLE_ = BLE()
