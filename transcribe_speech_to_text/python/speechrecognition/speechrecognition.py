"""
    azure cognitive speech recognition

    reference:  azure cognitive services speech sdk

"""
import wave

import azure.cognitiveservices.speech as speechsdk
import time
from transcribe_speech_to_text.python.common import secrets


class SpeechRecognition:
    # Creates an instance of a speech config
    speech_key, service_region = secrets.SPEECH_KEY, secrets.SERVICE_REGION
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    def speech_recognition_continuous_from_file(self, filename):
        """ cognitive speech continuous recognition from file  """
        done = False
        audio_input = speechsdk.AudioConfig(filename=filename)

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)

        print("Recognizing speech...")

        def callback_stop(e):
            print('closing on {}'.format(e))
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
        # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(callback_stop)
        speech_recognizer.canceled.connect(callback_stop)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        speech_recognizer.stop_continuous_recognition()
        print("Recognition completed")

    def speech_recognition_with_pull_stream(self, filename):
        """gives an example how to use a pull audio stream to recognize speech from a custom audio
        source"""

        class WavFileReaderCallback(speechsdk.audio.PullAudioInputStreamCallback):
            """Example class that implements the Pull Audio Stream interface to recognize speech from
            an audio file"""

            def __init__(self, filename2: str):
                super().__init__()
                self._file_h = wave.open(filename2, mode=None)

                self.sample_width = self._file_h.getsampwidth()

                print("channels: {}".format(self._file_h.getnchannels()))
                print("sampwidth: {}".format(self._file_h.getsampwidth()))
                print("framerate: {}".format(self._file_h.getframerate()))

                assert self._file_h.getnchannels() == 1
                assert self._file_h.getsampwidth() == 2
                assert self._file_h.getframerate() == 16000
                assert self._file_h.getcomptype() == 'NONE'

            def read(self, buffer: memoryview) -> int:
                """read callback function"""
                size = buffer.nbytes
                frames = self._file_h.readframes(size // self.sample_width)

                buffer[:len(frames)] = frames

                return len(frames)

            def close(self):
                """close callback function"""
                self._file_h.close()

        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)

        # specify the audio format
        wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16,
                                                        channels=1)

        # setup the audio stream
        callback = WavFileReaderCallback(filename)
        stream = speechsdk.audio.PullAudioInputStream(callback, wave_format)
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        # instantiate the speech recognizer with pull stream input
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False

        def stop_cb(evt):
            """callback that signals to stop continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        while not done:
            time.sleep(.5)

        speech_recognizer.stop_continuous_recognition()

    def speech_recognition_with_push_stream(self, filename):
        """gives an example how to use a push audio stream to recognize speech from a custom audio
        source"""
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)

        # setup the audio stream
        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        # instantiate the speech recognizer with push stream input
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

        # The number of bytes to push per buffer
        n_bytes = 3200
        wav_fh = wave.open(filename)

        print("filename: {}".format(filename))

        # start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # start pushing data until all data has been read from the file
        try:
            while (True):
                frames = wav_fh.readframes(n_bytes // 2)
                # print('read {} bytes'.format(len(frames)))
                if not frames:
                    break

                stream.write(frames)
                time.sleep(.5)
        finally:
            # stop recognition and clean up
            wav_fh.close()
            stream.close()
            speech_recognizer.stop_continuous_recognition()


# # call function
# audio_filename = '../../media/trm1-1.wav'
# stc = SpeechRecognition()
# stc.speech_recognition_continuous_from_file(filename=audio_filename)













