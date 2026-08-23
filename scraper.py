import json
import os

print("Starting Government Schemes Scraper...")

# Fallback robust data focusing on State/Region and Caste differences.
# In a real enterprise system, this would crawl myscheme.gov.in using Selenium/Playwright due to their React SPA nature.
scraped_policies = [
    {
        "id": "maharashtra-jyotirao",
        "title": {
            "en": "Mahatma Jyotirao Phule Shetkari Karjmukti Yojana",
            "hi": "महात्मा जोतीराव फुले शेतकरी कर्जमुक्ति योजना",
            "pa": "ਮਹਾਤਮਾ ਜੋਤੀਰਾਓ ਫੂਲੇ ਕਿਸਾਨ ਕਰਜ਼ ਮੁਆਫੀ ਯੋਜਨਾ",
            "ta": "மகாத்மா ஜோதிராவ் பூலே உழவர் கடன் தள்ளுபடி திட்டம்",
            "bn": "মহাত্মা জ্যোতিরাও ফুলে কৃষক ঋণ মুক্তি যোজনা"
        },
        "description": {
            "en": "Debt relief scheme for farmers in Maharashtra with outstanding crop loans.",
            "hi": "महाराष्ट्र में बकाया फसल ऋण वाले किसानों के लिए ऋण राहत योजना।",
            "pa": "ਮਹਾਰਾਸ਼ਟਰ ਵਿੱਚ ਕਿਸਾਨਾਂ ਲਈ ਕਰਜ਼ਾ ਰਾਹਤ ਯੋਜਨਾ।",
            "ta": "மகாராஷ்டிராவில் உள்ள விவசாயிகளுக்கான கடன் நிவாரண திட்டம்.",
            "bn": "মহারাষ্ট্রের কৃষকদের জন্য ঋণ মকুব প্রকল্প।"
        },
        "benefits": {
            "en": ["Waiver of crop loans up to ₹2,000,00", "Direct settlement with banks", "No collateral required"],
            "hi": ["₹2,000,00 तक के फसल ऋण की माफी"],
            "pa": ["₹2,000,00 ਤੱਕ ਦੇ ਫਸਲੀ ਕਰਜ਼ੇ ਦੀ ਮੁਆਫੀ"],
            "ta": ["₹2,000,00 வரை பயிர் கடன் தள்ளுபடி"],
            "bn": ["২ লক্ষ টাকা পর্যন্ত কৃষি ঋণ মকুব"]
        },
        "metrics": {"maxIncome": 800000, "ageMin": 18, "ageMax": 70, "benefitAmount": 200000},
        "eligibility": {
            "profession": ["farmer", "agricultural laborer"],
            "caste": ["any", "sc", "st", "obc"],
            "gender": ["any", "male", "female"],
            "incomeMax": 800000,
            "ageMin": 18,
            "ageMax": 70,
            "region": ["maharashtra"]
        }
    },
    {
        "id": "punjab-ashirwad",
        "title": {
            "en": "Punjab Ashirwad Scheme",
            "hi": "पंजाब आशीर्वाद योजना",
            "pa": "ਪੰਜਾਬ ਆਸ਼ੀਰਵਾਦ ਯੋਜਨਾ",
            "ta": "பஞ்சாப் ஆசிர்வாத் திட்டம்",
            "bn": "পাঞ্জাব আশীর্বাদ যোজনা"
        },
        "description": {
            "en": "Financial assistance of ₹51,000 for the marriage of girls belonging to SC/BC/Minority/BPL families.",
            "hi": "SC/BC/अल्पसंख्यक/BPL परिवारों की लड़कियों की शादी के लिए ₹51,000 की वित्तीय सहायता।",
            "pa": "SC/BC/ਘੱਟ ਗਿਣਤੀ/BPL ਪਰਿਵਾਰਾਂ ਦੀਆਂ ਕੁੜੀਆਂ ਦੇ ਵਿਆਹ ਲਈ ₹51,000 ਦੀ ਵਿੱਤੀ ਸਹਾਇਤਾ।",
            "ta": "எஸ்சி/பிசி/சிறுபான்மையினர் குடும்பங்களைச் சேர்ந்த பெண்களின் திருமணத்திற்கு ₹51,000 நிதியுதவி.",
            "bn": "এসসি/বিসি/সংখ্যালঘু/বিপিএল পরিবারের মেয়েদের বিয়ের জন্য ৫১,০০০ টাকার আর্থিক সহায়তা।"
        },
        "benefits": {
            "en": ["₹51,000 Shagun at the time of marriage", "Direct transfer to beneficiary account"],
            "hi": ["शादी के समय ₹51,000 शगुन"],
            "pa": ["ਵਿਆਹ ਦੇ ਸਮੇਂ ₹51,000 ਸ਼ਗੁਨ"],
            "ta": ["திருமணத்தின் போது ₹51,000 ஷகுன்"],
            "bn": ["বিয়ের সময় ৫১,০০০ টাকার শাগুন"]
        },
        "metrics": {"maxIncome": 32790, "ageMin": 18, "ageMax": 35, "benefitAmount": 51000},
        "eligibility": {
            "profession": ["any", "student", "unemployed", "homemaker"],
            "caste": ["sc", "obc", "minority"],
            "gender": ["female"],
            "incomeMax": 32790,
            "ageMin": 18,
            "ageMax": 35,
            "region": ["punjab"]
        }
    },
    {
        "id": "pm-svanidhi",
        "title": {
            "en": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
            "hi": "पीएम स्वनिधि",
            "pa": "ਪੀਐਮ ਸਵਨਿਧੀ",
            "ta": "பிஎம் ஸ்வநிதி",
            "bn": "পিএম স্বনিধি"
        },
        "description": {
            "en": "Micro-credit facility that provides affordable collateral-free working capital loans to street vendors.",
            "hi": "सड़क विक्रेताओं को किफायती संपार्श्विक-मुक्त कार्यशील पूंजी ऋण प्रदान करने वाली सूक्ष्म ऋण सुविधा।",
            "pa": "ਮਾਈਕ੍ਰੋ-ਕ੍ਰੈਡਿਟ ਸਹੂਲਤ ਜੋ ਸਟ੍ਰੀਟ ਵੈਂਡਰਾਂ ਨੂੰ ਕਿਫਾਇਤੀ ਜਮਾਂਦਰੂ-ਮੁਕਤ ਕਾਰਜਸ਼ੀਲ ਪੂੰਜੀ ਕਰਜ਼ੇ ਪ੍ਰਦਾਨ ਕਰਦੀ ਹੈ।",
            "ta": "தெரு வியாபாரிகளுக்கு மலிவு விலையில் பிணையமில்லா கடன் வழங்கும் சிறு-கடன் வசதி.",
            "bn": "রাস্তার বিক্রেতাদের জন্য একটি মাইক্রো-ক্রেডিট সুবিধা যা জামানত-মুক্ত ঋণ প্রদান করে।"
        },
        "benefits": {
            "en": ["Working capital loan up to ₹10,000", "7% interest subsidy", "Cashback on digital transactions"],
            "hi": ["₹10,000 तक का कार्यशील पूंजी ऋण"],
            "pa": ["₹10,000 ਤੱਕ ਦਾ ਕਾਰਜਸ਼ੀਲ ਪੂੰਜੀ ਕਰਜ਼ਾ"],
            "ta": ["₹10,000 வரை செயல் மூலதனக் கடன்"],
            "bn": ["১০,০০০ টাকা পর্যন্ত ঋণ"]
        },
        "metrics": {"maxIncome": 500000, "ageMin": 18, "ageMax": 65, "benefitAmount": 10000},
        "eligibility": {
            "profession": ["street vendor", "business owner", "artisan", "weaver", "barber"],
            "caste": ["any", "general", "obc", "sc", "st", "minority"],
            "gender": ["any", "male", "female", "other"],
            "incomeMax": 500000,
            "ageMin": 18,
            "ageMax": 65,
            "region": ["any", "punjab", "haryana", "delhi", "maharashtra"]
        }
    }
]

