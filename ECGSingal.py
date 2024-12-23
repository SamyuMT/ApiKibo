import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import scipy.signal as signal
from scipy.signal import find_peaks
import pandas as pd
import os
import wfdb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import pickle
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Input, Dense,GlobalAveragePooling2D , Dropout, Flatten, LSTM
from tensorflow.keras.layers import Conv1D, MaxPooling1D, BatchNormalization
from tensorflow.keras.layers import concatenate
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import pywt
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import MobileNetV2




def butterBandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpassFilter(data, lowcut, highcut, fs, order=5):
    b, a = butterBandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def printPlot(signal,t,annSample,annSymbol,fs,start,end, segment,r,n=0):
    # Graficar el segmento
    plt.figure(figsize=(15, 5))
    plt.plot(t, signal,'b', label='Filtrada', alpha=0.5)
    plt.plot(t[r], signal[r], 'ro', label='Picos R detectados')

    # Añadir anotaciones
    for j in range(len(annSample)):
        if start <= annSample[j] < end:
            plt.axvline(x=(annSample[j]) / fs, color='r', linestyle='--')
            plt.text((annSample[j]) / fs, max(signal), annSymbol[j], color='r')
    if len(signal) > 538:
        plt.title(f'Señal ECG - Segmento {segment+1}')
    else:
        plt.title(f'Señal ECG - Segmento {segment+1} muestra {n+1}')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud [mV]')
    plt.legend()
    plt.show()

def escalarVoltaje(signal): # Paso numero 2
    vmax = max(signal)
    vmin = min(signal)
    almacenar = []
    for dato in signal:
        almacenar.append((dato - vmin) / (vmax - vmin))
    signalNew = np.array([], dtype=np.float64)
    signalNew = np.append(signalNew, almacenar)
    return signalNew

def encontrarCrucePorCero(signal, fs, u): # Paso numero 3
    # Detectar picos en la señal filtrada
    distance = int(u * fs)  # Aproximadamente la distancia mínima entre picos R
    peaks, _ = find_peaks(signal, distance=distance, height=np.mean(signal))
    return peaks

def promedioRR(r,fs):
    # Calcular las diferencias entre picos consecutivos
    rrIntervals = np.diff(r) / fs  # Convertir a segundos
    mediaRR = np.mean(rrIntervals)  # Promedio de los intervalos RR
    return mediaRR

def SegmentarPorPartes(parte,segmento,signal,fs,annSample,annSymbol,hab,u):
    start = parte * segmento
    end = start + segmento
    segmentFilter = signal[start:end]
    segmentNew = escalarVoltaje(segmentFilter)
    # Crear el eje de tiempo para el segmento actual
    t = np.arange(start, end) / fs
    rPeaks = encontrarCrucePorCero(segmentNew, fs, u)
    T = promedioRR(rPeaks,fs)
    if hab != 0:
        print(f'Para el segmento {parte} el promedio Intervalo R-R: {T} s')
        print(f'tamaño del vector de 10 segundo es: {len(segmentNew)} muestras')
        printPlot(segmentNew,t,annSample,annSymbol,fs,start,end,parte,rPeaks)
    return start,end,segmentNew,T,rPeaks

def etiquetar(Sample,start,end,symbol,hab):
    priority = {'!': 1, 'F': 2, 'f': 3, 'V': 4, 'N': 5, 'O': 6}
    SymbolList = []
    selected_char = 'O'
    selected_priority = priority['O']
    for j in range(len(Sample)):
        if start <= Sample[j] < end:
            SymbolList.append(symbol[j])

    for char in SymbolList:
        if char in priority and priority[char] < selected_priority:
            selected_char = char
            selected_priority = priority[char]
    if hab != 0:
        print(selected_char)
    return selected_char
            

