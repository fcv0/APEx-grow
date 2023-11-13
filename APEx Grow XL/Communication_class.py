import serial
import time
import os
import csv
import struct
import numpy as np
from serial.tools import list_ports
import matplotlib.pyplot as plt


class Tools:
    def __init__(self, ) -> None:
        pass

    @property
    def find_port(self):
        ports = list_ports.comports(include_links=False)
        for port in ports:
            # We could use vendor ID also but this should suffice.
            if 'Arduino' in port.description:
                print(f'Found port: {port.device}')
                PORT = serial.Serial(port.device)
                break
            else:
                continue
        print('Device information: ', PORT)
        if PORT.isOpen():
            PORT.close()
        PORT = serial.Serial(port=port.device, baudrate=9600)
        PORT.flushInput(), PORT.flushOutput()
        print(f'Connecting to {PORT.name}')
        return PORT

    def reset_stores(self):
        self._OD_times = np.empty((1), dtype=np.uint32)
        self._OD = np.empty((6, 1), dtype=np.float32)
        self._OD.fill(np.nan)
        self._RawOD = np.empty((6, 1), dtype=np.float32)
        self._RawOD.fill(np.nan)
        self._OD_times_media = np.empty((1), dtype=np.uint32)
        self._OD_media = np.empty((6, 1), dtype=np.float32)
        self._OD_media.fill(np.nan)
        self._RawOD_media = np.empty((6, 1), dtype=np.float32)
        self._RawOD_media.fill(np.nan)
        self._Temp_times = np.array([], dtype=np.uint32)
        self._Temp = np.array([], dtype=np.float32)
        self._RawTemp = np.array([], dtype=np.uint16)
        self._TempIR = np.array([], dtype=np.float32)
        self._AmbientTempIR = np.array([], dtype=np.float32)
        self._Heater_power_times = np.array([], dtype=np.uint32)
        self._HeaterPower = np.array([], dtype=np.uint16)
        self._HeaterPowerSet = np.array([], dtype=np.uint16)
        self._Target_times = np.array([], dtype=np.uint32)
        self._Target_temp = np.array([], dtype=np.float32)
        self._Target_OD = np.array([], dtype=np.float32)
        self._Temp_times_media = np.array([], dtype=np.uint32)
        self._Temp_media = np.array([], dtype=np.float32)
        self._RawTemp_media = np.array([], dtype=np.uint16)
        self._TempIR_media = np.array([], dtype=np.float32)
        self._AmbientTempIR_media = np.array([], dtype=np.float32)
        self._Heater_power_times_media = np.array([], dtype=np.uint32)
        self._HeaterPower_media = np.array([], dtype=np.uint16)
        self._HeaterPowerSet_media = np.array([], dtype=np.uint16)
        self._Target_times_media = np.array([], dtype=np.uint32)
        self._Target_temp_media = np.array([], dtype=np.float32)
        self._Pump_times = np.empty((1), dtype=np.uint32)
        self._Pump = np.empty((9, 1), dtype=np.int16)
        self._absorb_scatter_times = np.empty((1), dtype=np.uint32)
        self._absorb = np.empty((6, 1), dtype=np.float32)
        self._absorb.fill(np.nan)
        self._scatter = np.empty((6, 1), dtype=np.float32)
        self._scatter.fill(np.nan)
        self._absorb_scatter_times_media = np.empty((1), dtype=np.uint32)
        self._absorb_media = np.empty((6, 1), dtype=np.float32)
        self._absorb_media.fill(np.nan)
        self._scatter_media = np.empty((6, 1), dtype=np.float32)
        self._scatter_media.fill(np.nan)

    def reset_generic_stores(self):
        self._Heater_power_times = np.array([], dtype=np.uint32)
        self._HeaterPower = np.array([], dtype=np.uint16)
        self._HeaterPowerSet = np.array([], dtype=np.uint16)
        self._Target_times = np.array([], dtype=np.uint32)
        self._Target_temp = np.array([], dtype=np.float32)
        self._Target_OD = np.array([], dtype=np.float32)
        self._Heater_power_times_media = np.array([], dtype=np.uint32)
        self._HeaterPower_media = np.array([], dtype=np.uint16)
        self._HeaterPowerSet_media = np.array([], dtype=np.uint16)
        self._Target_times_media = np.array([], dtype=np.uint32)
        self._Target_temp_media = np.array([], dtype=np.float32)
        self._Pump_times = self._Pump_times[-1:]
        self._Pump = self._Pump[:, -1:]

    @staticmethod
    def bytes_to_float(bytelist) -> float:
        return struct.unpack('f', bytelist[::-1])[0]

    @staticmethod
    def float_to_bytes(float_val) -> bytearray:
        try:
            float_val = float(float_val)
            return struct.pack('f', float_val)[::-1]
        except:
            print("{} was not able to be interpretted as a float".format(float_val))

    @staticmethod
    def log_info(info_array, headings, log_name, overwrite=False) -> None:
        WRT = 'w'

        if info_array is None:
            with open(log_name, "w", newline='') as log:
                writer = csv.writer(log)
                writer.writerow(headings)
            return

        # os.chdir('/logs/')
        # arrays need to be transposed at some point here; something like the below. I think reshape(-1, 1) for transposition was working ok.
        # .T is being a bitch... reshape was ok at doing the job, data seemed to stay the same.

        if not (len(info_array.shape) == 1) and info_array.shape[0] > 1 and info_array.shape[1] > 1:
            # ARRAY = np.hstack((info_array[i].reshape(-1, 1)
            #                    for i in range(len(info_array))))
            ARRAY = info_array
        else:
            ARRAY = np.hstack((info_array.reshape(-1, 1)))
        if os.path.isfile(log_name) == False or overwrite:
            WRT = 'w'
        else:
            WRT = "a"
        with open(log_name, WRT, newline='') as log:
            writer = csv.writer(log)
            if WRT == "w":
                writer.writerow(headings)
            if len(ARRAY.shape) == 1:
                writer.writerow(ARRAY)
            else:
                writer.writerows(ARRAY)

    def send_data(self):
        self._Device.write(bytes(self._Outbound))


