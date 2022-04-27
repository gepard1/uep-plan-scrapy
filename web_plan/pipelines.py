# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pandas as pd
import datetime
import os.path
import re

from itemadapter import ItemAdapter
from os.path import dirname, abspath
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class WebPlanPipeline:
    def process_item(self, item, spider):

        creds = None
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        d = dirname(dirname(abspath(__file__)))

        if os.path.exists(d + "\\token.json"):
            creds = Credentials.from_authorized_user_file(d + "\\token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    d + "\\credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(d + "\\token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds)

        except HttpError as error:
            print("An error occurred: %s" % error)
        del_list = []
        dict_test = {}

        plan_dict = ItemAdapter(item["weekends_dict"]).asdict()
        classes = {k: v for k, v in plan_dict.items() if v}

        for weekend in classes:
            matched = 0
            for line in classes[weekend]:
                match = re.search(r"\d{4}-\d{2}-\d{2}", line)
                if match:
                    matched = 1
            if matched == 0:
                del_list.append(weekend)

        for key_to_delete in del_list:
            del classes[key_to_delete]

        for weekend in classes:
            for line in classes[weekend]:
                match = re.search(r"\d{4}-\d{2}-\d{2}", line)
                if match:
                    date = match.group()
                    dict_test[date] = []
                else:
                    dict_test[date].append(line.split("\r\n"))

        for key in dict_test:
            for lesson in dict_test[key]:

                hours = lesson[0].split("-")

                end_hour = re.search(r"\d{2}:\d{2}", hours[1]).group()

                start = datetime.combine(
                    datetime.strptime(key, "%Y-%m-%d"),
                    datetime.strptime(hours[0], "%H:%M").time(),
                )
                end = datetime.combine(
                    datetime.strptime(key, "%Y-%m-%d"),
                    datetime.strptime(end_hour, "%H:%M").time(),
                )

                event = {
                    "summary": lesson[1],
                    "location": lesson[2],
                    "description": lesson[3],
                    "start": {
                        "dateTime": start.isoformat(),
                        "timeZone": "Europe/Warsaw",
                    },
                    "end": {
                        "dateTime": end.isoformat(),
                        "timeZone": "Europe/Warsaw",
                    },
                }
                event = (
                    service.events().insert(calendarId="primary", body=event).execute()
                )
                print("Event created: %s" % (event.get("htmlLink")))
        return item
