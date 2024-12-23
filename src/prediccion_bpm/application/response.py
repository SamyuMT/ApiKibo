from ECGSingal import *


class PrediccionResponse():

    @staticmethod
    def SetPrediccion(data):
        if data:
            segmentNew = escalarVoltaje(data)
            peaks = encontrarCrucePorCero(segmentNew, 125, 0.7)
            T = promedioRR(peaks,125)
            bpm = int(T*100)
            print(bpm)
            return bpm
        else:
            return 0            