def SegmentarPorRPeacks(peak,segmentAnnSample,segmentAnnSymbol,segmentNew,segmentLength,hab,fs,n,partes):
    listaSegmento = []
    startT = peak
    endT = startT + segmentLength
    rP = 0
    # Asegurarse de que endT no exceda el límite de la señal
    if endT > len(segmentNew):
        endT = len(segmentNew)
        startT = endT - segmentLength
        rP = peak - startT
    # Ajustar el rango de índice para el segmento
    if fs == 125:
        sampleSegment = 187
    else:
        sampleSegment = 538
    segmentoT = np.pad(segmentNew[startT:endT], (0, max(0, sampleSegment   - len(segmentNew[startT:endT]))), mode='constant')
    if len(segmentoT) >= sampleSegment:
        segmentoT = segmentoT[:sampleSegment]
    tT = np.arange(startT, startT+sampleSegment) / fs
    for sample in segmentoT:
        listaSegmento.append(sample)
    symbol = etiquetar(segmentAnnSample,startT,endT,segmentAnnSymbol,hab)
    listaSegmento.append(symbol) #ETIQUETAR
    if hab != 0:
        print(f'tamaño del vector de 1.2T segundos es: {len(segmentoT)} muestras')
        print(listaSegmento)
        print(len(listaSegmento))
        printPlot(segmentoT,tT,segmentAnnSample,segmentAnnSymbol,fs,startT,endT,partes,rP,n)
    return listaSegmento


def SegmentarPorRPeacksConPrediccion(model1D, peak,segmentAnnSample,segmentAnnSymbol,segmentNew,segmentLength,hab,fs,n,partes):
    label_to_number = {
    'V': 0,
    '!': 1,
    'F': 2,
    'f': 3,
    'N': 4,
    'O': 5
    }
    number_to_label = {v: k for k, v in label_to_number.items()}

    listaSegmento = []
    startT = peak
    endT = startT + segmentLength
    rP = 0
    # Asegurarse de que endT no exceda el límite de la señal
    if endT > len(segmentNew):
        endT = len(segmentNew)
        startT = endT - segmentLength
        rP = peak - startT
    # Ajustar el rango de índice para el segmento
    if fs == 125:
        sampleSegment = 187
    else:
        sampleSegment = 538
    segmentoT = np.pad(segmentNew[startT:endT], (0, max(0, sampleSegment   - len(segmentNew[startT:endT]))), mode='constant')
    if len(segmentoT) >= sampleSegment:
        segmentoT = segmentoT[:sampleSegment]
    tT = np.arange(startT, startT+sampleSegment) / fs
    for sample in segmentoT:
        listaSegmento.append(sample)
    symbol = etiquetar(segmentAnnSample,startT,endT,segmentAnnSymbol,hab)
    listaSegmento.append(symbol) #ETIQUETAR
    #predecir con modelo
    SegmentoPredecir = segmento1D(segmentoT)
    SegmentoPredecir = np.expand_dims(SegmentoPredecir, axis=0)
    symbolPrediccion = predecir1D(model1D,SegmentoPredecir)
    symbolPrediccion = int(symbolPrediccion[0])  # Convierte el primer elemento a int
    etiqueta = number_to_label[symbolPrediccion]
    listaSegmento.append(etiqueta) #ETIQUETAR
    print(symbol, etiqueta)
    if hab != 0:
        print(f'tamaño del vector de 1.2T segundos es: {len(segmentoT)} muestras')
        print(listaSegmento)
        print(len(listaSegmento))
        printPlot(segmentoT,tT,segmentAnnSample,segmentAnnSymbol,fs,startT,endT,partes,rP,n)
    return listaSegmento


