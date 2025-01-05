"""
    azure cognitive conversation transcription
"""

import asyncio
import azure.cognitiveservices.speech as speechsdk
import azure.cognitiveservices.speech.speech_py_impl as sdkpy
from common import secrets


class SpeechTranscription():

    async def conversation_transcription(self):
        transconfig = speechsdk.speech_py_impl.SpeechTranslationConfig(secrets.SPEECH_KEY, secrets.SERVICE_REGION)
        audioconfig = speechsdk.AudioConfig(False, secrets.AUDIO_FILENAME)
        transconfig.set_property("ConversationTranscriptionInRoomAndOnline", "True")
        transconfig.speech_recognition_language = "en-US"

        # conversation and transcriber
        meetingid = "vcimeeting"
        conversation = await speechsdk.speech_py_impl.Conversation.create_conversation_async(transconfig, meetingid)
        transcr = speechsdk.speech_py_impl.ConversationTranscriber.from_config(audioconfig)
        await speechsdk.speech_py_impl.ConversationTranscriber.join_conversation_async(transcr, conversation)

        # c-sharp base
        config = speechsdk.SpeechConfig("", secrets.SERVICE_REGION)
        config.set_property("ConversationTranscriptionInRoomAndOnline",  "True")
        config.speech_recognition_language = "en-us"    # default

        with speechsdk.AudioConfig(False, secrets.AUDIO_FILENAME) as audioinput:
            meetingid = "vcimeeting-1"
            async with speechsdk.speech_py_impl.Conversation_create_conversation_async(config, meetingid) as conv:
                with speechsdk.speech_py_impl.ConversationTranscriber(audioinput) as convtr:
                    speechsdk.speech_py_impl.ConversationTranscriber.transcribed += lambda s, e: {
                        # if e.Result.Reason == speechsdk.speech_py_impl.ConversationTranscriber
                    }







