# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from underthesea import ner
from pprint import pprint


class ActionAskPoint(Action):

    def name(self) -> Text:
        return "action_ask_point"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_message = (tracker.latest_message)['text']
        pprint(ner(last_message))
        dispatcher.utter_message(text=last_message)
        return []

class ActionGraduationAskTime(Action):
    def name(self) -> Text:
        return "action_graduation_ask_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_message = (tracker.latest_message)['text']
        pprint(ner(last_message))
        dispatcher.utter_message(text=last_message)
        return []



