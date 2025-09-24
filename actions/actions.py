from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProvidePrecaution(Action):

    def name(self):
        return "action_provide_precaution"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        disease = next(tracker.get_latest_entity_values("disease"), None)

        if not disease:
            dispatcher.utter_message(response="utter_ask_disease")
            return []

        # Precaution data
        precautions = {
            "malaria": {
                "en": "Malaria Precautions:\n1. Consult nearest hospital 🏥\n2. Avoid oily food 🍔\n3. Avoid outside food 🚫\n4. Keep hydrated 💧",
                "hi": "मलेरिया से बचाव:\n1. निकटतम अस्पताल से परामर्श करें 🏥\n2. तैलीय भोजन से बचें 🍔\n3. बाहर का खाना न खाएं 🚫\n4. हाइड्रेटेड रहें 💧"
            },
            "diabetes": {
                "en": "Diabetes Precautions:\n1. Regular exercise 🏃\n2. Eat a balanced diet 🥗\n3. Monitor blood sugar 🩸\n4. Avoid excess sugar 🍬",
                "hi": "डायबिटीज़ से बचाव:\n1. नियमित व्यायाम करें 🏃\n2. संतुलित आहार लें 🥗\n3. ब्लड शुगर की जांच करते रहें 🩸\n4. अधिक शक्कर से बचें 🍬"
            },
            "मलेरिया": {
                "en": "Malaria Precautions:\n1. Consult nearest hospital 🏥\n2. Avoid oily food 🍔\n3. Avoid outside food 🚫\n4. Keep hydrated 💧",
                "hi": "मलेरिया से बचाव:\n1. निकटतम अस्पताल से परामर्श करें 🏥\n2. तैलीय भोजन से बचें 🍔\n3. बाहर का खाना न खाएं 🚫\n4. हाइड्रेटेड रहें 💧"
            },
            "डायबिटीज़": {
                "en": "Diabetes Precautions:\n1. Regular exercise 🏃\n2. Eat a balanced diet 🥗\n3. Monitor blood sugar 🩸\n4. Avoid excess sugar 🍬",
                "hi": "डायबिटीज़ से बचाव:\n1. नियमित व्यायाम करें 🏃\n2. संतुलित आहार लें 🥗\n3. ब्लड शुगर की जांच करते रहें 🩸\n4. अधिक शक्कर से बचें 🍬"
            }
        }

        # Detect language automatically
        lang = "hi" if any('\u0900' <= c <= '\u097F' for c in disease) else "en"
        response = precautions.get(disease, {}).get(lang, "I don't have data for this disease yet.")

        dispatcher.utter_message(text=response)
        return []
