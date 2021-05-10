## Project

[Full report](Report.pdf)

From the abstract:

>>> Direction of voice (DoV) estimation is a recent development in audio signal processing which can be leveraged to enhance video call experiences such that they more closely resemble natural audio perception. Using some of the methods from recent research in this area, we provide a filtering-based application of DoV estimation to facilitate the transmission of relevant conversation to video call recipients. An extra-trees classifier determines which segments of audio are targeted towards the recording device. A filter blocks audio segments that are projected along irrelevant axes from being transmitted to the wrong audience. Empirically, the proposed work validates this filtering functionality using existing datasets and recordings that were acquired to emulate video call and streaming experiences.

## Implementation and Experiments

### Filtering app

We implemented a filtering app that takes in .wav audio files using librosa and removes the portions of the audio that were recorded when the person speaking was not facing the microphone, using the classifier we trained. Using a Hann window function of varying sizes $\ell$, we take the features from each window and use the 45-to-45 classifier to determine if they are facing (discussion of the 90-to-90 classifier in the subsequent section). If the audio is determined to be "facing" then the audio is concatenated to our output signal; if not, then a zero-signal of the same length ($\ell$) as the audio segment is concatenated instead. The complete implementation is available on Github at [emsal1863/554xproj](https://github.com/emsal1863/554xproj). 

We created speaking-only audio files that consist of portions where the speaker is facing the microphone and where the speaker is not. Some of these are compounds of files from the test portion of the dataset, concatenated togther. In addition, we acquired a ReSpeaker 4-mic array and recorded some audio clips in 4-channel in order to test the classifier on data recorded outside of the original test data. 

The window size is another hyperparameter that was found to have an effect on the quality of the filtering. Experiments were done to examine the properties of changing the window size $\ell$. 

### Experimentation & Results

We tested window sizes 200, 400, 600, 800, and 1000 ms; the script outputs the windows that were classified as facing and not facing, and compared against the ground truth from the audio file. From this we calculated the false positive and false negative classification rates for each case. On the files that are compounds of files from the test dataset, the filtering application performed unilaterally well, usually getting a 100% classification rate. As for the recordings on the ReSpeaker array, there were some on which the classifier performed well and some on which the classifier introduced many false negatives. Across the board, the classifier did always yield a low false positive rate, with the highest rate that could not be explained by an edge case being 2/11. 

There is no quantitatively clear cause for the high false negative rate on the out-of-test-data samples. Differences between the overall cases include the fact that the setup in the room in which the new clips were may have different acoustics; there  

When using the 90-to-90 classifier, however, the classifier introduced a much higher false positive rate, both on files from the test dataset and files from the newly recorded clips; on some of the newly recorded clips, the 90-to-90 classifier unilaterally designated all windows as facing for a 100% false positive rate on all window sizes.

The complete data is available in Table \ref{}.

## Technical details/how to reproduce

Data should be put in a subdirectory `data/`
