//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
//

using System;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using Microsoft.CognitiveServices.Speech.Transcription;

namespace csharp
{
    public class Program
    {
        static string _key = vars.ckey;
        static string _rg = vars.cregion;    
        static string _audiofile = "gettysburg10.wav";

        // It's always a good idea to access services in an async fashion
        static async Task Main()
        {
            // recognize from microphone
            Console.WriteLine("Speech from audio file....");

            // recognize from audio file
            await RecognizeSpeechAsync();

        // recognize from microphone
            Console.WriteLine("Begin speaking....");
            // recognize from Mic
            await RecognizeSpeechByMicAsync();

            //// transcribe feature
            //await TranscribeConversationsAsync(null, null);
            // await TranscribeConversationsAsync(String.Empty, string.Empty);            

            Console.WriteLine("Please press <Return> to continue.");
            Console.ReadLine();
        }

        public static async Task RecognizeSpeechAsync()
        {
            // set config
            var config = SpeechConfig.FromSubscription(_key, _rg); 

            // Setup the audio configuration, in this case, using a file that is in local storage.
            // path to assembly
            string exepath = System.Reflection.Assembly.GetExecutingAssembly().Location;
            string fpath = System.IO.Path.Combine(System.IO.Path.GetDirectoryName(exepath), _audiofile);
            // Console.WriteLine($"path to exe: {exepath}");
            using (var audioInput = AudioConfig.FromWavFileInput(fpath)) //   using (var audioInput = AudioConfig.FromWavFileInput("../../../../media/gettysburg10.wav"))

            // Pass the required parameters to the Speech Service which includes the configuration information
            // and the audio file name that you will use as input
            using (var recognizer = new SpeechRecognizer(config, audioInput))
            {
                Console.WriteLine("Recognizing first result...");
                var result = await recognizer.RecognizeOnceAsync();

                switch (result.Reason)
                {
                    case ResultReason.RecognizedSpeech:
                        // The file contained speech that was recognized and the transcription will be output
                        // to the terminal window
                        Console.WriteLine($"We recognized: {result.Text}");
                        break;
                    case ResultReason.NoMatch:
                        // No recognizable speech found in the audio file that was supplied.
                        // Out an informative message
                        Console.WriteLine($"NOMATCH: Speech could not be recognized.");
                        break;
                    case ResultReason.Canceled:
                        // Operation was cancelled
                        // Output the reason
                        var cancellation = CancellationDetails.FromResult(result);
                        Console.WriteLine($"CANCELED: Reason={cancellation.Reason}");

                        if (cancellation.Reason == CancellationReason.Error)
                        {
                            Console.WriteLine($"CANCELED: ErrorCode={cancellation.ErrorCode}");
                            Console.WriteLine($"CANCELED: ErrorDetails={cancellation.ErrorDetails}");
                            Console.WriteLine($"CANCELED: Did you update the subscription info?");
                        }
                        break;
                }
            }
        }

        public static async Task RecognizeSpeechByMicAsync()
        {
            var config = SpeechConfig.FromSubscription(_key, _rg);

            using (var recognizer = new SpeechRecognizer(config))
            {
                var result = await recognizer.RecognizeOnceAsync();

                if (result.Reason == ResultReason.RecognizedSpeech)
                {
                    Console.WriteLine($"We recognized: {result.Text}");
                }
                else if (result.Reason == ResultReason.NoMatch)
                {
                    Console.WriteLine($"NOMATCH: Speech could not be recognized.");
                }
                else if (result.Reason == ResultReason.Canceled)
                {
                    var cancellation = CancellationDetails.FromResult(result);
                    Console.WriteLine($"CANCELED: Reason={cancellation.Reason}");

                    if (cancellation.Reason == CancellationReason.Error)
                    {
                        Console.WriteLine($"CANCELED: ErrorCode={cancellation.ErrorCode}");
                        Console.WriteLine($"CANCELED: ErrorDetails={cancellation.ErrorDetails}");
                        Console.WriteLine($"CANCELED: Did you update the subscription info?");
                    }
                }
            }
        }