def SegmentarConPrediccion(model1D, duration,fs,signal,annSample, annSymbol,prueba=0,hab=0,c=1.2,u=0.7): ## Paso numero 1
    segmento = duration * fs
    if prueba == 0:
        numSegments = len(signal) // segmento
    else:
        numSegments = prueba
    n = 0
    matriz = []
    for i in range(numSegments):
        start,end,segmentNew,T,rPeaks = SegmentarPorPartes(i,segmento,signal,fs,annSample,annSymbol,hab,u)
        segmentLength = int(c * T * fs)  # Longitud del segmento en muestras Revisar
        # Ajustar anotaciones para el segmento actual
        mask = (annSample >= start) & (annSample < end)
        segmentAnnSample = annSample[mask] - start  # Restar 'start' para alinear con el segmento
        segmentAnnSymbol = np.array(annSymbol)[mask]  # Filtrar las anotaciones correspondientes
        for peak in rPeaks:
            listaSegmento = SegmentarPorRPeacksConPrediccion(model1D,peak,segmentAnnSample,segmentAnnSymbol,segmentNew,segmentLength,hab,fs,n,i)
            n += 1
            matriz.append(listaSegmento)
    print(f'Total de filas extraidas: {n}')
    return matriz

def Segmentar(duration,fs,signal,annSample, annSymbol,prueba=0,hab=0,c=1.2,u=0.7): ## Paso numero 1
    segmento = duration * fs
    if prueba == 0:
        numSegments = len(signal) // segmento
    else:
        numSegments = prueba
    n = 0
    matriz = []
    for i in range(numSegments):
        start,end,segmentNew,T,rPeaks = SegmentarPorPartes(i,segmento,signal,fs,annSample,annSymbol,hab,u)
        T = T if T == T else 0.89  # Usamos T != T para detectar nan
        segmentLength = int(c * T * fs)  # Longitud del segmento en muestras Revisar
        # Ajustar anotaciones para el segmento actual
        mask = (annSample >= start) & (annSample < end)
        segmentAnnSample = annSample[mask] - start  # Restar 'start' para alinear con el segmento
        segmentAnnSymbol = np.array(annSymbol)[mask]  # Filtrar las anotaciones correspondientes
        for peak in rPeaks:
            listaSegmento = SegmentarPorRPeacks(peak,segmentAnnSample,segmentAnnSymbol,segmentNew,segmentLength,hab,fs,n,i)
            n += 1
            matriz.append(listaSegmento)
    print(f'Total de filas extraidas: {n}')
    return matriz

def ajustarMuestreo(fsNew,fsOriginal,sign,annSample):
    # Paso 1: Filtro anti-aliasing antes del submuestreo
    nyquistRate = fsNew / 2.0
    b, a = signal.butter(4, nyquistRate / (fsOriginal / 2), btype='low')
    signalFiltered = signal.filtfilt(b, a, sign)
    # Paso 2: Submuestreo de la señal
    nSamples = int(len(signalFiltered) * fsNew / fsOriginal)
    signalNew = signal.resample(sign, nSamples)
    # Convertir los índices originales de las etiquetas a tiempos
    timesOriginal = annSample / fsOriginal
    # Convertir los tiempos a los nuevos índices basados en la tasa de muestreo rescalada
    annSampleNew = np.round(timesOriginal * fsNew).astype(int)
    return signalNew, annSampleNew

def cargarVector(path):
    # Leer el registro y las anotaciones
    record = wfdb.rdrecord(path)
    annotation = wfdb.rdann(path, 'atr')
    # Obtener la señal y las anotaciones
    signalOriginal = record.p_signal[:, 0]  # Tomamos solo una de las derivaciones
    annSample = annotation.sample
    annSymbol = annotation.symbol
    fsOriginal = record.fs  # Frecuencia de muestreo original
    return signalOriginal,annSample, annSymbol, fsOriginal

def crearDataFrame(sign,lowcut,highcut,fs,duration,annSample,annSymbol,prueba,hab,c,u):
    # Segmentar la señal original
    filteredSignal = bandpassFilter(sign, lowcut, highcut, fs, order=1)
    matriz = Segmentar(duration, fs, filteredSignal, annSample, annSymbol, prueba,hab,c,u)
    max_size = max(len(lista) for lista in matriz)
    # Rellenar con NaN las listas que tienen menos elementos que max_sizeOriginal
    for lista in matriz:
        while len(lista) < max_size:
            lista.append(np.nan)
    # Convertir a DataFrame
    df = pd.DataFrame(np.array(matriz))
    return df

