import librosa
import audio_conversion
import soundfile

FILENAME = "recording0_225_%d.wav"

audio_loads = [ librosa.load(FILENAME % i, sr=None) for i in range(1,5) ]

fs = audio_loads[0][1]
audio_data = [ entry[0] for entry in audio_loads ]
max_tau = 0.236e-3
frame_timelen = 100e-3

new_signals = audio_conversion.process_signal(audio_data,
                                              frame_timelen, fs, max_tau)

soundfile.write('conversion_output_225.wav', new_signals[0], fs)
