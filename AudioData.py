import subprocess
import struct
import numpy as np
import time
import json

def _AudioDataConditioning(AudioData):     #32bit audio daten roh 
    __AudioData = AudioData

    __SignalBlock = struct.unpack('<' + 'i' * (len(__AudioData) // 4), __AudioData) #wandelt daten in 32 bit float audio daten
    __SignalBlock = np.array(__SignalBlock, dtype=np.float32)                       #macht numpy array daraus
    __MaxAmplitude = np.max(np.abs(__SignalBlock))

    if __MaxAmplitude == 0:
        return __SignalBlock
    else:
        __SignalBlock = (__SignalBlock / __MaxAmplitude)*8                         #werte zwischen -10 und 10
        return __SignalBlock


def _FrequencyMagnitudeVectorForPositiveFrequencies(Signal , NumberOfSamples):
    __Window = np.hamming(2048)
    __WindowedSignal = Signal * __Window
    __NumberOfSamples = NumberOfSamples
    
    __AllFrequencyMagnitudes = np.fft.fft(__WindowedSignal) / (__NumberOfSamples/4)
    __FrequencyMagnitudesForPositiveFrequencies = __AllFrequencyMagnitudes[:__NumberOfSamples//2]
    return np.abs(__FrequencyMagnitudesForPositiveFrequencies)


def _PositiveFrequenciesAfterFFT(NumberOfSamples , Samplingrate):
    __NumberOfSamples = NumberOfSamples 
    __Samplingrate = Samplingrate

    __AllFrequencies = np.fft.fftfreq(__NumberOfSamples , 1/__Samplingrate)
    __PositiveFrequencieVector = __AllFrequencies[:__NumberOfSamples//2]
    return __PositiveFrequencieVector


def _Visualizer(PositiveFrequencyVector , PositiveMagnitudeVector):
    __PositiveFrequencyVector = PositiveFrequencyVector
    __PositiveMagnitudeVector = PositiveMagnitudeVector
    
    if np.all(__PositiveMagnitudeVector == 0):
        return [0,0,0,0,0,0,0,0,0,0]
    
    else:
        __FrequencyBands = [(1 , 31.25),            #Bass
                            (31.25 , 62.5),         #Bass
                            (62.5 , 125),           #Bass
                            (125 , 250),            #Mitten
                            (250 , 500),            #Mitten
                            (500 , 1000),           #Mitten
                            (1000 , 2000),          #Mitten
                            (2000 , 4000),          #Höhen
                            (4000 , 8000),          #Höhen
                            (8000 , 23500),         #Höhen
                            (23500, 24000)]         #Pseudo
        __FirstBandValue = 0
        __BandValue = 0
        __ListIndex = 0
        __OutputList = []
        for __idx in range (1, len(__PositiveFrequencyVector)):
            if __PositiveFrequencyVector[__idx] <= __FrequencyBands[__ListIndex][1]:        #höchste magnitude aus jeweilligem 
                __CurrentValue = __PositiveMagnitudeVector[__idx]                           #frequenzband wird der Ausgabeliste
                if __CurrentValue > __BandValue:                                            #zugeordnet und zwischen 0 und 10 konditioniert
                    __BandValue = __CurrentValue
            else:
                if __BandValue <= __FirstBandValue:
                    __BandValue = __FirstBandValue
                __OutputList.append(__BandValue)
                __FirstBandValue = __PositiveMagnitudeVector[__idx]
                __BandValue = 0
                __ListIndex += 1
        __OutputList = [round(__wert) for __wert in __OutputList]
        __OutputList = [min(x, 8) for x in __OutputList]
        return __OutputList

def AudioProgramm():
    from Bluetooth2 import BluetoothConnected , BluetoothProgramm , ShutdownRaspi
    __SamplesPerBlock = 2048
    __BytePerSample = 4
    __SamplingrateInHertz = 48000
 
    #Öffnen des Audiostreams
    __AudioStream = subprocess.Popen(
    ['ffmpeg', '-f', 'pulse', '-i', 'alsa_output.platform-fef00700.hdmi.hdmi-stereo.monitor', '-f', 'wav', '-'], # alsa_output.platform-fe00b840.mailbox.stereo-fallback.monitor
    stdout=subprocess.PIPE)

    #Öffnen der Pipe zum LED Programm
    __LEDPipe = subprocess.Popen(["sudo", "/home/EP/Documents/EP/EP/.venv/bin/python", "/home/EP/Documents/EP/EP/LED.py"],
    stdin=subprocess.PIPE,
    text=True)

    __Counter = 0
    __Time = 0
    __Duration = 15 * 60         # !!!! muss noch auf 15 min gesetzt werden (min * sekunden)
    __StartTimer = time.time()
    while True:
        starttime = time.time()
        if BluetoothConnected() == False:
            print("die Verbindung wurde unterbrochen")
            __AudioStream.terminate()
            __AudioStream.wait()
            BluetoothProgramm()
        
        else:
            __AudioData = __AudioStream.stdout.read(__BytePerSample * __SamplesPerBlock)    #Liest 2048 Samples vom Audiostream (4 Bytes = 32 Bit ist ein Sample)

            if __Counter >= 1:      #Erster Block hat irrelevante Information
                
                if __AudioData:
                    __SignalBlock = _AudioDataConditioning(__AudioData)
                    __OutputList = _Visualizer(
                                _PositiveFrequenciesAfterFFT(__SamplesPerBlock , __SamplingrateInHertz),
                                _FrequencyMagnitudeVectorForPositiveFrequencies(__SignalBlock , __SamplesPerBlock))
                    
                    if __OutputList != [0,0,0,0,0,0,0,0,0,0]:
                        __StartTimer = time.time()
                    else:
                        if (time.time() - __StartTimer) > __Duration:                       #wenn 15 min lang keine Audio abgespielt wird, fährt das System herunter
                            __AudioStream.terminate()
                            __AudioStream.wait()
                            ShutdownRaspi()
                            break
                    
                    __OutputListStr = json.dumps(__OutputList)
                    __LEDPipe.stdin.write(__OutputListStr + "\n")
                    __LEDPipe.stdin.flush()
                    # LEDLightenUp(__OutputList)
                    print(__OutputList)
                    endtime = time.time()
                    oldTime = endtime - starttime
                    __Time += oldTime
                    print(__Time/__Counter)

            __Counter += 1