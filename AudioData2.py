import subprocess 
import threading 
import struct
import numpy as np
import time


def _FrequencyMagnitudeVectorForPositiveFrequencies(Signal , NumberOfSamples):
    #private variables
    __Signal = Signal
    __NumberOfSamples = NumberOfSamples
    
    #method code
    __AllFrequencyMagnitudes = np.fft.fft(__Signal) / __NumberOfSamples
    __FrequencyMagnitudesForPositiveFrequencies = __AllFrequencyMagnitudes[:__NumberOfSamples//2]
    return np.abs(__FrequencyMagnitudesForPositiveFrequencies)



def _PositiveFrequenciesAfterFFT(NumberOfSamples , Samplingrate):
    #private variables
    __NumberOfSamples = NumberOfSamples 
    __Samplingrate = Samplingrate

    #method code
    __AllFrequencies = np.fft.fftfreq(__NumberOfSamples , 1/__Samplingrate)
    __PositiveFrequencieVector = __AllFrequencies[:__NumberOfSamples//2]
    return __PositiveFrequencieVector



def _Visualizer(PositiveFrequencyVector , PositiveMagnitudeVector):
    #private variables
    __PositiveFrequencyVector = PositiveFrequencyVector
    __PositiveMagnitudeVector = PositiveMagnitudeVector
    

    #method code
    if np.isnan(__PositiveMagnitudeVector).any():
        None
    
    else:
        __FrequencyBands = [(1 , 31.25),     
                            (31.25 , 62.5),
                            (62.5 , 125),     
                            (125 , 250),   
                            (250 , 500),  
                            (500 , 1000),
                            (1000 , 2000),
                            (2000 , 4000),
                            (4000 , 8000),
                            (8000 , 20000)]
        __BandValue = 0
        __OutputList = []
        for i, __Band in enumerate(__FrequencyBands):
            for __idx in range(1, len(__PositiveFrequencyVector)):
                if __Band[0] <= __PositiveFrequencyVector[__idx] <= __Band[1]:
                    __CurrentValue = __PositiveMagnitudeVector[__idx]
                    if __CurrentValue > __BandValue:
                        __BandValue = __CurrentValue
                if __PositiveFrequencyVector[__idx] > __Band[1]:
                    break
            __OutputList.append(__BandValue)
            __BandValue = 0
        #OutputList = (OutputList / np.max(OutputList))*10
        __OutputList = [round(__wert) for __wert in __OutputList]
        return __OutputList


AudioStream = subprocess.Popen(
['ffmpeg', '-f', 'pulse', '-i', 'alsa_output.platform-fef05700.hdmi.hdmi-stereo.monitor', '-f', 'wav', '-'],
stdout=subprocess.PIPE,
stderr=subprocess.PIPE)


SamplesPerBlock = 2048
SamplingrateInHertz = 48000
SharedList = []
DataReadyEvent = threading.Event()

def _AudioDataInList():
    global SharedList, DataReadyEvent
    while True:
        startzeit1 = time.time()
        __AudioData = AudioStream.stdout.read(4 * SamplesPerBlock)
        __SignalBlock = struct.unpack('<' + 'i' * (len(__AudioData) // 4), __AudioData)
        __SignalBlock = np.array(__SignalBlock, dtype=np.float32)
        __MaxAmplitude = np.max(np.abs(__SignalBlock))
        if __MaxAmplitude == 0:
            pass
        else:
            __SignalBlock = (__SignalBlock / __MaxAmplitude)*25
        SharedList = __SignalBlock
        DataReadyEvent.set()
        endzeit1 = time.time()
        #print("Aufnahmezeit:", endzeit1 - startzeit1)


def _VerarbeiteListe():
    global SharedList, DataReadyEvent

    while True:

        DataReadyEvent.wait()
        startzeit = time.time()
        __SignalBlock = SharedList

        #calculating outputlist
        __OutputList = _Visualizer(
        _PositiveFrequenciesAfterFFT(SamplesPerBlock , SamplingrateInHertz),
        _FrequencyMagnitudeVectorForPositiveFrequencies(__SignalBlock , SamplesPerBlock))
        print(__OutputList)
        DataReadyEvent.clear()
        endzeit = time.time()
        #print("Verarbeitungszeit: ", endzeit - startzeit)

FüllThread = threading.Thread(target = _AudioDataInList)
FüllThread.daemon = True
FüllThread.start()

VerarbeitungsThread = threading.Thread(target = _VerarbeiteListe)
VerarbeitungsThread.daemon = True
VerarbeitungsThread.start()

while True:
    pass


    


