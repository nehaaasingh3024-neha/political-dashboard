import feedparser
import pandas as pd
from datetime import datetime

# ---------------------------------
# RSS FEEDS
# ---------------------------------

rss_feeds = {
    "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "India Today": "https://www.indiatoday.in/rss/home",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss"
}

# ---------------------------------
# LEADERS + PARTIES
# ---------------------------------

leader_party_map = {

    # BJP
    "Narendra Modi": "BJP",
    "Amit Shah": "BJP",
    "Yogi Adityanath": "BJP",
    "Keshav Prasad Maurya": "BJP",
    "Rajnath Singh": "BJP",
    "Nitin Gadkari": "BJP",
    "Shivraj Singh Chouhan": "BJP",
    "Dharmendra Pradhan": "BJP",
    "Anurag Thakur": "BJP",
    "Smriti Irani": "BJP",

    # Congress
    "Rahul Gandhi": "INC",
    "Sonia Gandhi": "INC",
    "Priyanka Gandhi": "INC",
    "Mallikarjun Kharge": "INC",
    "Sachin Pilot": "INC",
    "Bhupesh Baghel": "INC",

    # SP
    "Akhilesh Yadav": "SP",
    "Dimple Yadav": "SP",
    "Ram Gopal Yadav": "SP",
    "Pushpendra Saroj": "SP",

    # BSP
    "Mayawati": "BSP",
    "Anand Kumar": "BSP",

    # AAP
    "Arvind Kejriwal": "AAP",
    "Bhagwant Mann": "AAP",
    "Manish Sisodia": "AAP",

    # TMC
    "Mamata Banerjee": "TMC",
    "Abhishek Banerjee": "TMC",

    # RJD
    "Tejashwi Yadav": "RJD",
    "Lalu Prasad Yadav": "RJD",

    # JDU
    "Nitish Kumar": "JDU",

    # DMK
    "M K Stalin": "DMK",
    "Udhayanidhi Stalin": "DMK",

    # BRS
    "K Chandrashekar Rao": "BRS",
    "KTR": "BRS",

    # NCP
    "Sharad Pawar": "NCP",
    "Ajit Pawar": "NCP",

    # Shiv Sena
    "Uddhav Thackeray": "Shiv Sena",
    "Eknath Shinde": "Shiv Sena"
}

# ---------------------------------
# CONSTITUENCIES
# ---------------------------------

constituencies = [
    "Kaushambi",
    "Prayagraj",
    "Allahabad",
    "Sirathu",
    "Chail",
    "Manjhanpur",
    "Kunda",
    "Phaphamau",
    "Soraon"
]

# ---------------------------------
# STATES
# ---------------------------------

states = [
    "Uttar Pradesh",
    "Bihar",
    "Delhi",
    "Maharashtra",
    "Gujarat",
    "Rajasthan",
    "Madhya Pradesh",
    "Punjab",
    "Haryana",
    "Uttarakhand",
    "Himachal Pradesh",
    "Jharkhand",
    "Chhattisgarh",
    "West Bengal",
    "Odisha",
    "Assam",
    "Tamil Nadu",
    "Kerala",
    "Karnataka",
    "Andhra Pradesh",
    "Telangana",
    "Goa",
    "Jammu and Kashmir"
]

# ---------------------------------
# TOPICS
# ---------------------------------

topic_rules = {

    "Politics": [
        "election","party","minister","government",
        "bjp","congress","sp","aap","tmc"
    ],

    "Employment": [
        "employment","job","jobs",
        "recruitment","vacancy","hiring"
    ],

    "Education": [
        "student","students","exam",
        "school","college","university",
        "neet","jee"
    ],

    "Health": [
        "hospital","health","doctor",
        "medical","covid","medicine"
    ],

    "Infrastructure": [
        "road","bridge","railway",
        "highway","metro","airport"
    ],

    "Agriculture": [
        "farmer","farmers",
        "crop","agriculture","wheat","rice"
    ],

    "Law & Order": [
        "police","crime","arrest",
        "court","violence","murder"
    ],

    "Women": [
        "women","woman",
        "girl","mahila","female"
    ],

    "Youth": [
        "youth","sports",
        "young","startup"
    ],

    "Economy": [
        "economy","gdp",
        "inflation","tax","budget"
    ],

    "Environment": [
        "climate","environment",
        "rain","flood","pollution"
    ],

    "Technology": [
        "ai","technology",
        "digital","startup","software"
    ],

    "Development": [
        "project","development",
        "scheme","investment"
    ]
}

# ---------------------------------
# FETCH NEWS
# ---------------------------------

rows = []

for source_name, rss_url in rss_feeds.items():

    feed = feedparser.parse(rss_url)

    for entry in feed.entries[:20]:

        headline = entry.title

        # -------------------------
        # LEADER DETECTION
        # -------------------------

        leader_found = "General Political News"
        party_found = "Multi-Party"

        for leader, party in leader_party_map.items():

            if leader.lower() in headline.lower():

                leader_found = leader
                party_found = party
                break

        # -------------------------
        # LOCATION DETECTION
        # -------------------------

        constituency_found = "National"
        district_found = "India"

        for constituency in constituencies:

            if constituency.lower() in headline.lower():

                constituency_found = constituency

                if constituency in [
                    "Kaushambi",
                    "Sirathu",
                    "Chail",
                    "Manjhanpur"
                ]:
                    district_found = "Kaushambi"

                elif constituency in [
                    "Prayagraj",
                    "Allahabad",
                    "Phaphamau",
                    "Soraon"
                ]:
                    district_found = "Prayagraj"

                break

        if constituency_found == "National":

            for state in states:

                if state.lower() in headline.lower():

                    constituency_found = state
                    district_found = state
                    break

        # -------------------------
        # TOPIC DETECTION
        # -------------------------

        topic_found = "General"

        for topic, keywords in topic_rules.items():

            matched = False

            for keyword in keywords:

                if keyword.lower() in headline.lower():

                    topic_found = topic
                    matched = True
                    break

            if matched:
                break

        # -------------------------
        # SAVE ROW
        # -------------------------

        rows.append({
            "Date": datetime.now().strftime("%d-%m-%Y"),
            "Headline": headline,
            "Constituency": constituency_found,
            "District": district_found,
            "Leader": leader_found,
            "Party": party_found,
            "Topic": topic_found,
            "Source": source_name
        })

# ---------------------------------
# CREATE CSV
# ---------------------------------

df = pd.DataFrame(rows)

df.to_csv("news.csv", index=False)

print(f"{len(df)} articles fetched successfully!")