        // public static async Task TranscribeConversationsAsync(string voiceSignatureStringUser1, string voiceSignatureStringUser2)
        // {
        //     var subscriptionKey = vars.ckey;
        //     var region = vars.cregion;
        //     var filepath = "../../../../media/sample-ms1.wav";

        //     var config = SpeechConfig.FromSubscription(subscriptionKey, region);
        //     config.SetProperty("ConversationTranscriptionInRoomAndOnline", "true");

        //     // en-us by default. Adding this code to specify other languages, like zh-cn.
        //     // config.SpeechRecognitionLanguage = "zh-cn";
        //     var stopRecognition = new TaskCompletionSource<int>();

        //     using (var audioInput = AudioConfig.FromWavFileInput(filepath))
        //     {
        //         var meetingID = Guid.NewGuid().ToString();
        //         using (var conversation = await Conversation.CreateConversationAsync(config, meetingID))
        //         {
        //             // create a conversation transcriber using audio stream input
        //             using (var conversationTranscriber = new ConversationTranscriber(audioInput))
        //             {
        //                 conversationTranscriber.Transcribing += (s, e) =>
        //                 {
        //                     Console.WriteLine($"TRANSCRIBING: Text={e.Result.Text} SpeakerId={e.Result.UserId}");
        //                 };

        //                 conversationTranscriber.Transcribed += (s, e) =>
        //                 {
        //                     if (e.Result.Reason == ResultReason.RecognizedSpeech)
        //                     {
        //                         Console.WriteLine($"TRANSCRIBED: Text={e.Result.Text} SpeakerId={e.Result.UserId}");
        //                     }
        //                     else if (e.Result.Reason == ResultReason.NoMatch)
        //                     {
        //                         Console.WriteLine($"NOMATCH: Speech could not be recognized.");
        //                     }
        //                 };

        //                 conversationTranscriber.Canceled += (s, e) =>
        //                 {
        //                     Console.WriteLine($"CANCELED: Reason={e.Reason}");

        //                     if (e.Reason == CancellationReason.Error)
        //                     {
        //                         Console.WriteLine($"CANCELED: ErrorCode={e.ErrorCode}");
        //                         Console.WriteLine($"CANCELED: ErrorDetails={e.ErrorDetails}");
        //                         Console.WriteLine($"CANCELED: Did you update the subscription info?");
        //                         stopRecognition.TrySetResult(0);
        //                     }
        //                 };

        //                 conversationTranscriber.SessionStarted += (s, e) =>
        //                 {
        //                     Console.WriteLine($"\nSession started event. SessionId={e.SessionId}");
        //                 };

        //                 conversationTranscriber.SessionStopped += (s, e) =>
        //                 {
        //                     Console.WriteLine($"\nSession stopped event. SessionId={e.SessionId}");
        //                     Console.WriteLine("\nStop recognition.");
        //                     stopRecognition.TrySetResult(0);
        //                 };

        //                 // here we don't need to identify speakers. we just enable differentiate guest speakers
        //                 config.SetProperty("DifferentiateGuestSpeakers", "true");
                        
        //                 //// Add participants to the conversation.
        //                 //var speaker1 = Participant.From("User1", "en-US", voiceSignatureStringUser1);
        //                 //var speaker2 = Participant.From("User2", "en-US", voiceSignatureStringUser2);
        //                 //await conversation.AddParticipantAsync(speaker1);
        //                 //await conversation.AddParticipantAsync(speaker2);

        //                 // Join to the conversation and start transcribing
        //                 await conversationTranscriber.JoinConversationAsync(conversation);
        //                 await conversationTranscriber.StartTranscribingAsync().ConfigureAwait(false);

        //                 // waits for completion, then stop transcription
        //                 Task.WaitAny(new[] { stopRecognition.Task });
        //                 await conversationTranscriber.StopTranscribingAsync().ConfigureAwait(false);
        //             }
        //         }
        //     }
        // }
    }
}