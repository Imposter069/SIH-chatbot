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
            # ✅ Already present
            "malaria": {
                "en": "Malaria Precautions:\n1. Consult nearest hospital 🏥\n2. Avoid oily food 🍔\n3. Avoid outside food 🚫\n4. Keep hydrated 💧",
                "hi": "मलेरिया से बचाव:\n1. निकटतम अस्पताल से परामर्श करें 🏥\n2. तैलीय भोजन से बचें 🍔\n3. बाहर का खाना न खाएं 🚫\n4. हाइड्रेटेड रहें 💧"
            },
            "diabetes": {
                "en": "Diabetes Precautions:\n1. Regular exercise 🏃\n2. Eat a balanced diet 🥗\n3. Monitor blood sugar 🩸\n4. Avoid excess sugar 🍬",
                "hi": "डायबिटीज़ से बचाव:\n1. नियमित व्यायाम करें 🏃\n2. संतुलित आहार लें 🥗\n3. ब्लड शुगर की जांच करते रहें 🩸\n4. अधिक शक्कर से बचें 🍬"
            },

            # ✅ Extended 40+ diseases
            "asthma": {
                "en": "Asthma Precautions:\n1. Avoid dust and smoke 🚭\n2. Always carry inhaler 💊\n3. Avoid cold weather ❄️\n4. Do breathing exercises 🧘",
                "hi": "अस्थमा से बचाव:\n1. धूल और धुएं से बचें 🚭\n2. हमेशा इनहेलर रखें 💊\n3. ठंडे मौसम से बचें ❄️\n4. श्वास व्यायाम करें 🧘"
            },
            "typhoid": {
                "en": "Typhoid Precautions:\n1. Drink boiled water 💧\n2. Avoid street food 🚫\n3. Complete antibiotics course 💊\n4. Maintain hygiene 🧼",
                "hi": "टाइफाइड से बचाव:\n1. उबला हुआ पानी पिएं 💧\n2. सड़क का खाना न खाएं 🚫\n3. एंटीबायोटिक कोर्स पूरा करें 💊\n4. स्वच्छता बनाए रखें 🧼"
            },
            "dengue": {
                "en": "Dengue Precautions:\n1. Use mosquito nets 🦟\n2. Wear full sleeve clothes 👕\n3. Avoid stagnant water 🚱\n4. Keep hydrated 💧",
                "hi": "डेंगू से बचाव:\n1. मच्छरदानी का प्रयोग करें 🦟\n2. फुल स्लीव कपड़े पहनें 👕\n3. रुका हुआ पानी न रखें 🚱\n4. हाइड्रेटेड रहें 💧"
            },
            "covid": {
                "en": "COVID-19 Precautions:\n1. Wear a mask 😷\n2. Wash hands frequently 🧼\n3. Maintain social distance ↔️\n4. Get vaccinated 💉",
                "hi": "कोविड-19 से बचाव:\n1. मास्क पहनें 😷\n2. बार-बार हाथ धोएं 🧼\n3. सामाजिक दूरी बनाए रखें ↔️\n4. टीकाकरण करवाएं 💉"
            },
            "hypertension": {
                "en": "Hypertension Precautions:\n1. Reduce salt intake 🧂\n2. Exercise daily 🏃\n3. Avoid stress 😌\n4. Regular BP checkup 💉",
                "hi": "हाई ब्लड प्रेशर से बचाव:\n1. नमक का सेवन कम करें 🧂\n2. रोज़ व्यायाम करें 🏃\n3. तनाव से दूर रहें 😌\n4. नियमित बीपी जांच करें 💉"
            },
            "tuberculosis": {
                "en": "Tuberculosis Precautions:\n1. Cover mouth while coughing 😷\n2. Take full medicine course 💊\n3. Eat healthy food 🥗\n4. Get regular checkups 🏥",
                "hi": "टीबी से बचाव:\n1. खांसते समय मुंह ढकें 😷\n2. दवा का पूरा कोर्स लें 💊\n3. पौष्टिक भोजन करें 🥗\n4. नियमित जांच करवाएं 🏥"
            },
            "pneumonia": {
                "en": "Pneumonia Precautions:\n1. Get vaccinated 💉\n2. Keep warm 🧥\n3. Avoid smoking 🚭\n4. Drink fluids 💧",
                "hi": "निमोनिया से बचाव:\n1. टीकाकरण करवाएं 💉\n2. गर्म कपड़े पहनें 🧥\n3. धूम्रपान से बचें 🚭\n4. तरल पदार्थ पिएं 💧"
            },
            "hepatitis": {
                "en": "Hepatitis Precautions:\n1. Avoid alcohol 🚫🍺\n2. Get vaccinated 💉\n3. Wash hands before meals 🧼\n4. Avoid contaminated food 🚫",
                "hi": "हेपेटाइटिस से बचाव:\n1. शराब से बचें 🚫🍺\n2. टीकाकरण करवाएं 💉\n3. भोजन से पहले हाथ धोएं 🧼\n4. दूषित भोजन से बचें 🚫"
            },
            "jaundice": {
                "en": "Jaundice Precautions:\n1. Drink boiled water 💧\n2. Avoid oily food 🍔\n3. Take complete rest 🛌\n4. Consult doctor 🏥",
                "hi": "पीलिया से बचाव:\n1. उबला हुआ पानी पिएं 💧\n2. तैलीय भोजन से बचें 🍔\n3. पूरा आराम करें 🛌\n4. डॉक्टर से परामर्श करें 🏥"
            },
            "anemia": {
                "en": "Anemia Precautions:\n1. Eat iron-rich food 🥬\n2. Take folic acid supplements 💊\n3. Avoid junk food 🍔\n4. Regular checkups 🩸",
                "hi": "एनीमिया से बचाव:\n1. आयरन युक्त भोजन करें 🥬\n2. फोलिक एसिड सप्लीमेंट लें 💊\n3. जंक फूड से बचें 🍔\n4. नियमित जांच करवाएं 🩸"
            },
            "migraine": {
                "en": "Migraine Precautions:\n1. Avoid loud noise 🔊\n2. Sleep properly 🛌\n3. Avoid stress 😌\n4. Take medicines on time 💊",
                "hi": "माइग्रेन से बचाव:\n1. तेज आवाज से बचें 🔊\n2. पर्याप्त नींद लें 🛌\n3. तनाव से बचें 😌\n4. समय पर दवा लें 💊"
            },
            "chickenpox": {
                "en": "Chickenpox Precautions:\n1. Isolate the patient 🛌\n2. Maintain hygiene 🧼\n3. Do not scratch blisters 🚫\n4. Take rest 😴",
                "hi": "चेचक से बचाव:\n1. रोगी को अलग रखें 🛌\n2. स्वच्छता बनाए रखें 🧼\n3. फोड़े न खुजलाएं 🚫\n4. आराम करें 😴"
            },
            "cholera": {
                "en": "Cholera Precautions:\n1. Drink safe water 💧\n2. Maintain hand hygiene 🧼\n3. Avoid street food 🚫\n4. ORS solution intake 🥤",
                "hi": "हैजा से बचाव:\n1. सुरक्षित पानी पिएं 💧\n2. हाथ धोएं 🧼\n3. सड़क का खाना न खाएं 🚫\n4. ओआरएस पिएं 🥤"
            },
            "arthritis": {
                "en": "Arthritis Precautions:\n1. Do regular exercise 🏃\n2. Maintain healthy weight ⚖️\n3. Avoid stress on joints 🦵\n4. Take medicines timely 💊",
                "hi": "गठिया से बचाव:\n1. नियमित व्यायाम करें 🏃\n2. वजन नियंत्रित रखें ⚖️\n3. जोड़ों पर जोर न डालें 🦵\n4. समय पर दवा लें 💊"
            },
            "kidney stone": {
                "en": "Kidney Stone Precautions:\n1. Drink plenty of water 💧\n2. Avoid salty food 🧂\n3. Limit protein intake 🍖\n4. Avoid junk food 🚫",
                "hi": "किडनी स्टोन से बचाव:\n1. खूब पानी पिएं 💧\n2. नमक कम खाएं 🧂\n3. प्रोटीन सीमित लें 🍖\n4. जंक फूड से बचें 🚫"
            },
            "cancer": {
                "en": "Cancer Precautions:\n1. Avoid smoking 🚭\n2. Eat healthy diet 🥗\n3. Go for regular screening 🏥\n4. Stay active 🏃",
                "hi": "कैंसर से बचाव:\n1. धूम्रपान न करें 🚭\n2. संतुलित आहार लें 🥗\n3. नियमित जांच करवाएं 🏥\n4. सक्रिय रहें 🏃"
            },
            "obesity": {
                "en": "Obesity Precautions:\n1. Exercise regularly 🏃\n2. Eat low-fat diet 🥗\n3. Avoid junk food 🍔\n4. Monitor weight ⚖️",
                "hi": "मोटापा से बचाव:\n1. नियमित व्यायाम करें 🏃\n2. कम वसा वाला भोजन करें 🥗\n3. जंक फूड से बचें 🍔\n4. वजन नियंत्रित रखें ⚖️"
            },
            "depression": {
                "en": "Depression Precautions:\n1. Talk to family/friends 🗣️\n2. Do meditation 🧘\n3. Exercise daily 🏃\n4. Take professional help 🏥",
                "hi": "अवसाद से बचाव:\n1. परिवार/दोस्तों से बात करें 🗣️\n2. ध्यान करें 🧘\n3. रोज़ व्यायाम करें 🏃\n4. विशेषज्ञ से मदद लें 🏥"
            },
            "gastritis": {
                "en": "Gastritis Precautions:\n1. Avoid spicy food 🌶️\n2. Eat on time ⏰\n3. Limit alcohol 🚫🍺\n4. Take medicines properly 💊",
                "hi": "गैस्ट्राइटिस से बचाव:\n1. मसालेदार भोजन से बचें 🌶️\n2. समय पर खाना खाएं ⏰\n3. शराब से बचें 🚫🍺\n4. दवा समय पर लें 💊"
            },
            "stroke": {
                "en": "Stroke Precautions:\n1. Control BP & sugar 🩸\n2. Avoid smoking 🚭\n3. Exercise daily 🏃\n4. Eat healthy diet 🥗",
                "hi": "स्ट्रोक से बचाव:\n1. बीपी और शुगर नियंत्रित रखें 🩸\n2. धूम्रपान से बचें 🚭\n3. नियमित व्यायाम करें 🏃\n4. स्वस्थ आहार लें 🥗"
            },
            "flu": {
                "en": "Flu Precautions:\n1. Wash hands regularly 🧼\n2. Avoid crowded places 🚫\n3. Cover mouth while coughing 😷\n4. Stay hydrated 💧",
                "hi": "फ्लू से बचाव:\n1. हाथ धोते रहें 🧼\n2. भीड़ से बचें 🚫\n3. खांसते समय मुंह ढकें 😷\n4. पानी अधिक पिएं 💧"
            },
            "allergy": {
                "en": "Allergy Precautions:\n1. Avoid allergens 🚫\n2. Keep environment clean 🧹\n3. Take prescribed medicine 💊\n4. Consult doctor 🏥",
                "hi": "एलर्जी से बचाव:\n1. एलर्जन से दूर रहें 🚫\n2. वातावरण साफ रखें 🧹\n3. डॉक्टर की बताई दवा लें 💊\n4. डॉक्टर से परामर्श करें 🏥"
            },
            "thyroid": {
                "en": "Thyroid Precautions:\n1. Take medicine regularly 💊\n2. Avoid junk food 🚫\n3. Regular checkups 🏥\n4. Eat iodine rich food 🧂",
                "hi": "थायराइड से बचाव:\n1. दवा नियमित लें 💊\n2. जंक फूड से बचें 🚫\n3. नियमित जांच करवाएं 🏥\n4. आयोडीन युक्त भोजन करें 🧂"
            },
            "ulcer": {
                "en": "Ulcer Precautions:\n1. Avoid spicy food 🌶️\n2. Don’t skip meals 🍽️\n3. Limit alcohol 🚫🍺\n4. Take medicines on time 💊",
                "hi": "अल्सर से बचाव:\n1. मसालेदार भोजन से बचें 🌶️\n2. खाना न छोड़ें 🍽️\n3. शराब से बचें 🚫🍺\n4. समय पर दवा लें 💊"
            },
            "epilepsy": {
                "en": "Epilepsy Precautions:\n1. Take medicines daily 💊\n2. Avoid lack of sleep 🛌\n3. Stay away from bright lights 💡\n4. Inform friends/family 🗣️",
                "hi": "मिर्गी से बचाव:\n1. रोज़ दवा लें 💊\n2. नींद पूरी करें 🛌\n3. तेज रोशनी से बचें 💡\n4. परिवार/दोस्तों को जानकारी दें 🗣️"
            },
            "skin infection": {
                "en": "Skin Infection Precautions:\n1. Keep skin clean 🧼\n2. Avoid sharing towels 🚫\n3. Use prescribed creams 💊\n4. Maintain hygiene 🧴",
                "hi": "त्वचा संक्रमण से बचाव:\n1. त्वचा साफ रखें 🧼\n2. तौलिया साझा न करें 🚫\n3. डॉक्टर की दवा लगाएं 💊\n4. स्वच्छता रखें 🧴"
            },
            "eye flu": {
                "en": "Eye Flu Precautions:\n1. Avoid touching eyes ✋\n2. Use clean tissues 🧻\n3. Do not share handkerchief 🚫\n4. Wash eyes with clean water 💧",
                "hi": "आई फ्लू से बचाव:\n1. आंखों को न छुएं ✋\n2. साफ टिश्यू का उपयोग करें 🧻\n3. रुमाल साझा न करें 🚫\n4. साफ पानी से आंखें धोएं 💧"
            },
            "heart disease": {
                "en": "Heart Disease Precautions:\n1. Avoid smoking 🚭\n2. Eat low cholesterol food 🥗\n3. Exercise daily 🏃\n4. Manage stress 😌",
                "hi": "हृदय रोग से बचाव:\n1. धूम्रपान से बचें 🚭\n2. कम कोलेस्ट्रॉल वाला भोजन करें 🥗\n3. रोज़ व्यायाम करें 🏃\n4. तनाव नियंत्रित करें 😌"
            },
            "malnutrition": {
                "en": "Malnutrition Precautions:\n1. Eat balanced diet 🥗\n2. Include vitamins & minerals 🍎\n3. Avoid junk food 🚫\n4. Regular health checkups 🏥",
                "hi": "कुपोषण से बचाव:\n1. संतुलित आहार लें 🥗\n2. विटामिन और खनिज शामिल करें 🍎\n3. जंक फूड से बचें 🚫\n4. नियमित जांच करवाएं 🏥"
            },
            "polio": {
                "en": "Polio Precautions:\n1. Vaccinate children 💉\n2. Maintain hygiene 🧼\n3. Drink clean water 💧\n4. Avoid contaminated food 🚫",
                "hi": "पोलियो से बचाव:\n1. बच्चों का टीकाकरण करवाएं 💉\n2. स्वच्छता रखें 🧼\n3. साफ पानी पिएं 💧\n4. दूषित भोजन से बचें 🚫"
            },
            "swine flu": {
                "en": "Swine Flu Precautions:\n1. Wear mask 😷\n2. Avoid crowded places 🚫\n3. Wash hands regularly 🧼\n4. Get medical help 🏥",
                "hi": "स्वाइन फ्लू से बचाव:\n1. मास्क पहनें 😷\n2. भीड़ से बचें 🚫\n3. हाथ धोते रहें 🧼\
