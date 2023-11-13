from Communication_class import *
from GUI.guiRoot import *

fossilRecordConnected = False
if fossilRecordConnected:
    from robotArm import *


fossilInterval = 30
lastFossilSample = time.time()

if __name__ == "__main__":
    comm_handler = Communication()
    testObj = windows(comm_handler)
    if fossilRecordConnected:
        fossilRecord = FRecord()
    time.sleep(2)

    loopsPerDataRefresh = 50000
    i = 0
    while True:
        comm_handler.main()
        testObj.update_idletasks()
        testObj.update()
        testObj.update_data_every()
        if i > loopsPerDataRefresh:
            testObj.update_data()
            i = 0
        i += 1
        if not fossilRecordConnected:
            continue
        fossilRecord.ArmMovement()
        if fossilRecord.pumpFossilSample:
            if not comm_handler._pumps_on_delay[fossilRecord.activePump]:
                comm_handler._pumps_on_delay[fossilRecord.activePump] = True
                comm_handler._pump_delay_time = fossilRecord.pumpTime
                comm_handler.set_Status(5)
            else:
                if comm_handler._Pump[fossilRecord.activePump, -1] == 0:
                    fossilRecord.pumpFossilSample = False
                    comm_handler._pumps_on_delay[fossilRecord.activePump] = False
        elif fossilRecord.armReady() and time.time() - lastFossilSample > fossilInterval:
            fossilRecord.TriggerRecord()
            lastFossilSample = time.time()