def procesarArchivo(indice, fsNew=125, duration=10, prueba=0,hab=0,c=1.2,u=0.7, namepath='archivosCSV'):
    # Ruta a los archivos del MIT-BIH Arrhythmia Database
    basePath = 'mit-bih-arrhythmia-database-1.0.0/'
    recordName = f'{basePath}{indice}'
    signalOriginal, annSampleOriginal, annSymbol, fsOriginal = cargarVector(recordName)
    signalNew, annSampleNew = ajustarMuestreo(fsNew,fsOriginal,signalOriginal,annSampleOriginal)
    # Definir los parámetros de corte del filtro
    lowcut = 0.5
    highcut = 50.0
    # Segmentar la señal original
    dfOriginal = crearDataFrame(signalOriginal,lowcut,highcut,fsOriginal,duration,annSampleOriginal,annSymbol,prueba,hab,c,u)
    dfNew = crearDataFrame(signalNew,lowcut,highcut,fsNew,duration,annSampleNew,annSymbol,prueba,hab,c,u)
    # Crear la carpeta para los archivos CSV si no existe
    os.makedirs(namepath, exist_ok=True)
    # Guardar los DataFrames en archivos CSV
    dfOriginal.to_csv(f'{namepath}/arrhythmia{indice}-{fsOriginal}.csv', index=False)
    dfNew.to_csv(f'{namepath}/arrhythmia{indice}-{fsNew}.csv', index=False)
    print('Se guardaron correctamente los archivos')

def augmentData(df, target_size):
    # Crear una lista para almacenar los vectores aumentados
    augmented_vectors = df.iloc[:, :187].values.tolist()  # Extraer los vectores originales
    current_size = len(augmented_vectors)
    
    while current_size < target_size:
        # Seleccionar aleatoriamente un vector y aplicar ruido para aumentar
        random_vector = df.sample(n=1).iloc[:, :187].values.flatten()
        noise = np.random.normal(0, 0.01, size=random_vector.shape)  # Ruido gaussiano
        augmented_vector = random_vector + noise
        augmented_vector = np.clip(augmented_vector, a_min=0, a_max=None)
        augmented_vectors.append(augmented_vector)
        current_size += 1
    
    # Crear un DataFrame con los vectores aumentados
    augmented_df = pd.DataFrame(augmented_vectors, columns=df.columns[:187])
    # Añadir la etiqueta a los vectores aumentados
    augmented_df[df.columns[187]] = df.iloc[0, 187]
    
    return augmented_df

def separarData(maxSignal,labels,df,random=None):
    # Crear un diccionario para almacenar los dataframes separados
    separated_dfs = {}
    # Iterar sobre cada etiqueta
    for label in labels.keys():
        # Filtrar el DataFrame por la etiqueta actual
        label_number = labels[label]
        df_label = df[df.iloc[:, 187] == label_number]
        # Comprobar el número de señales en la etiqueta
        num_signals = len(df_label)
        if num_signals > maxSignal:
            # Si hay más de 2000 señales, seleccionar 2000 de forma aleatoria
            df_label = df_label.sample(n=maxSignal, random_state=random)
        else:
            # Aumentar los datos si hay menos de 2000 señales
            df_label = augmentData(df_label, maxSignal)
        # Guardar el DataFrame resultante en el diccionario con el nombre df_{etiqueta}
        separated_dfs[f'df_{label}'] = df_label
    # Mostrar los tamaños de los dataframes generados para verificación
    for key, df in separated_dfs.items():
        print(f"{key}: {len(df)} filas")
    return separated_dfs

