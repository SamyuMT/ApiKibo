from ECGSingal import *


class PrediccionResponse():

    @staticmethod
    def SetPrediccion(data):
        if data:
            segmentNew = escalarVoltaje(data)
            peaks = encontrarCrucePorCero(segmentNew, 125, 0.7)
            T = promedioRR(peaks,125)
            ecg = int(T*100)
            print(ecg)
            return ecg
        else:
            return 0            