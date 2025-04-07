import subprocess
import struct
import numpy as np
import time

def ShutdownRaspi():
    subprocess.run(["sudo","shutdown"], check = True)

def _AudioDataConditioning(AudioData):     #32bit audi0 codec 
    #private variables
    __AudioData = AudioData

    #method code
    __SignalBlock = struct.unpack('<' + 'i' * (len(__AudioData) // 4), __AudioData)
    __SignalBlock = np.array(__SignalBlock, dtype=np.float32)
    __MaxAmplitude = np.max(np.abs(__SignalBlock))
    #empty signalblock
    if __MaxAmplitude == 0:
        return __SignalBlock
    #full signalblock
    else:
        __SignalBlock = (__SignalBlock / __MaxAmplitude)*22
        return __SignalBlock



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
    if np.all(__PositiveMagnitudeVector == 0):
        return [0,0,0,0,0,0,0,0,0]
    
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
                            (8000 , 24000)]         #Höhen
        __FirstBandValue = 0
        __BandValue = 0
        __ListIndex = 0
        __OutputList = []
        for __idx in range (1, len(__PositiveFrequencyVector)):
            if __PositiveFrequencyVector[__idx] <= __FrequencyBands[__ListIndex][1]:
                __CurrentValue = __PositiveMagnitudeVector[__idx]
                if __CurrentValue > __BandValue:
                    __BandValue = __CurrentValue
            else:
                if __BandValue <= __FirstBandValue:
                    __BandValue = __FirstBandValue
                __OutputList.append(__BandValue)
                __FirstBandValue = __PositiveMagnitudeVector[__idx]
                __BandValue = 0
                __ListIndex += 1
        #__OutputList = (__OutputList / np.max(__OutputList))*10
        __OutputList = [round(__wert) for __wert in __OutputList]
        return __OutputList


            

        #__BandValue = 0
        #__OutputList = []
        #for i, __Band in enumerate(__FrequencyBands):
         #   for __idx in range(1, len(__PositiveFrequencyVector)):
          #      if __Band[0] <= __PositiveFrequencyVector[__idx] <= __Band[1]:
           #         __CurrentValue = __PositiveMagnitudeVector[__idx]
            #        if __CurrentValue > __BandValue:
             #           __BandValue = __CurrentValue
            #__OutputList.append(__BandValue)
            #__BandValue = 0
        #OutputList = (OutputList / np.max(OutputList))*10
        #__OutputList = [round(__wert) for __wert in __OutputList]
        #return __OutputList
    


def AudioProgramm():
    from Bluetooth2 import BluetoothConnected , BluetoothProgramm
    from LED import LEDLightenUp
    __SamplesPerBlock = 2048
    __BytePerSample = 4
    __SamplingrateInHertz = 48000

    #opens the audio stream 

    __AudioStream = subprocess.Popen(
    ['ffmpeg', '-f', 'pulse', '-i', 'alsa_output.platform-fe00b840.mailbox.stereo-fallback.monitor', '-f', 'wav', '-'], # alsa_output.platform-fef00700.hdmi.hdmi-stereo.monitor
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)

    #processes the audio stream
    __Counter = 0
    __ShutdownCounter = 0
    Time = 0
    while True:
        starttime = time.time()
        if BluetoothConnected() == False:
            print("die Verbindung wurde unterbrochen")
            __AudioStream.terminate()
            __AudioStream.wait()
            BluetoothProgramm()
        
        else:
            #reads 2048 Samples from the audio stream (4 Bytes = 32 Bit is one Sample)
            __AudioData = __AudioStream.stdout.read(__BytePerSample * __SamplesPerBlock)

            #first block has irellevant information
            if __Counter >= 1:
                
                #actual programm
                if __AudioData:
                    __SignalBlock = _AudioDataConditioning(__AudioData)
                    __OutputList = _Visualizer(
                                _PositiveFrequenciesAfterFFT(__SamplesPerBlock , __SamplingrateInHertz),
                                _FrequencyMagnitudeVectorForPositiveFrequencies(__SignalBlock , __SamplesPerBlock))
                    if __OutputList != [0,0,0,0,0,0,0,0,0]:
                        __ShutdownCounter = 0
                    else:
                        __ShutdownCounter += 1
                        if __ShutdownCounter > 7000:
                            ShutdownRaspi()
                    
                    subprocess.run(["sudo", "python3", "/home/EP/Documents/Projekt/LED.py"])
                    # LEDLightenUp(__OutputList)
                    print(__OutputList)
                    endtime = time.time()
                    oldTime = endtime - starttime
                    Time += oldTime
                    # print(Time/__Counter)


                else:
                    print("keine Audio Daten")

                #__Counter -= 1

            __Counter += 1
            #print(__Counter)