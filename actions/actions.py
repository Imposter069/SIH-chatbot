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
                "hi": "स्वाइन फ्लू से बचाव:\n1. मास्क पहनें 😷\n2. भीड़ से बचें 🚫\n3. हाथ धोते रहें 🧼\n4. चिकित्सकीय मदद लें 🏥"
            },
            "अस्थमा": {
               "en": "Asthma Precautions:\n1. Avoid dust and smoke 🚭\n2. Always carry inhaler 💊\n3. Avoid cold weather ❄️\n4. Do breathing exercises 🧘",
     "hi": "अस्थमा से बचाव:\n1. धूल और धुएं से बचें 🚭\n2. हमेशा इनहेलर रखें 💊\n3. ठंडे मौसम से बचें ❄️\n4. श्वास व्यायाम करें 🧘"
},
"टाइफाइड": {
    "en": "Typhoid Precautions:\n1. Drink boiled water 💧\n2. Avoid street food 🚫\n3. Complete antibiotics course 💊\n4. Maintain hygiene 🧼",
    "hi": "टाइफाइड से बचाव:\n1. उबला हुआ पानी पिएं 💧\n2. सड़क का खाना न खाएं 🚫\n3. एंटीबायोटिक कोर्स पूरा करें 💊\n4. स्वच्छता बनाए रखें 🧼"
},
"डेंगू": {
    "en": "Dengue Precautions:\n1. Use mosquito nets 🦟\n2. Wear full sleeve clothes 👕\n3. Avoid stagnant water 🚱\n4. Keep hydrated 💧",
    "hi": "डेंगू से बचाव:\n1. मच्छरदानी का प्रयोग करें 🦟\n2. फुल स्लीव कपड़े पहनें 👕\n3. रुका हुआ पानी न रखें 🚱\n4. हाइड्रेटेड रहें 💧"
},
"कोविड-19": {
    "en": "COVID-19 Precautions:\n1. Wear a mask 😷\n2. Wash hands frequently 🧼\n3. Maintain social distance ↔️\n4. Get vaccinated 💉",
    "hi": "कोविड-19 से बचाव:\n1. मास्क पहनें 😷\n2. बार-बार हाथ धोएं 🧼\n3. सामाजिक दूरी बनाए रखें ↔️\n4. टीकाकरण करवाएं 💉"
},
"हाई ब्लड प्रेशर": {
    "en": "Hypertension Precautions:\n1. Reduce salt intake 🧂\n2. Exercise daily 🏃\n3. Avoid stress 😌\n4. Regular BP checkup 💉",
    "hi": "हाई ब्लड प्रेशर से बचाव:\n1. नमक का सेवन कम करें 🧂\n2. रोज़ व्यायाम करें 🏃\n3. तनाव से दूर रहें 😌\n4. नियमित बीपी जांच करें 💉"
},
"टीबी": {
    "en": "Tuberculosis Precautions:\n1. Cover mouth while coughing 😷\n2. Take full medicine course 💊\n3. Eat healthy food 🥗\n4. Get regular checkups 🏥",
    "hi": "टीबी से बचाव:\n1. खांसते समय मुंह ढकें 😷\n2. दवा का पूरा कोर्स लें 💊\n3. पौष्टिक भोजन करें 🥗\n4. नियमित जांच करवाएं 🏥"
},
"निमोनिया": {
    "en": "Pneumonia Precautions:\n1. Get vaccinated 💉\n2. Keep warm 🧥\n3. Avoid smoking 🚭\n4. Drink fluids 💧",
    "hi": "निमोनिया से बचाव:\n1. टीकाकरण करवाएं 💉\n2. गर्म कपड़े पहनें 🧥\n3. धूम्रपान से बचें 🚭\n4. तरल पदार्थ पिएं 💧"
},
"हेपेटाइटिस": {
    "en": "Hepatitis Precautions:\n1. Avoid alcohol 🚫🍺\n2. Get vaccinated 💉\n3. Wash hands before meals 🧼\n4. Avoid contaminated food 🚫",
    "hi": "हेपेटाइटिस से बचाव:\n1. शराब से बचें 🚫🍺\n2. टीकाकरण करवाएं 💉\n3. भोजन से पहले हाथ धोएं 🧼\n4. दूषित भोजन से बचें 🚫"
},
"पीलिया": {
    "en": "Jaundice Precautions:\n1. Drink boiled water 💧\n2. Avoid oily food 🍔\n3. Take complete rest 🛌\n4. Consult doctor 🏥",
    "hi": "पीलिया से बचाव:\n1. उबला हुआ पानी पिएं 💧\n2. तैलीय भोजन से बचें 🍔\n3. पूरा आराम करें 🛌\n4. डॉक्टर से परामर्श करें 🏥"
},
"एनीमिया": {
    "en": "Anemia Precautions:\n1. Eat iron-rich food 🥬\n2. Take folic acid supplements 💊\n3. Avoid junk food 🍔\n4. Regular checkups 🩸",
    "hi": "एनीमिया से बचाव:\n1. आयरन युक्त भोजन करें 🥬\n2. फोलिक एसिड सप्लीमेंट लें 💊\n3. जंक फूड से बचें 🍔\n4. नियमित जांच करवाएं 🩸"
},
                "माइग्रेन": {
    "en": "Migraine Precautions:\n1. Avoid loud noise 🔊\n2. Sleep properly 🛌\n3. Avoid stress 😌\n4. Take medicines on time 💊",
    "hi": "माइग्रेन से बचाव:\n1. तेज आवाज से बचें 🔊\n2. पर्याप्त नींद लें 🛌\n3. तनाव से बचें 😌\n4. समय पर दवा लें 💊"
},
"चेचक": {
    "en": "Chickenpox Precautions:\n1. Isolate the patient 🛌\n2. Maintain hygiene 🧼\n3. Do not scratch blisters 🚫\n4. Take rest 😴",
    "hi": "चेचक से बचाव:\n1. रोगी को अलग रखें 🛌\n2. स्वच्छता बनाए रखें 🧼\n3. फोड़े न खुजलाएं 🚫\n4. आराम करें 😴"
},
"हैजा": {
    "en": "Cholera Precautions:\n1. Drink safe water 💧\n2. Maintain hand hygiene 🧼\n3. Avoid street food 🚫\n4. ORS solution intake 🥤",
    "hi": "हैजा से बचाव:\n1. सुरक्षित पानी पिएं 💧\n2. हाथ धोएं 🧼\n3. सड़क का खाना न खाएं 🚫\n4. ओआरएस पिएं 🥤"
},
"गठिया": {
    "en": "Arthritis Precautions:\n1. Do regular exercise 🏃\n2. Maintain healthy weight ⚖️\n3. Avoid stress on joints 🦵\n4. Take medicines timely 💊",
    "hi": "गठिया से बचाव:\n1. नियमित व्यायाम करें 🏃\n2. वजन नियंत्रित रखें ⚖️\n3. जोड़ों पर जोर न डालें 🦵\n4. समय पर दवा लें 💊"
},
"किडनी स्टोन": {
    "en": "Kidney Stone Precautions:\n1. Drink plenty of water 💧\n2. Avoid salty food 🧂\n3. Limit protein intake 🍖\n4. Avoid junk food 🚫",
    "hi": "किडनी स्टोन से बचाव:\n1. खूब पानी पिएं 💧\n2. नमक कम खाएं 🧂\n3. प्रोटीन सीमित लें 🍖\n4. जंक फूड से बचें 🚫"
},
"कैंसर": {
    "en": "Cancer Precautions:\n1. Avoid smoking 🚭\n2. Eat healthy diet 🥗\n3. Go for regular screening 🏥\n4. Stay active 🏃",
    "hi": "कैंसर से बचाव:\n1. धूम्रपान न करें 🚭\n2. संतुलित आहार लें 🥗\n3. नियमित जांच करवाएं 🏥\n4. सक्रिय रहें 🏃"
},
"मोटापा": {
    "en": "Obesity Precautions:\n1. Exercise regularly 🏃\n2. Eat low-fat diet 🥗\n3. Avoid junk food 🍔\n4. Monitor weight ⚖️",
    "hi": "मोटापा से बचाव:\n1. नियमित व्यायाम करें 🏃\n2. कम वसा वाला भोजन करें 🥗\n3. जंक फूड से बचें 🍔\n4. वजन नियंत्रित रखें ⚖️"
},
"अवसाद": {
    "en": "Depression Precautions:\n1. Talk to family/friends 🗣️\n2. Do meditation 🧘\n3. Exercise daily 🏃\n4. Take professional help 🏥",
    "hi": "अवसाद से बचाव:\n1. परिवार/दोस्तों से बात करें 🗣️\n2. ध्यान करें 🧘\n3. रोज़ व्यायाम करें 🏃\n4. विशेषज्ञ से मदद लें 🏥"
},
"गैस्ट्राइटिस": {
    "en": "Gastritis Precautions:\n1. Avoid spicy food 🌶️\n2. Eat on time ⏰\n3. Limit alcohol 🚫🍺\n4. Take medicines properly 💊",
    "hi": "गैस्ट्राइटिस से बचाव:\n1. मसालेदार भोजन से बचें 🌶️\n2. समय पर खाना खाएं ⏰\n3. शराब से बचें 🚫🍺\n4. दवा समय पर लें 💊"
},
"स्ट्रोक": {
    "en": "Stroke Precautions:\n1. Control BP & sugar 🩸\n2. Avoid smoking 🚭\n3. Exercise daily 🏃\n4. Eat healthy diet 🥗",
    "hi": "स्ट्रोक से बचाव:\n1. बीपी और शुगर नियंत्रित रखें 🩸\n2. धूम्रपान से बचें 🚭\n3. नियमित व्यायाम करें 🏃\n4. स्वस्थ आहार लें 🥗"
},
"फ्लू": {
    "en": "Flu Precautions:\n1. Wash hands regularly 🧼\n2. Avoid crowded places 🚫\n3. Cover mouth while coughing 😷\n4. Stay hydrated 💧",
    "hi": "फ्लू से बचाव:\n1. हाथ धोते रहें 🧼\n2. भीड़ से बचें 🚫\n3. खांसते समय मुंह ढकें 😷\n4. पानी अधिक पिएं 💧"
},
"एलर्जी": {
    "en": "Allergy Precautions:\n1. Avoid allergens 🚫\n2. Keep environment clean 🧹\n3. Take prescribed medicine 💊\n4. Consult doctor 🏥",
    "hi": "एलर्जी से बचाव:\n1. एलर्जन से दूर रहें 🚫\n2. वातावरण साफ रखें 🧹\n3. डॉक्टर की बताई दवा लें 💊\n4. डॉक्टर से परामर्श करें 🏥"
},
"थायराइड": {
    "en": "Thyroid Precautions:\n1. Take medicine regularly 💊\n2. Avoid junk food 🚫\n3. Regular checkups 🏥\n4. Eat iodine rich food 🧂",
    "hi": "थायराइड से बचाव:\n1. दवा नियमित लें 💊\n2. जंक फूड से बचें 🚫\n3. नियमित जांच करवाएं 🏥\n4. आयोडीन युक्त भोजन करें 🧂"
},
"अल्सर": {
    "en": "Ulcer Precautions:\n1. Avoid spicy food 🌶️\n2. Don’t skip meals 🍽️\n3. Limit alcohol 🚫🍺\n4. Take medicines on time 💊",
    "hi": "अल्सर से बचाव:\n1. मसालेदार भोजन से बचें 🌶️\n2. खाना न छोड़ें 🍽️\n3. शराब से बचें 🚫🍺\n4. समय पर दवा लें 💊"
},
"मिर्गी": {
    "en": "Epilepsy Precautions:\n1. Take medicines daily 💊\n2. Avoid lack of sleep 🛌\n3. Stay away from bright lights 💡\n4. Inform friends/family 🗣️",
    "hi": "मिर्गी से बचाव:\n1. रोज़ दवा लें 💊\n2. नींद पूरी करें 🛌\n3. तेज रोशनी से बचें 💡\n4. परिवार/दोस्तों को जानकारी दें 🗣️"
},
"त्वचा संक्रमण": {
    "en": "Skin Infection Precautions:\n1. Keep skin clean 🧼\n2. Avoid sharing towels 🚫\n3. Use prescribed creams 💊\n4. Maintain hygiene 🧴",
    "hi": "त्वचा संक्रमण से बचाव:\n1. त्वचा साफ रखें 🧼\n2. तौलिया साझा न करें 🚫\n3. डॉक्टर की दवा लगाएं 💊\n4. स्वच्छता रखें 🧴"
},
"आई फ्लू": {
    "en": "Eye Flu Precautions:\n1. Avoid touching eyes ✋\n2. Use clean tissues 🧻\n3. Do not share handkerchief 🚫\n4. Wash eyes with clean water 💧",
    "hi": "आई फ्लू से बचाव:\n1. आंखों को न छुएं ✋\n2. साफ टिश्यू का उपयोग करें 🧻\n3. रुमाल साझा न करें 🚫\n4. साफ पानी से आंखें धोएं 💧"
},
"हृदय रोग": {
    "en": "Heart Disease Precautions:\n1. Avoid smoking 🚭\n2. Eat low cholesterol food 🥗\n3. Exercise daily 🏃\n4. Manage stress 😌",
    "hi": "हृदय रोग से बचाव:\n1. धूम्रपान से बचें 🚭\n2. कम कोलेस्ट्रॉल वाला भोजन करें 🥗\n3. रोज़ व्यायाम करें 🏃\n4. तनाव नियंत्रित करें 😌"
},
"कुपोषण": {
    "en": "Malnutrition Precautions:\n1. Eat balanced diet 🥗\n2. Include vitamins & minerals 🍎\n3. Avoid junk food 🚫\n4. Regular health checkups 🏥",
    "hi": "कुपोषण से बचाव:\n1. संतुलित आहार लें 🥗\n2. विटामिन और खनिज शामिल करें 🍎\n3. जंक फूड से बचें 🚫\n4. नियमित जांच करवाएं 🏥"
},
"पोलियो": {
    "en": "Polio Precautions:\n1. Vaccinate children 💉\n2. Maintain hygiene 🧼\n3. Drink clean water 💧\n4. Avoid contaminated food 🚫",
    "hi": "पोलियो से बचाव:\n1. बच्चों का टीकाकरण करवाएं 💉\n2. स्वच्छता रखें 🧼\n3. साफ पानी पिएं 💧\n4. दूषित भोजन से बचें 🚫"
},
"स्वाइन फ्लू": {
    "en": "Swine Flu Precautions:\n1. Wear mask 😷\n2. Avoid crowded places 🚫\n3. Wash hands regularly 🧼\n4. Get medical help 🏥",
    "hi": "स्वाइन फ्लू से बचाव:\n1. मास्क पहनें 😷\n2. भीड़ से बचें 🚫\n3. हाथ धोते रहें 🧼\n4. डॉक्टर से मदद लें 🏥"
},

}


        # Detect language automatically
        lang = "hi" if any('\u0900' <= c <= '\u097F' for c in disease) else "en"
        response = precautions.get(disease, {}).get(lang, "I don't have data for this disease yet.")

        dispatcher.utter_message(text=response)
        return []

