import threading
import os
import numpy
import time
import DobotDllType as dType

# if (state == dType.DobotConnect.DobotConnect_NoError):
#     for j in range(3):
#         wellCoords = [180, 0, 50, 0]
#         for i in range(6):
#             dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x=wellCoords[0], y=wellCoords[1], z=wellCoords[2], rHead=wellCoords[3], isQueued=1)
#             wellCoords[0]+=20
#             wellCoords[2] = - wellCoords[2]
#     lIDX = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x=(wellCoords[0] - 40), y=wellCoords[1], z=wellCoords[2], rHead=wellCoords[3])[0]

#     dType.SetQueuedCmdStartExec(api)
#     while lIDX > dType.GetQueuedCmdCurrentIndex(api)[0]:
#         dType.dSleep(100)
#     dType.SetQueuedCmdStopExec(api)
# dType.DisconnectDobot(api)


class _Main:
    message = numpy.zeros((30, 1), dtype=numpy.uint8)

    def __init__(self) -> None:
        pass


class FRecord:
    HOMED = False
    colPos = 0
    colStartCoords = [[180, 0, 50, 0], [180, -20, 50, 0],
                      [180, -40, 50, 0], [180, -60, 50, 0]]  # x, y, z, r; let r = 0
    injectCoords = [[180, 0, -50, 0], [180, -20, -50, 0],
                    [180, -40, -50, 0], [180, -60, -50, 0]]
    wasteCoords = [200, 80, 140, 0]
    MotorIDX, PinchIDX, wellIDX = [0, 1, 2], [0, 1, 2], 1
    PumpingActive, MoveState, InjectState, WasteState, PumpDone = False, False, False, False, False
    INITSTATE, MoveInject, InjectWaste, MoveDone, FIRST = False, False, False, False, True

    def __init__(self) -> None:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        self.api, self.state = self.connectTo()
        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            dType.RestartMagicBox(self.api)
            dType.ClearAllAlarmsState(self.api)
            dType.SetQueuedCmdClear(self.api)
            # apply settings to instance
            if not self.HOMED:
                self.HOMED = self._HomeInstance
            self.main()
            # dType.GetQueuedCmdMotionFinish(self.api)
            # except KeyboardInterrupt:
            #     dType.ClearAllAlarmsState(self.api)
            #     dType.SetQueuedCmdForceStopExec(self.api)
            #     dType.SetQueuedCmdClear(self.api)
            #     dType.SetQueuedCmdStopExec(self.api)
            #     dType.DisconnectDobot(self.api)

    @staticmethod
    def connectTo():
        CON_STR = {dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
                   dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound", dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
        api = dType.load()
        state = dType.ConnectDobot(api, "", 115200)[0]
        print("Connect status: ", CON_STR[state])
        return api, state

    @property
    def _HomeInstance(self, ) -> None:
        # Single homing called vs
        dType.GetQueuedCmdMotionFinish(self.api)
        # r was 200 idk if thats correct ?
        dType.SetHOMEParams(self.api, x=200, y=200, z=200, r=0, isQueued=1)
        dType.SetPTPJointParams(self.api, 200, 200, 200,
                                200, 200, 200, 200, 200, isQueued=1)
        dType.SetPTPCommonParams(self.api, 100, 100, isQueued=1)
        ls = dType.SetHOMECmd(self.api, temp=0, isQueued=1)[0]
        while ls > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(100)
        print(dType.GetArmSpeedRatio(self.api))
        return True

    @staticmethod
    def _pumpSample() -> None:
        _Main.message[27] = 1  # Pinch valve to growth chamber open.
        _Main.message[28] = 255  # Pump to maxima
        time.sleep(5)  # need to test the timings.
        _Main.message[28] = 0

    @staticmethod
    def _strelTube() -> None:
        _Main.message[27] = 0  # Pinch valve to growth chamber closed.
        _Main.message[26] = 255  # strel pump on flush bleach -> 5 s
        time.sleep(5)
        _Main.message[26] = 0  # strel pump on flush bleach -> 5 s
        # Then we wanna blast dH20 to get rid of bleach for double the duration. -> 10 s
        _Main.message[25] = 255
        time.sleep(10)
        _Main.message[25] = 0

    def checkPumpState(self, ) -> bool:
        if self.PumpingActive:
            return True
        return False

    def checkMoveState(self, ) -> bool:
        if not self.PumpingActive and self.MoveState:
            return True
        return False

    def ArmMovement(self, ) -> None:
        wellComplete = False
        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            if self.INITSTATE and self.checkMoveState():  # MoveState = true -> INITSTATE = true
                if self.FIRST:
                    dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=(self.colStartCoords[self.colPos][0]+(
                        self.wellIDX*20)), y=self.colStartCoords[self.colPos][1], z=self.colStartCoords[self.colPos][2], rHead=self.colStartCoords[self.colPos][3], isQueued=1)
                    dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=(self.injectCoords[self.colPos][0]+(
                        self.wellIDX*20)), y=self.injectCoords[self.colPos][1], z=self.injectCoords[self.colPos][2], rHead=self.injectCoords[self.colPos][3], isQueued=1)
                    self.FIRST = False
                else:
                    pose = dType.GetPose(self.api)
                    self.INITSTATE = False
                    self.MoveState = False
                    self.FIRST = True
            elif self.checkPumpState() and not self.MoveState() and self.InjectState:
                self._pumpSample()
            elif not self.InjectState and not self.checkPumpState() and self.checkMoveState():
                # if first time etc.
                dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=(self.colStartCoords[self.colPos][0]+(
                    self.wellIDX*20)), y=self.colStartCoords[self.colPos][1], z=self.colStartCoords[self.colPos][2], rHead=self.colStartCoords[self.colPos][3], isQueued=1)
                dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode,
                                x=self.wasteCoords[0], y=self.wasteCoords[1], z=self.wasteCoords[2], rHead=self.wasteCoords[3], isQueued=1)
                dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=self.wasteCoords[0], y=self.wasteCoords[1], z=(
                    self.wasteCoords[2]-60), rHead=self.wasteCoords[3], isQueued=1)
            elif self.InjectWaste and self.checkPumpState() and not self.checkMoveState():
                self._strelTube()
            elif not self.checkPumpState() and self.checkMoveState() and self.MoveDone:
                dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode,
                                x=self.wasteCoords[0], y=self.wasteCoords[1], z=self.wasteCoords[2], rHead=self.wasteCoords[3], isQueued=1)
                wellComplete = True
            if wellComplete:
                self.wellIDX += 1
                if ((self.wellIDX // 6) == 1) or ((self.wellIDX // 6) == 2) or ((self.wellIDX // 6) == 3):
                    self.colPos += 1
                    self.wellIDX = 1

    # def main(self, ) -> None:
    #     # time.sleep is just better...
    #     dType.GetQueuedCmdMotionFinish(self.api)
    #     # idk if commands in here should be queued into the buffer.
    #     _Main.message[29] = 1
    #     if (self.state == dType.DobotConnect.DobotConnect_NoError) and (_Main.message[29] > 0): # _Main.message[29] = well position -> 1, 2, 3 ... 4 going up then across once 6 is achieved. Best to add a timer to this function, I.E sample rate = 3600 seconds -> 1 hour, do action.
    #         for i in range(0, 23):
    #             # Each well needs three actions -> init pos, z=+50 -> probe pos, z=-50 -> reset pos -> z=+50 then over waste. E.G
    #             dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=self.colStartCoords[self.colPos][0], y=self.colStartCoords[self.colPos][1], z=self.colStartCoords[self.colPos][2], rHead=self.colStartCoords[self.colPos][3], isQueued=1)
    #             # Then we inject and pump the sample.
    #             dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=self.injectCoords[self.colPos][0], y=self.injectCoords[self.colPos][1], z=self.injectCoords[self.colPos][2], rHead=self.injectCoords[self.colPos][3], isQueued=1)
    #             self._pumpSample()
    #             # Then we reset the arm to standard pos.
    #             dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=self.colStartCoords[self.colPos][0], y=self.colStartCoords[self.colPos][1], z=self.colStartCoords[self.colPos][2], rHead=self.colStartCoords[self.colPos][3], isQueued=1)
    #             # Then we hover over waste pos.
    #             dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=self.wasteCoords[0], y=self.wasteCoords[1], z=self.wasteCoords[2], rHead=self.wasteCoords[3], isQueued=1)
    #             dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=self.wasteCoords[0], y=self.wasteCoords[1], z=(self.wasteCoords[2]-60), rHead=self.wasteCoords[3], isQueued=1)
    #             self._strelTube()
    #             ls = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x=self.wasteCoords[0], y=self.wasteCoords[1], z=self.wasteCoords[2], rHead=self.wasteCoords[3], isQueued=1)[0]
    #             # Then reset pos.

    #             self.colStartCoords[self.colPos][0] += 20
    #             self.injectCoords[self.colPos][0] += 20
    #             if i  == 5 or i == 11 or i == 17:
    #                 self.colPos += 1
    #             # if self.colStartCoords[self.colPos][0] >= 300:
    #             #     self.colPos += 1
    #         while ls > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
    #             dType.dSleep(100)


FRecord()