def guardarDataSegmentadaInTrainVal(df,maxSignal,labels,testVal,path,random=None):
    separated_dfs = separarData(maxSignal,labels,df,random)
    # Combinar todos los dataframes en separated_dfs en un solo dataframe
    dataSegmentada = pd.concat(separated_dfs.values(), ignore_index=True)

    # Mostrar el tamaño del nuevo dataframe para verificación
    print(f"dataSegmentada: {len(dataSegmentada)} filas y {len(dataSegmentada.columns)} columnas")
        # Separar características (X) y etiquetas (y)
    X = dataSegmentada.iloc[:, :-1]  # Características (vectores)
    y = dataSegmentada.iloc[:, -1]   # Etiquetas
    # Dividir el dataframe en entrenamiento y validación con estratificación
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=testVal, stratify=y, random_state=random)
    train_df = pd.concat([X_train, y_train], axis=1)
    val_df = pd.concat([X_val, y_val], axis=1)
    # Opcional: Guardar los DataFrames en archivos CSV
    train_df.to_csv(f'train_df_{path}.csv', index=False)
    val_df.to_csv(f'val_df_{path}.csv', index=False)
    # Contar el número de vectores por etiqueta en el DataFrame de entrenamiento
    label_counts = train_df.iloc[:, -1].value_counts()

    # Mostrar el conteo de vectores por etiqueta
    print("Número de vectores por etiqueta en train_df:")
    print(label_counts)
    # Contar el número de vectores por etiqueta en el DataFrame de entrenamiento
    label_counts = val_df.iloc[:, -1].value_counts()

    # Mostrar el conteo de vectores por etiqueta
    print("Número de vectores por etiqueta en train_df:")
    print(label_counts)

def modificarDfTrainVal(dfTrain,dfVal,etiquetas,path):
    # Cargar los DataFrames originales desde los archivos CSV
    train_df = pd.read_csv(dfTrain)
    val_df = pd.read_csv(dfVal)

    # Filtrar las filas donde la última columna no contiene las etiquetas especificadas
    train_df = train_df[~train_df.iloc[:, -1].isin(etiquetas)]
    val_df = val_df[~val_df.iloc[:, -1].isin(etiquetas)]

    # Guardar los DataFrames modificados con el nombre especificado en el path
    train_df.to_csv(f"train_df_{path}.csv", index=False)
    val_df.to_csv(f"val_df_{path}.csv", index=False)

def unirEtiquetas(df,newEtiqueta):
    df.iloc[:, -1] = newEtiqueta  
    return df

def unirDf(df1,df2):
    df = pd.concat([df1,df2], ignore_index=True)
    return df

def imprimirSignalDf(labels,df):
    # Seleccionar una muestra de cada etiqueta para graficar
    samples = {}
    for label, number in labels.items():
        samples[label] = df[df.iloc[:, 187] == number].iloc[0, :187].values.astype('float64')
    # Crear los subplots
    fig, axes = plt.subplots(3, 2, figsize=(10, 15))  # 2 filas, 3 columnas
    axes = axes.flatten()

    # Plotear cada señal en un subplot
    for i, (label, vector) in enumerate(samples.items()):
        axes[i].plot(vector,'b')
        axes[i].set_title(f'Etiqueta: {label}')
        axes[i].set_xlabel('Muestras')
        axes[i].set_ylabel('Amplitud')
        axes[i].set_xticks([0,50,100,150])

    # Ajustar el layout
    plt.tight_layout()
    plt.show()

def create_phase_diagram(vector):
    # Crear vectores desplazados
    phase_diagram = np.vstack((vector[:-1], vector[1:])).T
    return phase_diagram

