import os

from distutils.util import strtobool

coreAppDir = os.getcwd()
dummyFilesRelativePath = "EndUserManagement/dummyData/files"
dummyFilesStoragePath = os.path.join(coreAppDir, dummyFilesRelativePath)

dummyCases = {
    "Ali": [],
    "Eduard": [
        {
            "Coverage": "HOUSEHOLD",
            "Description": "I arrived to Chisinau on x/x/2024 after our house in Kharkiv was bombarded by the Russian army. My father passed away" \
            "int eh hospital and together with my mother and sister we sought refuge in Moldova. We need a place to stay, clothes, food and some cash" \
            "to survive. My mother is pregnant and needs medical assistance as well. We don't speak Romanian and don't know where to get assistance.",
            "Status": "OPEN",
            "CaseTypes": ["Cash assistance", "Shelter support", "Health support", "NFI support"],
            "PsnTypes": ["Pregnant woman"],
            "File": [
                os.path.join(dummyFilesStoragePath, "Dummy_Case_Document.pdf"),
                os.path.join(dummyFilesStoragePath, "Dummy_Case_Image.png")
            ],
            "VoiceRecording": [
                os.path.join(dummyFilesStoragePath, "Dummy_Case_Voice_Recording.mp3")
            ],
            "Messages": [
                {
                    "TextMessage": "Hello",
                    "HasMedia": False,
                    "SenderRole": "User"
                },
                {
                    "TextMessage": "Hi. How can I help you?",
                    "HasMedia": False,
                    "SenderRole": "Case Supporter"
                },
                {
                    "TextMessage": "Can you examine this document about my case?",
                    "HasMedia": True,
                    "SenderRole": "User",
                    "File": [
                        os.path.join(dummyFilesStoragePath, "Dummy_Message_Document.pdf")
                    ]
                },
                {
                    "TextMessage": "I will check it out. Thanks",
                    "HasMedia": False,
                    "SenderRole": "Case Supporter"
                },
                {
                    "TextMessage": None,
                    "HasMedia": True,
                    "SenderRole": "User",
                    "VoiceRecording": [
                        os.path.join(dummyFilesStoragePath, "Dummy_Message_Voice_Recording.mp3")
                    ]
                }
            ]
        }
    ],
    "Dilshad": [
        {
            "Coverage": "INDIVIDUAL",
            "Description": "I was living in Tehran and had a boyfriend. He suggested that we get married and we elude from the houses of our parents." \
            "I believed him and run away from my parents' house. We tried to go to Turkiye but in the border the police officers called our parents." \
            "My family came and took me. I was held captive at home for 4 months until I could find an opportunity to escape from the beating and threats" \
            "of my father. Through a smuggler I arrived the Iraq, I got registered. A week ago I learned that my family found where I am living and I" \
            "continue to receive threats from them. I am afraid of my life every second. I need help.",
            "Status": "OPEN",
            "CaseTypes": ["Protection from violence", "Legal support"],
            "PsnTypes": []
        }
    ]
}

def getDummyCases():
    return dummyCases
