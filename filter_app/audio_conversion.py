from gccphat import gcc_phat
import pandas as pd
import numpy as np
import pickle


COLNAMES = [*[f'gccphat_{i}_{j}_{d}' for i in range(4)
                                     for j in range(i+1, 4)
                                     for d in ['maxshift', 'auc', 'peakval']],
            *[f'gccphatval_{i}_{j}_{k}' for i in range(4)
                                        for j in range(i+1, 4)
                                        for k in range(23)]]

with open('model-1-0.sav', 'rb') as f:
    CLASSIFIER = pickle.load(f)

def _get_featurized_data(frame_signals, fs, max_tau):
    df = pd.DataFrame(columns=COLNAMES)
    data_row = {}
    for i in range(4):
        for j in range(i+1,4):
            gcc_phat_data = gcc_phat(frame_signals[i], frame_signals[j],
                                  fs = fs,
                                  max_tau=max_tau, interp=1)
            data_row[f'gccphat_{i}_{j}_peakval'] = gcc_phat_data[1][11]
            data_row[f'gccphat_{i}_{j}_auc'] = np.sum(gcc_phat_data[1])
            data_row[f'gccphat_{i}_{j}_maxshift'] = gcc_phat_data[0]
            for k in range(23):
                data_row[f'gccphatval_{i}_{j}_{k}'] = gcc_phat_data[1][k]
    df = df.append(data_row, ignore_index=True)
    return df.values

def process_signal(audio_signals, frame_timelen, fs, max_tau):
    frame = True

    sample_len = len(audio_signals[0])
    frame_indexlen = int(fs * frame_timelen)

    hann_window = 0.5 * 1 + np.cos(2 * np.pi * np.arange(sample_len) / frame_indexlen)

    for i in range(4):
        audio_signals[i] = hann_window * audio_signals[i]

    cursor = 0

    full_sig = [ [] for i in range(4) ]

    while cursor <= sample_len - frame_indexlen:
        frame_sig = [ [] for i in range(4) ]
        for i in range(4):
            frame_sig[i] = audio_signals[i][cursor:cursor+frame_indexlen]

        data_featurized = _get_featurized_data(frame_sig, fs, max_tau)

        facing = CLASSIFIER.predict(data_featurized)
        if facing == 1:
            pass
        else:
            frame_sig = [ [0] * frame_indexlen for i in range(4) ]

        for i in range(4):
            full_sig[i] = np.concatenate((full_sig[i], frame_sig[i]), axis=0)
        cursor += frame_indexlen

    return full_sig