def dataPhase(pathTrain,pathVal):
    train_df = pd.read_csv(pathTrain)
    val_df = pd.read_csv(pathVal)
    # Separar características y etiquetas para el conjunto de entrenamiento
    X_train = train_df.iloc[:, :-1].values  # Todas las filas, todas las columnas menos la última
    y_train = train_df.iloc[:, -1].values   # Todas las filas, solo la última columna

    # Separar características y etiquetas para el conjunto de validación
    X_val = val_df.iloc[:, :-1].values      # Todas las filas, todas las columnas menos la última
    y_val = val_df.iloc[:, -1].values       # Todas las filas, solo la última columna

    X_train_phase = np.array([create_phase_diagram(x) for x in X_train], dtype=np.float32)
    X_val_phase = np.array([create_phase_diagram(x) for x in X_val], dtype=np.float32)
    y_train = np.array(y_train, dtype=np.int32)
    y_val = np.array(y_val, dtype=np.int32)

    return X_train_phase,y_train,X_val_phase,y_val


def head(numFilters, numKernelSize,input, mul):
    conv1 = Conv1D(filters=numFilters[0]*mul, kernel_size=numKernelSize[0], activation='relu')(input)
    pool1 = MaxPooling1D(pool_size=2)(conv1)
    norm1 = BatchNormalization()(pool1)
    drop1 = Dropout(0.5)(norm1)

    conv1_1 = Conv1D(filters=numFilters[1]*mul, kernel_size=numKernelSize[1], activation='relu')(drop1)
    pool1_1 = MaxPooling1D(pool_size=2)(conv1_1)
    norm1_1 = BatchNormalization()(pool1_1)
    drop1_1 = Dropout(0.5)(norm1_1)

    conv1_2 = Conv1D(filters=numFilters[2]*mul, kernel_size=numKernelSize[2], activation='relu')(drop1_1)
    pool1_2 = MaxPooling1D(pool_size=2)(conv1_2)
    norm1_2 = BatchNormalization()(pool1_2)
    drop1_2 = Dropout(0.5)(norm1_2)

    # Capa LSTM
    lstm1 = LSTM(100, return_sequences=True)(drop1_2)
    lstm1_1 = LSTM(100)(lstm1)
    flat1 = Flatten()(lstm1_1)
    return flat1


def CrearModelo(X, clases = 6, numFilters=[64,128,256], numKernelSize=[3,5,10], multiplicadores = [1,2,3]):
    # Desactivar el modo eager para evitar problemas con TensorArray y LSTM
    tf.config.run_functions_eagerly(False)

    inputs1 = Input(shape=(X.shape[1], X.shape[2]))
    inputs2 = Input(shape=(X.shape[1], X.shape[2]))
    inputs3 = Input(shape=(X.shape[1], X.shape[2]))

    # Head 1
    flat1 = head(numFilters, numKernelSize, inputs1, multiplicadores[0])
    # Head 2
    flat2 = head(numFilters, numKernelSize, inputs2, multiplicadores[1])
    # Head 3
    flat3 = head(numFilters, numKernelSize, inputs3, multiplicadores[2])
    # Merge
    merged = concatenate([flat1, flat2, flat3])
    # Interpretación
    dense1 = Dense(100, activation='relu')(merged)
    outputs = Dense(clases, activation='softmax')(dense1)
    # Modelo final
    cnn_model = Model(inputs=[inputs1, inputs2, inputs3], outputs=outputs)
    # Compilación del modelo
    cnn_model.summary()
    cnn_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return cnn_model

def imprimirReporte(history):
    # Graficar la precisión del entrenamiento y la validación
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Accuracy (Train)')
    plt.plot(history.history['val_accuracy'], label='Accuracy (Validation)')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Accuracy')

    # Graficar la pérdida del entrenamiento y la validación
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Loss (Train)')
    plt.plot(history.history['val_loss'], label='Loss (Validation)')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Loss')

    plt.tight_layout


def predecir1D(model,X):
    # Hacer predicciones usando el modelo
    y_pred_uno = model.predict([X, X, X])
    # Convertir las predicciones en las clases con la mayor probabilidad
    yPrediccion = np.argmax(y_pred_uno, axis=1)
    return yPrediccion

def cargarModelo(path):
    model = load_model(path)
    return model

def segmento1D(segmento):
    x = np.array(create_phase_diagram(segmento), dtype=np.float32)
    return x


