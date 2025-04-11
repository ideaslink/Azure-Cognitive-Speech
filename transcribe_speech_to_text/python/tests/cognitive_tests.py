import unittest
import sys
import os

# Add the parent directory of 'transcribe_speech_to_text' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from speechrecognition.speechrecognition import SpeechRecognition
# transcribe_speech_to_text.python.speechrecognition.speechrecognition import SpeechRecognition
from common import secrets

class CognitiveTests(unittest.TestCase):
    audio_filename = secrets.AUDIO_FILENAME

    def setUp(self) -> None:
        self.stcobj = SpeechRecognition()
        if len(self.audio_filename) == 0:
            self.audio_filename = input("Enter audio file: ")

    def test_speech_continous_fromfile(self):
        """ speech continuous recognition from file """
        self.stcobj.speech_recognition_continuous_from_file(filename=self.audio_filename)
        self.assertTrue(True)

    @unittest.skip
    def test_speech_continuous_pull_stream(self):
        """ speech continuous pull stream """
        self.stcobj.speech_recognition_with_pull_stream(filename=self.audio_filename)

    @unittest.skip
    def test_speech_continuous_push_stream(self):
        """ speech continuous push scream """
        self.stcobj.speech_recognition_with_push_stream(filename=self.audio_filename)

    def tearDown(self) -> None:
        """ prepare to close """
        pass


if __name__ == '__main__':
    unittest.main()
