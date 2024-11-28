import json
import os
import shutil
import uuid
from urllib import request

from django.core.management.base import BaseCommand

from core.models import Locale
from core.models.question_answer import UserQuestion
from core.services.files import download_file
from twinby import settings

rus = [
    "Мои идеальные выходные — это…",
    "Моя самая безумная мечта — это…",
    "Две правды и одна ложь обо мне",
    "Свой идеальный день я бы описал(а) так",
    "Фильм, который я готов(а) пересматривать вечно, называется…",
    "Меня можно описать тремя словами",
    "День пройдет ужасно, если я не…",
    "Больше всего в жизни я горжусь, что",
    "Больше всего времени я провожу в…",
    "Свидание моей мечты я вижу так",
]
eng = [
    "My perfect weekend is…",
    "My craziest dream is...",
    "Two truths and one lie about me",
    "I would describe my perfect day as...",
    "The movie I'm willing to re-watch again and again is called...",
    "I can be described in three words as...",
    "The day will go terribly if I don't...",
    "What I'm most proud of in life is...",
    "I spend the most time in...",
    "I imagine my dream date as...",
]
img_url = [
    "https://drive.google.com/file/d/1_efkzmCHrrb8Hlx-xADHc8zH7hz_pLEs/view?usp=drive_link",
    "https://drive.google.com/file/d/1dVBZZRlXHh3paLdv5beHTJg4l_lUkoiM/view?usp=drive_link",
    "https://drive.google.com/file/d/1DwzLNuNzmvMa6pvOTcEDQoSAMW3t4E7F/view?usp=drive_link",
    "https://drive.google.com/file/d/1aadfZEbfPfzLtlxUQxnRLX5z4UDXnRnZ/view?usp=drive_link",
    "https://drive.google.com/file/d/1QaV7UkiyCSMjlC1pFp3LiN_YhK0sU_Ew/view?usp=drive_link",
    "https://drive.google.com/file/d/1-y2hvpY2l5NA98t1Ald1dXVlBsb4tKrM/view?usp=drive_link",
    "https://drive.google.com/file/d/1V1k-MamH3eH65ixP5N0wK_0l96Azeu_Q/view?usp=drive_link",
    "https://drive.google.com/file/d/1nMWDPmCbNbNKyCyxVZo4CXBafj-PWDem/view?usp=drive_link",
    "https://drive.google.com/file/d/1S5Xq27S3FTsHpC-Y-H8jAIM8GqK7r2gi/view?usp=drive_link",
    "https://drive.google.com/file/d/18r0fHIkYhWHN4d5wHtsm_LLaFHWj6Zkj/view?usp=drive_link",
]
question_data = dict(zip(rus, eng))
question_icons = dict(zip(rus, img_url))
import requests

def handle_file(url, name):
    response = requests.get(
        url,
    )
    if response.status_code == requests.codes.ok:
        with open(name, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
            return os.getcwd() + "/" + name


class Command(BaseCommand):
    def handle(self, *args, **options):
        for rus, eng in question_data.items():
            headers = {
                'accept': 'application/json',
                'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNTc1MzQ4LCJqdGkiOiI2ZmI5NWE1ZWRhMmM0YWUxYTk4NThiNGRmZjUzNzc1NCIsInVzZXJfaWQiOjEwMjE5MTgzODIwNjM0ODQ5MzEsInRvdHAiOmZhbHNlLCJzdWIiOiIxMDIxOTE4MzgyMDYzNDg0OTMxIn0.cucTLWIlNBMd6CI_Uvmw43pvzdv5Xmx2Ws0fKSJED_0',
                'X-CSRFToken': 'M0vslfCZMcZgWWqA3LlvcsEQ4L8EtWFH7jyruKGfJlXGtLuSmNYoA1lGUHizceR8',
                "Content-Type": "multipart/form-data"
            }
            filename2 = str(uuid.uuid4())
            with open(handle_file(question_icons[rus],filename2), "rb") as img2:
                camel_data =  {
                    'question_text': rus,
                    "question_translate": json.dumps({"en": eng, "rus": rus}),
                }
                camel_data["icon"] = img2

                response = requests.post(
                            "http://185.141.234.122:8000/api/admin/core/question-answer/", data=camel_data, headers=headers
                        )
                print(response.status_code)