def matrixConfusion(yReal,yPred,labels):
    # Crear la matriz de confusión
    conf_matrix = confusion_matrix(yReal, yPred)
    # Mostrar la matriz de confusión
    print("Matriz de Confusión:")
    print(conf_matrix)
    # Visualizar la matriz de confusión
    vis_matriz = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=labels)
    vis_matriz.plot(cmap=plt.cm.Blues)
    plt.show()

def reporteMetricas(yReal,yPred,clases):
    # Imprimir un reporte de clasificación
    report = classification_report(yReal, yPred, target_names=[f'Clase {i}' for i in range(clases)])

    # Mostrar el reporte
    print("Reporte de Clasificación:")
    print(report)

def entrenarModeloGuardarlo1D(pathTrain, pathVal, batch_size, epochs, pathSave,labels = ['V', '!', 'F', 'f', 'N', 'O'], clases = 6, numFilters=[64,128,256], numKernelSize=[3,5,10], multiplicadores = [1,2,3]):
    X_train_phase,y_train,X_val_phase,y_val = dataPhase(pathTrain, pathVal)
    print(X_train_phase.shape)
    model = CrearModelo(X_train_phase, clases, numFilters, numKernelSize, multiplicadores)
    # Convertir etiquetas a formato categórico (one-hot encoding)
    y_train_hot = to_categorical(y_train, num_classes=clases)
    y_val_hot = to_categorical(y_val, num_classes=clases)
    history = model.fit([X_train_phase,X_train_phase,X_train_phase], y_train_hot, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=([X_val_phase,X_val_phase,X_val_phase],y_val_hot),shuffle=True)
    imprimirReporte(history)
    # Guardar el historial en un archivo
    with open(f'{pathSave}.pkl', 'wb') as file:
        pickle.dump(history.history, file)
    model.save(f'{pathSave}.h5')
    # Guardar el modelo en el formato nativo de Keras
    model.save(f'{pathSave}.keras')

    yPred = predecir1D(model,X_val_phase)
    matrixConfusion(y_val,yPred,labels)
    reporteMetricas(y_val,yPred,clases)

def createGaus4(vector):
    wavelet = 'gaus4'
    coefficients, _ = pywt.cwt(vector, np.arange(1, 188), wavelet)
    return coefficients

def createPhase2D(vector):
    length = len(vector)
    phase_diagram_2d = np.zeros((length, length))
    for i in range(length):
        if i < length:
            phase_diagram_2d[i, :length - i] = vector[i:]
    return phase_diagram_2d

def createCmor(vector):
    wavelet = 'cmor0.5-1.0'
    coefficients, _ = pywt.cwt(vector, np.arange(1, 188), wavelet)
    return coefficients

def datagaus(X_train, X_val):
    xTrains = np.array([createGaus4(x) for x in X_train], dtype=np.float32)
    xVal = np.array([createGaus4(x) for x in X_val], dtype=np.float32)
    xTrains1 = np.expand_dims(xTrains, axis=-1)
    xVal1 = np.expand_dims(xVal, axis=-1)
    return xTrains1,xVal1


def datacmor(X_train, X_val):
    xTrains = np.array([createCmor(x) for x in X_train], dtype=np.float32)
    xVal = np.array([createCmor(x) for x in X_val], dtype=np.float32)
    xTrains1 = np.expand_dims(xTrains, axis=-1)
    xVal1 = np.expand_dims(xVal, axis=-1)
    return xTrains1,xVal1

def dataphase2D(X_train, X_val):
    xTrains = np.array([createPhase2D(x) for x in X_train], dtype=np.float32)
    xVal = np.array([createPhase2D(x) for x in X_val], dtype=np.float32)
    xTrains1 = np.expand_dims(xTrains, axis=-1)
    xVal1 = np.expand_dims(xVal, axis=-1)
    return xTrains1,xVal1