# We write this as a JS file so the browser can load it locally without CORS issues.
js_content = f"""// AUTO-GENERATED BY scraper.py
const i18n = {{
    en: {{
        navHome: "Home", navCompare: "Visual Compare", navSentiment: "Sentiment", navLogin: "Login", navLogout: "Logout",
        title: "Discover Your Benefits", subtitle: "Find highly specific policies based on your State and Caste.",
        region: "State/Region", caste: "Caste/Community Category", age: "Age", income: "Annual Income (₹)", gender: "Gender", profession: "Profession",
        submit: "Find Eligible Schemes", resultsTitle: "Matched Policies", noResults: "No policies match this specific Region/Caste combination.",
        readMore: "View Policy Details", compareTitle: "Visual Dashboard Comparison", compareBtn: "Analyze Policies",
        casteOptions: ["General", "OBC (Other Backward Class)", "SC (Scheduled Caste)", "ST (Scheduled Tribe)", "EBC (Economically Backward)", "Minority", "Nomadic Tribes"],
        regionOptions: ["All India", "Punjab", "Haryana", "Delhi", "Maharashtra", "Tamil Nadu", "West Bengal", "Uttar Pradesh"]
    }}
}};

const policies = {json.dumps(scraped_policies, indent=4)};
"""

with open('scraped_data.js', 'w') as f:
    f.write(js_content)

print("✅ Successfully generated scraped_data.js with Region and Caste specific policies!")
