import json
import requests
import time
from data_base.db_connection.db_mongo import collection
from bson import json_util  # ייבוא מודול bson.json_util

# הגדרת משתנים
EVENT_REGISTRY_URL = "http://localhost:5000/articles?page="
GROQ_API_KEY = "xai-Eyla3sPEnxbmfjaPvflTCQJSnpnXEeLg6PdCH9Uli7wxIbe9docUFNG5Jv2lTSE6h6jDR7Xw09OQhp1I"
GROQ_API_URL = "https://api.x.ai/v1/chat/completions"
OPENCAGE_API_KEY = "8f115f04ffd44908b3b0ff9d242f428b"

response_format_groq = {
    "type": "json_schema",
    "json_schema": {
        "name": "news_classification",
        "schema": {
            "type": "object",
            "properties": {
                "classification": {
                    "type": "string",
                    "enum": [
                        "Current terrorism event",
                        "Past terrorism event",
                        "Other news event"
                    ]
                },
                "location": {
                    "type": "string",
                    "description": "The location where the event occurred",
                    "longitude": "float",
                    "latitude" : "float"
                }
            },
            "required": ["classification", "location"],
            "additionalProperties": False
        },
        "strict": True
    }
}

def fetch_articles(page):
    response = requests.get(f"{EVENT_REGISTRY_URL}{page}")
    if response.status_code == 200:
        return response.json().get('articles')
    else:
        print(f"Error fetching articles: {response.status_code}")
        return []

def classify_news_article(article_content):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
        "messages": [
            {"role": "system",
             "content": """
             Hello,
             Please return the following data in JSON format:
             {
               "country": "string",
               "city": "string",
               "lon": "float",
               "lat": "float",
               "category": "enum": [
                 "Current terrorism event",
                 "Past terrorism event",
                 "Other news event"
               ]
             }
             Explanation of the fields:
             country: The name of the country where the event occurred.
             city: The name of the city where the event occurred.
             lon: The longitude of the event location.
             lat: The latitude of the event location.
             category: The category of the event.
             Thank you!"""},
            {"role": "user", "content": f"This is a news article: {article_content}"}
        ],
        "model": "grok-2-1212",
        "stream": False,
        "temperature": 0,
        "response_format": response_format_groq
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            response_json = response.json()
            return response_json
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
            return None
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None

def get_location(name):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={name}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]
            lon = location["lng"]
            lat = location["lat"]
            return {"lon": lon, "lat": lat}
        else:
            print(f"No geolocation data found for {name}.")
            return {"lon": 0.0, "lat": 0.0}
    else:
        print(f"Error fetching geolocation data: {response.status_code}")
        return {"lon": 0.0, "lat": 0.0}

def main():
    articles_page = 1
    while True:
        print(f"Fetching articles for page {articles_page}...")
        articles = fetch_articles(articles_page)
        if not articles:
            break
        results = articles.get("results")

        for article in results[:10]:
            body = article.get("body", "")
            location = article.get("source", {}).get("title", "Unknown Location")
            body = body[:300]  # לקיחת 300 מילים ראשונות מהמאמר
            classification = classify_news_article(body)
            content = classification['choices'][0]['message']['content']

            # המרת התוכן למילון
            parsed_content = json.loads(content)

            # יצירת אובייקט JSON חדש
            result = {
                'country': parsed_content.get('location', ''),
                'city': '',
                'category': parsed_content.get('classification', '')
            }
            location_ll = get_location(result['country'])
            result['lon'] = location_ll['lon']
            result['lat'] = location_ll['lat']

            # הוספת התוצאה למונגו
            collection.insert_one(result)

            # הדפסת התוצאה ב-JJSON עם bson.json_util
            print(json.dumps(result, default=json_util.default, indent=2))
            print(classification)

        articles_page += 1
        time.sleep(120)

if __name__ == "__main__":
    main()
