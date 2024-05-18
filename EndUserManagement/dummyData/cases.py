import os

from distutils.util import strtobool

dummyCases = {
    "Sadiq": [
        {
            "Description": "I am living inside the UN refugee camp in the north of Baghdat, near the city border."\
            "I live with my wife and 3 kids in the tent number 13. I believe that there are not enough hygiene products"\
            "inside the daily supplies box they give us. I think we need more soap and shampoo as a family. I am attaching"\
            "the contents of the box as a photo to this request. I would be very happy if you take care about this problem."\
            "Thank you!",
            "Status": "OPEN"
        },
        {
            "Description": "Hello. My friend Salahaddin also lives in the UN refugee camp in the North of Baghdat."\
            "He has a problem but he does not have a smartphone and he can only speak Arabic. We are attaching his"\
            "voice recording to this request. Thank you for reading this message.",
            "Status": "CW ASSIGNED"
        },
        {
            "Description": "I am living inside the UN refugee camp in the north of Baghdat, near the city border."\
            "I live with my wife and 3 kids in the tent number 13. My mom and dad lives inside the tent next to me"\
            "but my dad needs a wheelchair. Can you provide us a wheelchair? Thank you.",
            "Status": "ON PROGRESS"
        }
    ],
    "Latimah": [
        {
            "Description": "My English bad. I record sound. Thanks.",
            "Status": "OPEN"
        }
    ],
    "Mandla": [],
    "Mohammad": [],
    "Yousef": []
}

def getDummyCases():
    return dummyCases