# ───── Add new class for Symptoms here ─────

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProvideSymptoms(Action):

    def name(self):
        return "action_provide_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        disease = next(tracker.get_latest_entity_values("disease"), None)

        if not disease:
            dispatcher.utter_message(response="utter_ask_disease")
            return []

        # Symptoms data
        symptoms = {
            "malaria": {
                "en": "Malaria Symptoms:\n1. Fever 🌡️\n2. Chills ❄️\n3. Headache 🤕\n4. Nausea 🤢",
                "hi": "मलेरिया लक्षण:\n1. बुखार 🌡️\n2. ठंड लगना ❄️\n3. सिरदर्द 🤕\n4. मतली 🤢"
            },
            "diabetes": {
                "en": "Diabetes Symptoms:\n1. Frequent urination 🚽\n2. Increased thirst 💧\n3. Fatigue 😴\n4. Blurred vision 👀",
                "hi": "डायबिटीज़ लक्षण:\n1. बार-बार पेशाब 🚽\n2. अधिक प्यास 💧\n3. थकान 😴\n4. धुंधली दृष्टि 👀"
            },
            "asthma": {
                "en": "Asthma Symptoms:\n1. Shortness of breath 😮‍💨\n2. Wheezing 🎵\n3. Chest tightness 💢\n4. Coughing 🤧",
                "hi": "अस्थमा लक्षण:\n1. सांस लेने में कठिनाई 😮‍💨\n2. घरघराहट 🎵\n3. सीने में दबाव 💢\n4. खाँसी 🤧"
            },
            "typhoid": {
                "en": "Typhoid Symptoms:\n1. High fever 🌡️\n2. Weakness 😓\n3. Stomach pain 🤕\n4. Loss of appetite 🍽️",
                "hi": "टाइफाइड लक्षण:\n1. तेज बुखार 🌡️\n2. कमजोरी 😓\n3. पेट में दर्द 🤕\n4. भूख कम होना 🍽️"
            },
                "hepatitis": {
        "en": "Hepatitis Symptoms:\n1. Fatigue 😴\n2. Jaundice 👀\n3. Abdominal pain 🤕\n4. Dark urine 🧴",
        "hi": "हेपेटाइटिस लक्षण:\n1. थकान 😴\n2. पीलिया 👀\n3. पेट दर्द 🤕\n4. गाढ़ा मूत्र 🧴"
    },
    "anemia": {
        "en": "Anemia Symptoms:\n1. Fatigue 😴\n2. Pale skin 🧑🏻\n3. Dizziness 😵\n4. Shortness of breath 😮‍💨",
        "hi": "एनीमिया लक्षण:\n1. थकान 😴\n2. पीली त्वचा 🧑🏻\n3. चक्कर आना 😵\n4. सांस फूलना 😮‍💨"
    },
    "migraine": {
        "en": "Migraine Symptoms:\n1. Severe headache 🤕\n2. Nausea 🤢\n3. Sensitivity to light 💡\n4. Sensitivity to sound 🔊",
        "hi": "माइग्रेन लक्षण:\n1. तेज सिरदर्द 🤕\n2. मतली 🤢\n3. रोशनी से परेशानी 💡\n4. आवाज़ से परेशानी 🔊"
    },
    "chickenpox": {
        "en": "Chickenpox Symptoms:\n1. Itchy rash 🤒\n2. Fever 🌡\n3. Fatigue 😴\n4. Loss of appetite 🍽",
        "hi": "चेचक लक्षण:\n1. खुजली वाला दाने 🤒\n2. बुखार 🌡\n3. थकान 😴\n4. भूख कम लगना 🍽"
    },
    "arthritis": {
        "en": "Arthritis Symptoms:\n1. Joint pain 💢\n2. Stiffness 🦴\n3. Swelling 💧\n4. Reduced movement 🚶",
        "hi": "गठिया लक्षण:\n1. जोड़ों में दर्द 💢\n2. जकड़न 🦴\n3. सूजन 💧\n4. चलने-फिरने में कठिनाई 🚶"
    },
    "kidney stone": {
        "en": "Kidney Stone Symptoms:\n1. Severe back/side pain 🤕\n2. Painful urination 🚽\n3. Blood in urine 🧴\n4. Nausea 🤢",
        "hi": "किडनी स्टोन लक्षण:\n1. पीठ/पक्ष में तेज दर्द 🤕\n2. पेशाब में दर्द 🚽\n3. मूत्र में खून 🧴\n4. मतली 🤢"
    },
    "cancer": {
        "en": "Cancer Symptoms:\n1. Unexplained weight loss ⚖\n2. Fatigue 😴\n3. Persistent pain 🤕\n4. Lumps/swelling 🎯",
        "hi": "कैंसर लक्षण:\n1. बिना कारण वजन घटना ⚖\n2. थकान 😴\n3. लगातार दर्द 🤕\n4. गांठ/सूजन 🎯"
    },
    "obesity": {
        "en": "Obesity Symptoms:\n1. Excess body fat ⚖\n2. Breathlessness 😮‍💨\n3. Joint pain 💢\n4. Fatigue 😴",
        "hi": "मोटापा लक्षण:\n1. अधिक शरीर की चर्बी ⚖\n2. सांस फूलना 😮‍💨\n3. जोड़ों में दर्द 💢\n4. थकान 😴"
    },
    "flu": {
        "en": "Flu Symptoms:\n1. Fever 🌡\n2. Cough 🤧\n3. Sore throat 😷\n4. Body aches 💢",
        "hi": "फ्लू लक्षण:\n1. बुखार 🌡\n2. खाँसी 🤧\n3. गले में खराश 😷\n4. शरीर में दर्द 💢"
    },
    "allergy": {
        "en": "Allergy Symptoms:\n1. Sneezing 🤧\n2. Runny nose 👃\n3. Itchy eyes 👀\n4. Skin rash 🤒",
        "hi": "एलर्जी लक्षण:\n1. छींक आना 🤧\n2. बहती नाक 👃\n3. आँखों में खुजली 👀\n4. त्वचा पर चकत्ते 🤒"
    },
    "thyroid": {
        "en": "Thyroid Symptoms:\n1. Fatigue 😴\n2. Weight changes ⚖\n3. Swelling in neck 👤\n4. Mood swings 🙂😡",
        "hi": "थायरॉयड लक्षण:\n1. थकान 😴\n2. वजन में बदलाव ⚖\n3. गर्दन में सूजन 👤\n4. मूड बदलना 🙂😡"
    },
    "epilepsy": {
        "en": "Epilepsy Symptoms:\n1. Seizures ⚡\n2. Confusion 😵\n3. Loss of consciousness 😴\n4. Staring spells 👀",
        "hi": "मिर्गी लक्षण:\n1. दौरे ⚡\n2. भ्रम 😵\n3. होश खोना 😴\n4. घूरना 👀"
    },
    "heart disease": {
        "en": "Heart Disease Symptoms:\n1. Chest pain 💔\n2. Shortness of breath 😮‍💨\n3. Swelling in legs/feet 🦶\n4. Fatigue 😴",
        "hi": "हृदय रोग लक्षण:\n1. सीने में दर्द 💔\n2. सांस फूलना 😮‍💨\n3. पैरों में सूजन 🦶\n4. थकान 😴"
    },
    "malnutrition": {
        "en": "Malnutrition Symptoms:\n1. Weight loss ⚖\n2. Weakness 😓\n3. Dry skin/hair 💇\n4. Slow growth 📉",
        "hi": "कुपोषण लक्षण:\n1. वजन घटना ⚖\n2. कमजोरी 😓\n3. रूखी त्वचा/बाल 💇\n4. धीमी वृद्धि 📉"
    },
    "polio": {
        "en": "Polio Symptoms:\n1. Fever 🌡\n2. Weakness 😓\n3. Muscle pain 💢\n4. Paralysis 🦽",
        "hi": "पोलियो लक्षण:\n1. बुखार 🌡\n2. कमजोरी 😓\n3. मांसपेशियों में दर्द 💢\n4. लकवा 🦽"
    },
    "swine flu": {
        "en": "Swine Flu Symptoms:\n1. Fever 🌡\n2. Cough 🤧\n3. Sore throat 😷\n4. Body pain 💢",
        "hi": "स्वाइन फ्लू लक्षण:\n1. बुखार 🌡\n2. खाँसी 🤧\n3. गले में खराश 😷\n4. शरीर में दर्द 💢"
    },
    "depression": {
        "en": "Depression Symptoms:\n1. Persistent sadness 😢\n2. Loss of interest 🎭\n3. Fatigue 😴\n4. Sleep problems 🛌",
        "hi": "डिप्रेशन लक्षण:\n1. लगातार उदासी 😢\n2. रुचि की कमी 🎭\n3. थकान 😴\n4. नींद की समस्या 🛌"
    },
    "gastritis": {
        "en": "Gastritis Symptoms:\n1. Stomach pain 🤕\n2. Nausea 🤢\n3. Bloating 🎈\n4. Vomiting 🤮",
        "hi": "गैस्ट्राइटिस लक्षण:\n1. पेट दर्द 🤕\n2. मतली 🤢\n3. पेट फूलना 🎈\n4. उल्टी 🤮"
    },
    "ulcer": {
        "en": "Ulcer Symptoms:\n1. Burning stomach pain 🔥\n2. Bloating 🎈\n3. Heartburn 💔\n4. Nausea 🤢",
        "hi": "अल्सर लक्षण:\n1. पेट में जलन 🔥\n2. पेट फूलना 🎈\n3. सीने में जलन 💔\n4. मतली 🤢"
    },
    "skin infection": {
        "en": "Skin Infection Symptoms:\n1. Redness 🔴\n2. Swelling 💧\n3. Itching 🤕\n4. Pus discharge 💦",
        "hi": "त्वचा संक्रमण लक्षण:\n1. लालिमा 🔴\n2. सूजन 💧\n3. खुजली 🤕\n4. पस निकलना 💦"
    },
    "eye flu": {
        "en": "Eye Flu Symptoms:\n1. Red eyes 👀\n2. Watering 💧\n3. Itching 🤕\n4. Blurred vision 👓",
        "hi": "आंखों का फ्लू लक्षण:\n1. लाल आँखें 👀\n2. पानी आना 💧\n3. खुजली 🤕\n4. धुंधली दृष्टि 👓"
    }

        }

        # Detect language automatically
        lang = "hi" if any('\u0900' <= c <= '\u097F' for c in disease) else "en"
        response = symptoms.get(disease, {}).get(lang, "I don't have symptom data for this disease yet.")

        dispatcher.utter_message(text=response)
        return []