def data2D(pathTrain, pathVal, tipo):
    train_df = pd.read_csv(pathTrain)
    val_df = pd.read_csv(pathVal)
    X_train = train_df.iloc[:, :-1].values  # Todas las filas, todas las columnas menos la última
    y_train = train_df.iloc[:, -1].values   # Todas las filas, solo la última columna

    # Separar características y etiquetas para el conjunto de validación
    X_val = val_df.iloc[:, :-1].values      # Todas las filas, todas las columnas menos la última
    y_val = val_df.iloc[:, -1].values       # Todas las filas, solo la última columna
    y_train = np.array(y_train, dtype=np.int32)
    y_val = np.array(y_val, dtype=np.int32)

    if tipo == 'phase':
        x_train, x_val = dataphase2D(X_train, X_val)
    elif tipo == 'gaus':
        x_train, x_val = datagaus(X_train, X_val)
    elif tipo == 'cmor':
        x_train, x_val = datacmor(X_train, X_val)
    else:
        print('Ese tipo no existe')
    
    return x_train, y_train, x_val, y_val

def preprocessImages(images):
    resized_images = tf.image.resize(images, (224, 224))
    rgb_images = tf.image.grayscale_to_rgb(resized_images)
    return rgb_images

def VGG16Model(clases=6):
    vgg16_base = VGG16(input_shape=(224, 224, 3),
                    include_top=False,  # No incluir las capas densas superiores
                    weights='imagenet')

    # Congelar las capas de VGG16
    vgg16_base.trainable = False
    # Definir el modelo
    model_VGG16 = Sequential([
        vgg16_base,
        Flatten(),  # Aplanar las salidas para la capa densa
        Dense(128, activation='relu'),  # Capa densamente conectada
        Dense(clases, activation='softmax')  # Capa de salida con 6 clases
    ])
    # Compilar el modelo
    model_VGG16.summary()
    model_VGG16.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return model_VGG16

def mobilNetModel(clases=6):
    mobilenetv2_base = MobileNetV2(input_shape=(224, 224, 3),
                                include_top=False,
                                weights='imagenet')
    # Congelar las capas de MobileNetV2
    mobilenetv2_base.trainable = False
    # Definir el modelo
    model_mobilenet = Sequential([
        mobilenetv2_base,
        GlobalAveragePooling2D(),
        Flatten(),  # Aplanar las salidas para la capa densa
        Dense(128, activation='relu'),  # Capa densamente conectada
        Dense(clases, activation='softmax')
    ])
    model_mobilenet.summary()
    model_mobilenet.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return model_mobilenet


def predecir2D(model,X):
    # Hacer predicciones usando el modelo
    y_pred_uno = model.predict(X)
    # Convertir las predicciones en las clases con la mayor probabilidad
    yPrediccion = np.argmax(y_pred_uno, axis=1)
    return yPrediccion

def entrenarModeloGuardar2D(pathTrain, pathVal, batchSize, epocas, pathSave,tranferencia = 0, tipo = 'phase' ,labels = ['V', '!', 'F', 'f', 'N', 'O'], clases = 6):
    xTrain,y_train,xVall,y_val = data2D(pathTrain, pathVal, tipo)
    X_train = preprocessImages(xTrain)
    X_val = preprocessImages(xVall)
    if tranferencia == 0:
        model = VGG16Model(clases)
    else:
        model = mobilNetModel(clases)

    history = model.fit(X_train, y_train,
                    validation_data=(X_val, y_val),
                    epochs=epocas,
                    batch_size=batchSize)
    imprimirReporte(history)
    # Guardar el historial en un archivo
    with open(f'{pathSave}.pkl', 'wb') as file:
        pickle.dump(history.history, file)
    model.save(f'{pathSave}.h5')
    # Guardar el modelo en el formato nativo de Keras
    model.save(f'{pathSave}.keras')
    yPred = predecir2D(model,X_val)
    matrixConfusion(y_val,yPred,labels)
    reporteMetricas(y_val,yPred,clases) 


