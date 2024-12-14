from ECGSingal import *

def SegmentarPorRPeacksPrediccion(model1D, peak,segmento,segmentLength):
    label_to_number = {
    'V': 0,
    '!': 1,
    'F': 2,
    'f': 3,
    'N': 4,
    }
    number_to_label = {v: k for k, v in label_to_number.items()}
    sampleSegment = 187
    startT = peak
    endT = startT + segmentLength
    # Asegurarse de que endT no exceda el límite de la señal
    if endT > len(segmento):
        endT = len(segmento)
        startT = endT - segmentLength
    segmentoT = np.pad(segmento[startT:endT], (0, max(0, sampleSegment   - len(segmento[startT:endT]))), mode='constant')
    if len(segmentoT) >= sampleSegment:
        segmentoT = segmentoT[:sampleSegment]
    #predecir con modelo
    SegmentoPredecir = segmento1D(segmentoT)
    SegmentoPredecir = np.expand_dims(SegmentoPredecir, axis=0)
    symbolPrediccion = predecir1D(model1D,SegmentoPredecir)
    symbolPrediccion = int(symbolPrediccion[0])  # Convierte el primer elemento a int
    etiqueta = number_to_label[symbolPrediccion]
    print(etiqueta)
    return etiqueta



class PrediccionResponse():

    @staticmethod
    def SetPrediccion(data, model):
        if data:
            segmentNew = escalarVoltaje(data)
            peaks = encontrarCrucePorCero(segmentNew, 125, 0.7)
            T = promedioRR(peaks,125)
            segmentLength = int(1.2 * T * 125)  # Longitud del segmento en muestras Revisar
            for peak in peaks:
                listaSegmento = SegmentarPorRPeacksPrediccion(model, peak, segmentNew, segmentLength)
            return 1
        else:
            return 0            