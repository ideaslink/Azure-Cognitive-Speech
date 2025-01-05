"""
    azure cognitive speech recognition
"""

import azure.cognitiveservices.speech as speechsdk
import time
import secrets


class SpeechRecognition:
    # Creates an instance of a speech config
    speech_key, service_region = secrets.SPEECH_KEY, secrets.SERVICE_REGION
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # audio_filename = "../../media/narration.wav"
    # audio_filename = "../../media/trm1-5.wav"

    def speech_text_continuous_from_file(self, filename):
        isdone = False
        audio_input = speechsdk.AudioConfig(filename=filename)

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)

        print("Recognizing speech...")

        def callback_stop(e):
            print('closing on {}'.format(e))
            nonlocal isdone
            isdone = True

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
        while not isdone:
            time.sleep(.5)

        speech_recognizer.stop_continuous_recognition()
        print("Recognition completed")


# call function
audio_filename = '../../media/trm1-2.wav'
stc = SpeechRecognition()
stc.speech_text_continuous_from_file(filename=audio_filename)












