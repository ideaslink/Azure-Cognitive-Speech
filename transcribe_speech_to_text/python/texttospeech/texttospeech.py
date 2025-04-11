"""
azure cognitive service - speech to text
"""

import azure.cognitiveservices.speech as speechsdk
from common import secrets

class TextToSpeech:
    """
    Test to speech 
    """

    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = secrets.SPEECH_KEY, secrets.SERVICE_REGION
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # uncomment this line to change the voice used for synthesis
    # speech_config.speech_synthesis_voice_name = "en-CA-Linda"

    def text_to_speech(self, text: str):
        """ text to speech """
        # Creates a speech synthesizer using the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

        # Receives a text from console input.
        if len(text) == 0:
            text = input("\nType some text that you want to speak...\n")

        # Synthesizes the received text to speech.
        # The synthesized speech is expected to be heard on the speaker with this line executed.
        result = speech_synthesizer.speak_text_async(text).get()

        # Checks result.
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized to speaker for text [{text}]")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(f"Error details: {cancellation_details.error_details}")
            print("Did you update the subscription info?")
