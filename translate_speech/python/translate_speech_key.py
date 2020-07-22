import azure.cognitiveservices.speech as speechsdk

speech_key, service_region =  "f7b1af1399664520806f4b0724765a40", "eastus"

def translate_speech_to_text():

    # Creates an instance of a speech translation config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)

    # Sets source and target languages.
    # Replace with the languages of your choice, from list found here: https://aka.ms/speech/sttt-languages
    fromLanguage = 'en-US'
    tolanglist = ['zh-Hans', 'fr', 'de']

    toLanguage = 'zh-Hans' # 'fr' # 'de'
    for lng in tolanglist:
        translation_config.add_target_language(lng)
    translation_config.speech_recognition_language = fromLanguage
    # translation_config.add_target_language(toLanguage)

    # Creates a translation recognizer using and audio file as input.
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config)

    # prepare to handle the synthesized audio data.
    def synthesis_callback(evt):
        size = len(evt.result.audio)
        print('AUDIO SYNTHESIZED: {} byte(s) {}'.format(size, '(COMPLETED)' if size == 0 else ''))

    recognizer.synthesizing.connect(synthesis_callback)

    # Starts translation, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognized text as well as the translation.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    print("Say something...")
    result = recognizer.recognize_once()
    # result = recognizer.start_continuous_recognition()

    # Check the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("RECOGNIZED '{}': {}".format(fromLanguage, result.text))
        for lng in tolanglist:
            print("TRANSLATED into {}: {}".format(lng, result.translations[lng]))
        # print("TRANSLATED into {}: {}".format(toLanguage, result.translations[toLanguage]))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("RECOGNIZED: {} (text could not be translated)".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("NOMATCH: Speech could not be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("CANCELED: Reason={}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("CANCELED: ErrorDetails={}".format(result.cancellation_details.error_details))

translate_speech_to_text()