class Communication(Tools):
    def __init__(self) -> None:
        super().__init__()
        self.Status = 0
        self._DeviceStatus = 0
        self._Device = None
        self._logcomms = None

        self.generic_log_interval = 60

        self._OD_times = np.empty((1), dtype=np.uint32)
        self._OD = np.empty((6, 1), dtype=np.float32)
        self._OD.fill(np.nan)
        self._RawOD = np.empty((6, 1), dtype=np.float32)
        self._RawOD.fill(np.nan)
        self._OD_times_media = np.empty((1), dtype=np.uint32)
        self._OD_media = np.empty((6, 1), dtype=np.float32)
        self._OD_media.fill(np.nan)
        self._RawOD_media = np.empty((6, 1), dtype=np.float32)
        self._RawOD_media.fill(np.nan)
        self._Temp_times = np.array([], dtype=np.uint32)
        self._Temp = np.array([], dtype=np.float32)
        self._RawTemp = np.array([], dtype=np.uint16)
        self._TempIR = np.array([], dtype=np.float32)
        self._AmbientTempIR = np.array([], dtype=np.float32)
        self._Heater_power_times = np.array([], dtype=np.uint32)
        self._HeaterPower = np.array([], dtype=np.uint16)
        self._HeaterPowerSet = np.array([], dtype=np.uint16)
        self._Target_times = np.array([], dtype=np.uint32)
        self._Target_temp = np.array([], dtype=np.float32)
        self._Target_OD = np.array([], dtype=np.float32)
        self._Temp_times_media = np.array([], dtype=np.uint32)
        self._Temp_media = np.array([], dtype=np.float32)
        self._RawTemp_media = np.array([], dtype=np.uint16)
        self._TempIR_media = np.array([], dtype=np.float32)
        self._AmbientTempIR_media = np.array([], dtype=np.float32)
        self._Heater_power_times_media = np.array([], dtype=np.uint32)
        self._HeaterPower_media = np.array([], dtype=np.uint16)
        self._HeaterPowerSet_media = np.array([], dtype=np.uint16)
        self._Target_times_media = np.array([], dtype=np.uint32)
        self._Target_temp_media = np.array([], dtype=np.float32)
        self._Pump_times = np.zeros((1), dtype=np.uint32)
        self._Pump = np.zeros((9, 1), dtype=np.int16)
        self._absorb_scatter_times = np.empty((1), dtype=np.uint32)
        self._absorb = np.empty((6, 1), dtype=np.float32)
        self._absorb.fill(np.nan)
        self._scatter = np.empty((6, 1), dtype=np.float32)
        self._scatter.fill(np.nan)
        self._absorb_scatter_times_media = np.empty((1), dtype=np.uint32)
        self._absorb_media = np.empty((6, 1), dtype=np.float32)
        self._absorb_media.fill(np.nan)
        self._scatter_media = np.empty((6, 1), dtype=np.float32)
        self._scatter_media.fill(np.nan)
        self._FolderPath = ''
        self._Inbound = np.zeros(60, dtype=np.uint8)
        self._Outbound = np.zeros(60, dtype=np.uint8)
        self._DecodedInboundLog = []
        self._TimeInit = time.time()
        self._RealTime = 0
        self._LastGenericLogTime = 0
        self._comm_turn = True
        ####

        self._OD_calibration_gradient = 1
        self._OD_calibration_offset = 0
        self._OD_reference_absorbance = 3300000

        self._OD_target = 20

        self._OD_pid_enable = False
        self._OD_P = 1
        self._OD_I = 0
        self._OD_D = 0

        self._temp_calibration_gradient = 1
        self._temp_calibration_offset = 0

        self._temp_target = 37

        self._temp_pid_enable = False
        self._temp_P = 1
        self._temp_I = 0
        self._temp_D = 0

        self._pump_overides = np.full((9), False)
        self._pump_overide_speeds = np.zeros((9), dtype=np.uint8)
        self._pump_overide_directions = np.zeros((9), dtype=bool)

        self._pumps_on_delay = np.full((9), False)
        self._pump_delay_pump = 0
        self._pump_delay_speed = 255
        self._pump_delay_time = 0

        self._sequance_list = np.empty((1, 14))
        self._sequence_index = 0
        self._sequence_loaded = False

        self._OD_plot_min_t = 0

        self._OD_plot_enable = np.array(
            [False, False, False, False, False, False])
        self._OD_plot_enable_media = np.array(
            [False, False, False, False, False, False])

        self._Temp_plot_min_t = 0
        self._Temp_plot_enable = np.array(
            [False, False])
        self._Temp_plot_enable_media = np.array(
            [False, False])

        # fossil record

        self._fossil_record_connected = True
        self._well_plate_size = (4, 6)
        self._well_plate_spacing = (1.89, 1.89)
        self._gantry_size = (250, 250)
        self._motor_steps_per_rev = (200, 200)
        self._motor_RPMs = (150, 150)
        self._distance_per_rev = (0.8, 0.8)

        self._distance_to_move = (0, 0)
        self._steps_to_move = (0, 0)
        self._position_to_move_to = (0, 0)
        self._well_to_move_to = 0

        self._set_well_as_first_flag = True

        ####

        self.setup

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, value):
        self._Status = value

    def set_Status(self, value):
        self._Status = value

    def set_plot_bools(self, plot_string, plot_num, value):
        if plot_string == "OD":
            self._OD_plot_enable[plot_num] = value
        elif plot_string == "OD Media":
            self._OD_plot_enable_media[plot_num] = value
        elif plot_string == "Temp":
            self._Temp_plot_enable[plot_num] = value
        elif plot_string == "Temp Media":
            self._Temp_plot_enable_media[plot_num] = value

    def save_sequence(self, filepath="sequence.csv"):
        try:
            if filepath == "":
                raise Exception("Empty Filepath Provided")
            if filepath[-4:] != ".csv":
                filepath += ".csv"
            np.savetxt(filepath, self._sequance_list, delimiter=",")
        except Exception as e:
            print("Sequence Not Saved: ", e)

    def load_sequence(self, filepath):
        try:
            self._sequence_loaded = True
            if filepath[-4:] != ".csv":
                filepath += ".csv"
            self._sequance_list = np.loadtxt(filepath,
                                             delimiter=",", dtype=float)
        except Exception as e:
            print("Sequence Not Loaded: ", e)
            self._sequence_loaded = False

    def set_OD_calibration_gradient(self, value):
        if value == "" or value == "-":
            value = 0
        try:
            self._OD_calibration_gradient = float(value)
        except:
            print("invalid value encountered when trying to set OD calibration gradient: {} could not be interpreted as a float".format(value))
            self._OD_calibration_gradient = 1

    def set_OD_calibration_offset(self, value):
        if value == "" or value == "-":
            value = 0
        try:
            self._OD_calibration_offset = float(value)
        except:
            print("invalid value encountered when trying to set OD calibration offset: {} could not be interpreted as a float".format(value))
            self._OD_calibration_offset = 0

    def set_OD_reference_absorbance(self, value):
        if value == "":
            value = 0
        try:
            self._OD_reference_absorbance = float(value)
        except:
            print("invalid value encountered when trying to set OD reference absorbance: {} could not be interpreted as a float".format(value))
            self._OD_reference_absorbance = 3300000

    def set_OD_target(self, value):
        if value == "":
            value = 0
        try:
            self._OD_target = float(value)
        except:
            print("invalid value encountered when trying to set OD target: {} could not be interpreted as a float".format(value))
            self._OD_target = 20

    def set_OD_P(self, value):
        if value == "":
            value = 0
        try:
            self._OD_P = float(value)
        except:
            print("invalid value encountered when trying to set OD P: {} could not be interpreted as a float".format(value))
            self._OD_P = 1

    def set_OD_I(self, value):
        if value == "":
            value = 0
        try:
            self._OD_I = float(value)
        except:
            print("invalid value encountered when trying to set OD I: {} could not be interpreted as a float".format(value))
            self._OD_I = 0

    def set_OD_D(self, value):
        if value == "":
            value = 0
        try:
            self._OD_D = float(value)
        except:
            print("invalid value encountered when trying to set OD D: {} could not be interpreted as a float".format(value))
            self._OD_D = 0

    def set_temp_calibration_gradient(self, value):
        if value == "" or value == "-":
            value = 0
        try:
            self._temp_calibration_gradient = float(value)
        except:
            print("invalid value encountered when trying to set temperature calibration gradient: {} could not be interpreted as a float".format(value))
            self._temp_calibration_gradient = 1

    def set_temp_calibration_offset(self, value):
        if value == "" or value == "-":
            value = 0
        try:
            self._temp_calibration_offset = float(value)
        except:
            print("invalid value encountered when trying to set temperature calibration offset: {} could not be interpreted as a float".format(value))
            self._temp_calibration_offset = 1

    def set_temp_target(self, value):
        if value == "":
            value = 0
        try:
            self._temp_target = float(value)
        except:
            print("invalid value encountered when trying to set temperature target: {} could not be interpreted as a float".format(value))
            self._temp_target = 0

    def set_temp_P(self, value):
        if value == "":
            value = 0
        try:
            self._temp_P = float(value)
        except:
            print("invalid value encountered when trying to set temperature P: {} could not be interpreted as a float".format(value))
            self._temp_P = 1

    def set_temp_I(self, value):
        if value == "":
            value = 0
        try:
            self._temp_I = float(value)
        except:
            print("invalid value encountered when trying to set temperature I: {} could not be interpreted as a float".format(value))
            self._temp_I = 0

    def set_temp_D(self, value):
        if value == "":
            value = 0
        try:
            self._temp_D = float(value)
        except:
            print("invalid value encountered when trying to set temperature D: {} could not be interpreted as a float".format(value))
            self._temp_D = 0

    def set_pump_overide(self, pump, overide):
        self._pump_overides[pump] = overide

        self._Status = 4

    def set_pump_speed(self, pump, speed):
        try:
            speed = int(speed)
        except:
            speed = 0

        self._pump_overide_directions[pump] = speed < 0

        speed = abs(speed)

        self._pump_overide_speeds[pump] = speed

        self._Status = 4

    def set_distance_to_move(self, axis, value):
        try:
            value = float(value)
        except:
            value = 0
        self._distance_to_move = list(self._distance_to_move)
        self._distance_to_move[axis] = value
        self._distance_to_move = tuple(self._distance_to_move)

    def set_set_well_as_first_flag(self, first):
        self._set_well_as_first_flag = first
        self.set_Status(85)

    def set_od_plot_start_time(self, start_time):
        try:
            start_time = float(start_time)
        except:
            start_time = 0

        self._OD_plot_min_t = start_time

    def set_temp_plot_start_time(self, start_time):
        try:
            start_time = float(start_time)
        except:
            start_time = 0
        self._Temp_plot_min_t = start_time

    def check_inbound(self):
        if self._Device.in_waiting >= 60:
            rec = self._Device.read(60)
            self._Inbound = np.array([int(a)
                                     for a in rec], dtype=np.uint8)
            # print(rec)
            self._DecodedInboundLog.append(rec)
            # print(f'Data acquired: {rec}')

            status = rec[0]  # int.from_bytes(rec[0])
            self._DeviceStatus = status
            device_time = int.from_bytes(rec[1:5])
            # print(status,device_time)

            self.inbound_decoder(status, device_time, rec[5:])

            self._comm_turn = True

    def inbound_decoder(self, status, timestamp, package):
        if status == 0 or status == 1 or status == 10:

            temp_target = self.bytes_to_float(package[0:4])
            heater_power = int.from_bytes(package[4:6])
            heater_power_set = int.from_bytes(package[6:8])
            tmp_speeds = np.zeros((9, 1), dtype=np.int16)

            for i in range(9):
                tmp_speeds[i] = package[i+8]
                if package[i+17] == 1:
                    tmp_speeds[i] *= -1
                if tmp_speeds[i] == 0 and self._pumps_on_delay[i]:
                    self._pumps_on_delay[i] = False

            temp_target_media = self.bytes_to_float(package[26:30])
            heater_power_media = int.from_bytes(package[30:32])
            heater_power_set_media = int.from_bytes(package[32:34])
            OD_target = self.bytes_to_float(package[34:38])
            tmp_pump_time = int.from_bytes(package[38:42])

            self._Target_times = np.append(
                self._Target_times, timestamp)
            self._Target_temp = np.append(self._Target_temp, temp_target)

            self._Heater_power_times = np.append(
                self._Heater_power_times, timestamp)
            self._HeaterPower = np.append(self._HeaterPower, heater_power)
            self._HeaterPowerSet = np.append(
                self._HeaterPowerSet, heater_power_set)

            self._Target_times_media = np.append(
                self._Target_times_media, timestamp)
            self._Target_temp_media = np.append(
                self._Target_temp_media, temp_target)

            self._Heater_power_times_media = np.append(
                self._Heater_power_times_media, timestamp)
            self._HeaterPower_media = np.append(
                self._HeaterPower_media, heater_power_media)
            self._HeaterPowerSet_media = np.append(
                self._HeaterPowerSet_media, heater_power_set_media)

            self._Pump_times = np.append(self._Pump_times, tmp_pump_time)
            self._Pump = np.append(self._Pump, tmp_speeds, axis=1)

            self._Target_OD = np.append(self._Target_OD, OD_target)

        elif status == 4 or status == 7:
            tmp_OD = np.zeros((6, 1), dtype=np.float32)
            tmp_ODRaw = np.zeros((6, 1), dtype=np.float32)
            reading_time = int.from_bytes(package[0:4])

            tmp_OD[0] = self.bytes_to_float(package[4:8])
            tmp_OD[1] = self.bytes_to_float(package[8:12])
            tmp_OD[2] = self.bytes_to_float(package[12:16])
            tmp_OD[3] = self.bytes_to_float(package[16:20])
            tmp_OD[4] = self.bytes_to_float(package[20:24])
            tmp_OD[5] = self.bytes_to_float(package[24:28])

            # Same again:
            # N = 28
            # for i in range(len(tmp_ODRaw)):
            # tmp_ODRaw[i] = self.bytes_to_float(package[N:int(N+4)])
            tmp_ODRaw[0] = self.bytes_to_float(package[28:32])
            tmp_ODRaw[1] = self.bytes_to_float(package[32:36])
            tmp_ODRaw[2] = self.bytes_to_float(package[36:40])
            tmp_ODRaw[3] = self.bytes_to_float(package[40:44])
            tmp_ODRaw[4] = self.bytes_to_float(package[44:48])
            tmp_ODRaw[5] = self.bytes_to_float(package[48:52])

            if status == 4:
                self._OD_times = np.append(self._OD_times, reading_time)

                if self._OD is None:
                    self._OD = tmp_OD.copy()
                else:
                    self._OD = np.append(self._OD, tmp_OD, axis=1)

                if self._RawOD is None:
                    self._RawOD = tmp_ODRaw.copy()
                else:
                    self._RawOD = np.append(self._RawOD, tmp_ODRaw, axis=1)

                self.log_info(
                    np.hstack((self._OD_times[-1], self._OD[:, -1], self._RawOD[:, -1], self._absorb[:, -1], self._scatter[:, -1])), [], "OD_log.csv")
            elif status == 7:
                self._OD_times_media = np.append(
                    self._OD_times_media, reading_time)

                if self._OD_media is None:
                    self._OD_media = tmp_OD.copy()
                else:
                    self._OD_media = np.append(self._OD_media, tmp_OD, axis=1)

                if self._RawOD_media is None:
                    self._RawOD_media = tmp_ODRaw.copy()
                else:
                    self._RawOD_media = np.append(
                        self._RawOD_media, tmp_ODRaw, axis=1)

                self.log_info(
                    np.hstack((self._OD_times_media[-1], self._OD_media[:, -1], self._RawOD_media[:, -1], self._absorb_media[:, -1], self._scatter_media[:, -1])), [], "OD_media_log.csv")

        elif status == 5 or status == 8:
            tmp_absorb = np.zeros((6, 1), dtype=np.float32)
            tmp_scatter = np.zeros((6, 1), dtype=np.float32)
            reading_time = int.from_bytes(package[0:4])
            # Clean up code:
            # N = 4
            # for i in range(len(tmp_absorb)):
            #     tmp_absorb[i] = self.bytes_to_float(package[N:(int(N+4))])

            tmp_absorb[0] = self.bytes_to_float(package[4:8])
            tmp_absorb[1] = self.bytes_to_float(package[8:12])
            tmp_absorb[2] = self.bytes_to_float(package[12:16])
            tmp_absorb[3] = self.bytes_to_float(package[16:20])
            tmp_absorb[4] = self.bytes_to_float(package[20:24])
            tmp_absorb[5] = self.bytes_to_float(package[24:28])

            # Same again:
            # N = 28
            # for i in range(len(tmp_scatter)):
            # tmp_scatter[i] = self.bytes_to_float(package[N:int(N+4)])

            tmp_scatter[0] = self.bytes_to_float(package[28:32])
            tmp_scatter[1] = self.bytes_to_float(package[32:36])
            tmp_scatter[2] = self.bytes_to_float(package[36:40])
            tmp_scatter[3] = self.bytes_to_float(package[40:44])
            tmp_scatter[4] = self.bytes_to_float(package[44:48])
            tmp_scatter[5] = self.bytes_to_float(package[48:52])

            if status == 5:
                self._absorb_scatter_times = np.append(
                    self._absorb_scatter_times, reading_time)

                if self._absorb is None:
                    self._absorb = tmp_absorb.copy()
                else:
                    self._absorb = np.append(self._absorb, tmp_absorb, axis=1)

                if self._scatter is None:
                    self._scatter = tmp_scatter.copy()
                else:
                    self._scatter = np.append(
                        self._scatter, tmp_scatter, axis=1)
            elif status == 8:
                self._absorb_scatter_times_media = np.append(
                    self._absorb_scatter_times_media, reading_time)

                if self._absorb_media is None:
                    self._absorb_media = tmp_absorb.copy()
                else:
                    self._absorb_media = np.append(
                        self._absorb_media, tmp_absorb, axis=1)

                if self._scatter_media is None:
                    self._scatter_media = tmp_scatter.copy()
                else:
                    self._scatter_media = np.append(
                        self._scatter_media, tmp_scatter, axis=1)

        elif status == 6 or status == 9:
            reading_time = int.from_bytes(package[0:4])
            temp = self.bytes_to_float(package[4:8])
            raw_temp = int.from_bytes(package[8:10])
            heater_power = int.from_bytes(package[10:12])
            heater_power_set = int.from_bytes(package[12:14])
            temp_ir = self.bytes_to_float(package[14:18])
            ambient_temp_ir = self.bytes_to_float(package[18:22])

            if status == 6:
                self._Temp_times = np.append(self._Temp_times, reading_time)
                self._Temp = np.append(self._Temp, temp)
                self._RawTemp = np.append(self._RawTemp, raw_temp)
                self._TempIR = np.append(self._TempIR, temp_ir)
                self._AmbientTempIR = np.append(
                    self._AmbientTempIR, ambient_temp_ir)
                self._Heater_power_times = np.append(
                    self._Heater_power_times, reading_time)
                self._HeaterPower = np.append(self._HeaterPower, heater_power)
                self._HeaterPowerSet = np.append(
                    self._HeaterPowerSet, heater_power_set)

                self.log_info(
                    np.hstack((self._Temp_times[-1], self._Temp[-1], self._RawTemp[-1], self._TempIR[-1], self._AmbientTempIR[-1])), [], "temp_log.csv")
            elif status == 9:
                self._Temp_times_media = np.append(
                    self._Temp_times_media, reading_time)
                self._Temp_media = np.append(self._Temp_media, temp)
                self._RawTemp_media = np.append(self._RawTemp_media, raw_temp)
                self._TempIR_media = np.append(self._TempIR_media, temp_ir)
                self._AmbientTempIR_media = np.append(
                    self._AmbientTempIR_media, ambient_temp_ir)
                self._Heater_power_times_media = np.append(
                    self._Heater_power_times_media, reading_time)
                self._HeaterPower_media = np.append(
                    self._HeaterPower_media, heater_power)
                self._HeaterPowerSet_media = np.append(
                    self._HeaterPowerSet_media, heater_power_set)

                self.log_info(
                    np.hstack((self._Temp_times_media[-1], self._Temp_media[-1], self._RawTemp_media[-1], self._TempIR_media[-1], self._AmbientTempIR_media[-1])), [], "temp_media_log.csv")

    def check_sum(self, data, count=58):
        sum1, sum2 = 0, 0
        for i in range(count):
            sum1 = (sum1 + data[i]) % 255
            sum2 = (sum1 + sum2) % 255
        checksumH, checksumL = sum2, sum1
        # print(checksumH, checksumL)
        return checksumH, checksumL

    def construct_outbound(self):
        self._Outbound = np.zeros(60, dtype=np.uint8)
        # should wipe outbound first to avoid old data getting transmitted in the event of a code mistake
        self._Outbound[0] = self.Status
        self._RealTime = np.uint32(round(time.time() - self._TimeInit) * 1000)

        time_bytes = self._RealTime.tobytes()

        for i, b in enumerate(time_bytes):
            self._Outbound[4 - i] = b
        # Perhaps change to match case:

        if self.Status == 2:
            # Reset the arrays
            # self.reset_stores()
            self.Status = 0

        elif self.Status == 3:
            self.Status = 0

        elif self.Status == 4:
            # pump overides

            for i in range(9):
                self._Outbound[i + 5] = 1 if self._pump_overides[i] else 0
                self._Outbound[i + 14] = self._pump_overide_speeds[i]
                self._Outbound[i +
                               23] = 1 if self._pump_overide_directions[i] else 0

            self.Status = 0

        elif self.Status == 5:
            self._Outbound[5] = self._pump_delay_pump
            self._Outbound[6] = self._pump_delay_speed
            time_bytes = np.uint32(self._pump_delay_time).to_bytes()
            for i, b in enumerate(time_bytes):
                self._Outbound[10 - i] = b
            self._pumps_on_delay[self._pump_delay_pump] = True

        elif self.Status == 32 or self.Status == 33 or self.Status == 34:
            # run sequance transmission

            # make sure that rounding is all happening as expected

            self._Outbound[5] = self._sequance_list[self._sequence_index][0]

            time_trigger = np.uint32(
                self._sequance_list[self._sequence_index][1])
            time_bytes = time_trigger.tobytes()[::-1]
            for i, b in enumerate(time_bytes):
                self._Outbound[6 + i] = b

            temp_trigger_bytes = np.uint16.tobytes(
                np.uint16(self._sequance_list[self._sequence_index][2] * 10))[::-1]

            self._Outbound[10] = temp_trigger_bytes[0]
            self._Outbound[11] = temp_trigger_bytes[1]

            for i in range(6):
                OD_trigger_bytes = np.uint16.tobytes(
                    np.uint16(self._sequance_list[self._sequence_index][3 + i] * 100))[::-1]

                self._Outbound[12 + 2*i] = OD_trigger_bytes[0]
                self._Outbound[13 + 2*i] = OD_trigger_bytes[1]

            temp_target_bytes = np.uint16.tobytes(
                np.uint16(self._sequance_list[self._sequence_index][9] * 10))[::-1]

            self._Outbound[24] = temp_target_bytes[0]
            self._Outbound[25] = temp_target_bytes[1]

            self._Outbound[26] = self._sequance_list[self._sequence_index][10]

            OD_target_bytes = np.uint16.tobytes(
                np.uint16(self._sequance_list[self._sequence_index][11] * 100))[::-1]

            self._Outbound[27] = OD_target_bytes[0]
            self._Outbound[28] = OD_target_bytes[1]

            OD_drift_bytes = np.uint16.tobytes(
                np.uint16(self._sequance_list[self._sequence_index][12] * 100))[::-1]

            self._Outbound[29] = OD_drift_bytes[0]
            self._Outbound[30] = OD_drift_bytes[1]

            self._Outbound[31] = self._sequance_list[self._sequence_index][13]

            self._sequence_index += 1

            if self.Status == 32:
                sequence_length = len(self._sequance_list)
                sequence_length_bytes = np.uint16.tobytes(
                    np.uint16(sequence_length))[::-1]

                self._Outbound[32] = sequence_length_bytes[0]
                self._Outbound[33] = sequence_length_bytes[1]

                self.Status = 34 if self._sequence_index < len(
                    self._sequance_list) - 1 else 33

            elif self.Status == 33:
                self._sequence_index = 0
                self.Status = 0

            elif self.Status == 34:
                self.Status = 34 if self._sequence_index < len(
                    self._sequance_list) - 1 else 33

        elif self.Status == 48:
            # Temperature Calibration
            temp_calibration_gradient_bytes = self.float_to_bytes(
                self._temp_calibration_gradient)
            for i, b in enumerate(temp_calibration_gradient_bytes):
                self._Outbound[i+5] = b

            temp_calibration_offset_bytes = self.float_to_bytes(
                self._temp_calibration_offset)
            for i, b in enumerate(temp_calibration_offset_bytes):
                self._Outbound[i+9] = b

            self.Status = 0

        elif self.Status == 49:
            # temperature target
            temp_target_bytes = np.uint16.tobytes(
                np.uint16(self._temp_target * 10))[::-1]

            self._Outbound[5] = temp_target_bytes[0]
            self._Outbound[6] = temp_target_bytes[1]

            self.Status = 0

        elif self.Status == 50:
            # PID values for temperature system
            temp_P_bytes = self.float_to_bytes(
                self._temp_P)
            for i, b in enumerate(temp_P_bytes):
                self._Outbound[i+5] = b

            temp_I_bytes = self.float_to_bytes(
                self._temp_I)
            for i, b in enumerate(temp_I_bytes):
                self._Outbound[i+9] = b

            temp_D_bytes = self.float_to_bytes(
                self._temp_D)
            for i, b in enumerate(temp_D_bytes):
                self._Outbound[i+13] = b

            self._Outbound[17] = 1 if self._temp_pid_enable else 0

            self.Status = 0

        elif self.Status == 64:
            # OD Calibration

            OD_calibration_gradient_bytes = self.float_to_bytes(
                self._OD_calibration_gradient)
            for i, b in enumerate(OD_calibration_gradient_bytes):
                self._Outbound[i+5] = b

            OD_calibration_offset_bytes = self.float_to_bytes(
                self._OD_calibration_offset)
            for i, b in enumerate(OD_calibration_offset_bytes):
                self._Outbound[i+9] = b

            OD_reference_absorbance_bytes = self.float_to_bytes(
                self._OD_reference_absorbance)
            for i, b in enumerate(OD_reference_absorbance_bytes):
                self._Outbound[i+13] = b
            self.Status = 0

        elif self.Status == 65:
            # OD target
            OD_target_bytes = np.uint16.tobytes(
                np.uint16(self._OD_target * 100))[::-1]

            self._Outbound[5] = OD_target_bytes[0]
            self._Outbound[6] = OD_target_bytes[1]

            self.Status = 0

        elif self.Status == 66:
            # OD PID
            OD_P_bytes = self.float_to_bytes(
                self._OD_P)
            for i, b in enumerate(OD_P_bytes):
                self._Outbound[i+5] = b

            OD_I_bytes = self.float_to_bytes(
                self._OD_I)
            for i, b in enumerate(OD_I_bytes):
                self._Outbound[i+9] = b

            OD_D_bytes = self.float_to_bytes(
                self._OD_D)
            for i, b in enumerate(OD_D_bytes):
                self._Outbound[i+13] = b

            self._Outbound[17] = 1 if self._OD_pid_enable else 0

            self.Status = 0

        elif self.Status == 80:
            # connect dissconect fossil record
            self._Outbound[5] = 1 if self._fossil_record_connected else 0
            if (self._fossil_record_connected):
                self._Outbound[6] = self._well_plate_size[0]
                self._Outbound[7] = self._well_plate_size[1]
                well_plate_spacing_bytes = (
                    self.float_to_bytes(self._well_plate_spacing[0]),
                    self.float_to_bytes(self._well_plate_spacing[1]))

                gantry_size_bytes = (
                    self.float_to_bytes(self._gantry_size[0]),
                    self.float_to_bytes(self._gantry_size[1]))

                motor_steps_per_rev_bytes = (np.uint16.tobytes(np.uint16(self._motor_steps_per_rev[0]))[::-1],
                                             np.uint16.tobytes(np.uint16(self._motor_steps_per_rev[1]))[::-1])

                motor_RPMs_bytes = (
                    self.float_to_bytes(self._motor_RPMs[0]),
                    self.float_to_bytes(self._motor_RPMs[1]))
                distance_per_rev = (
                    self.float_to_bytes(self._distance_per_rev[0]),
                    self.float_to_bytes(self._distance_per_rev[1]))

                for i in range(4):
                    self._Outbound[i+8] = well_plate_spacing_bytes[0][i]
                    self._Outbound[i+12] = well_plate_spacing_bytes[1][i]

                    self._Outbound[i+16] = gantry_size_bytes[0][i]
                    self._Outbound[i+20] = gantry_size_bytes[1][i]

                    if i < 2:
                        self._Outbound[i+24] = motor_RPMs_bytes[0][i]
                        self._Outbound[i+26] = motor_RPMs_bytes[1][i]

                    self._Outbound[i+28] = motor_RPMs_bytes[0][i]
                    self._Outbound[i+32] = motor_RPMs_bytes[1][i]

                    self._Outbound[i+36] = distance_per_rev[0][i]
                    self._Outbound[i+40] = distance_per_rev[1][i]
            self.Status = 0

        elif self.Status == 81:
            # move fossil record by distance
            move_size_bytes = (self.float_to_bytes(self._distance_to_move[0]),
                               self.float_to_bytes(self._distance_to_move[1]))

            move_size_regen = (self.bytes_to_float(move_size_bytes[0]),
                               self.bytes_to_float(move_size_bytes[1]))

            print(self._distance_to_move, move_size_bytes, move_size_regen)

            for i in range(4):
                self._Outbound[i+5] = move_size_bytes[0][i]
                self._Outbound[i+9] = move_size_bytes[1][i]
            self.Status = 0

        elif self.Status == 82:
            # move fossil record by steps
            move_size_bytes = (np.int32.tobytes(np.int32(self._steps_to_move[0]))[::-1],
                               np.int32.tobytes(np.int32(self._steps_to_move[1]))[::-1])

            for i in range(4):
                self._Outbound[i+5] = move_size_bytes[0][i]
                self._Outbound[i+9] = move_size_bytes[1][i]
            self.Status = 0

        elif self.Status == 83:
            # move fossil record to position
            move_destination_bytes = (self.float_to_bytes(self._position_to_move_to[0]),
                                      self.float_to_bytes(self._position_to_move_to[1]))

            for i in range(4):
                self._Outbound[i+5] = move_destination_bytes[0][i]
                self._Outbound[i+9] = move_destination_bytes[1][i]
            self.Status = 0

        elif self.Status == 85:
            # set current pos as first/last well
            self._Outbound[5] = 1 if self._set_well_as_first_flag else 0
            self.Status = 0

        elif self.Status == 94:
            # set well plate dimensions
            if (self._fossil_record_connected):
                self._Outbound[5] = self._well_plate_size[0]
                self._Outbound[6] = self._well_plate_size[1]
                well_plate_spacing_bytes = (
                    self.float_to_bytes(self._well_plate_spacing[0]),
                    self.float_to_bytes(self._well_plate_spacing[1]))

                for i in range(4):
                    self._Outbound[i+7] = well_plate_spacing_bytes[0][i]
                    self._Outbound[i+11] = well_plate_spacing_bytes[1][i]
            self.Status = 0

        else:
            self.Status = 0

        checksumUB, checksumLB = self.check_sum(self._Outbound)
        self._Outbound[58] = checksumUB
        self._Outbound[59] = checksumLB

        # print(self._Outbound)

    @property
    def setup(self):
        # Main needs a loop lol, I'll leave it now as I need to relook into proactive command with python.
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        if os.path.isdir('logs') == False:
            os.makedirs(name='logs')
            print(f'Log folder created in file directory {__file__}')
        os.chdir('logs/')
        try:
            self._Device = self.find_port
        except:
            pass

        comm_log_lables = ["" for i in range(60)]
        comm_log_lables[0] = "Status"
        comm_log_lables[1] = "Time(ms)"
        comm_log_lables[58] = "Checksum"
        self.log_info(self._Outbound, comm_log_lables,
                      "comms_log.csv", overwrite=True)

        OD_log_labels = ["Time(ms)", "OD1", "OD2", "OD3", "OD4", "OD5", "OD6", "Raw OD1", "Raw OD2", "Raw OD3", "Raw OD4", "Raw OD5", "Raw OD6", "Absorb 1",
                         "Absorb 2", "Absorb 3", "Absorb 4", "Absorb 5", "Absorb 6", "Scatter 1", "Scatter 2", "Scatter 3", "Scatter 4", "Scatter 5", "Scatter 6"]
        self.log_info(None, OD_log_labels,
                      "OD_log.csv", overwrite=True)

        temp_log_labels = ["Time(ms)", "Temperature", "Raw Temperature",
                           "Temperature IR", "Temperature IR Ambient"]
        self.log_info(None, temp_log_labels,
                      "temp_log.csv", overwrite=True)

        pump_log_labels = ["Time(ms)", "Media OD Sensor", "Media Inlet",
                           "Media Transfer", "Main OD Sensor", "Waster Pump",
                           "Sterilization Input", "Fossil Record Pump", "Main Mixer", "Media Mixer"]
        self.log_info(None, pump_log_labels,
                      "pump_log.csv", overwrite=True)

        heater_log_labels = ["Time(ms)", "Heater Power", "Heater Activation"]
        self.log_info(None, heater_log_labels,
                      "heater_log.csv", overwrite=True)

        target_temp_log_labels = [
            "Time(ms)", "Target Temp", "Target Temp Media", "Target OD"]
        self.log_info(None, target_temp_log_labels,
                      "target_log.csv", overwrite=True)

        self.log_info(None, OD_log_labels,
                      "OD_media_log.csv", overwrite=True)

        self.log_info(None, temp_log_labels,
                      "temp_media_log.csv", overwrite=True)

        self.log_info(None, heater_log_labels,
                      "heater_media_log.csv", overwrite=True)

    def main(self):
        if self._RealTime - self._LastGenericLogTime > self.generic_log_interval * 1000:
            self._LastGenericLogTime = self._RealTime

            if len(self._Pump_times[1:] > 0):
                self.log_info(np.hstack((self._Pump_times[1:].reshape(
                    self._Pump_times.shape[0]-1, 1), self._Pump[:, 1:].T)),
                    [], "pump_log.csv")

            if self._Heater_power_times.shape[0] > 0:
                self.log_info(np.hstack((self._Heater_power_times.reshape(
                    self._Heater_power_times.shape[0], 1), self._HeaterPower.reshape(
                    self._HeaterPower.shape[0], 1), self._HeaterPowerSet.reshape(
                    self._HeaterPowerSet.shape[0], 1))),
                    [], "heater_log.csv")

            if (self._Target_times.shape[0] > 0):
                self.log_info(np.hstack((self._Target_times.reshape(
                    self._Target_times.shape[0], 1), self._Target_temp.reshape(
                    self._Target_temp.shape[0], 1), self._Target_temp_media.reshape(
                    self._Target_temp_media.shape[0], 1), self._Target_OD.reshape(
                    self._Target_OD.shape[0], 1))),
                    [], "target_log.csv")

            if self._Heater_power_times_media.shape[0] > 0:
                self.log_info(np.hstack((self._Heater_power_times_media.reshape(
                    self._Heater_power_times_media.shape[0], 1), self._HeaterPower_media.reshape(
                    self._HeaterPower_media.shape[0], 1), self._HeaterPowerSet_media.reshape(
                    self._HeaterPowerSet_media.shape[0], 1))),
                    [], "heater_media_log.csv")

            self.reset_generic_stores()

        if self._Device is None:
            self.setup
        else:
            # print(self._comm_turn)
            if self._comm_turn:
                self.construct_outbound()
                # print(self._Outbound)
                self.log_info(self._Outbound, [], "comms_log.csv")
                self.send_data()
                self._comm_turn = False
            else:
                self.check_inbound()
                if self._comm_turn:
                    # print(self._Inbound)
                    self.log_info(
                        self._Inbound, [], "comms_log.csv")


if __name__ == '__main__':
    c = Communication()
    time.sleep(2)
    while True:
        c.main()
