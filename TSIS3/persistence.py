import json

def load_settings():
    try:
        return json.load(open("settings.json"))
    except:
        return {"difficulty":"normal"}

def save_settings(settings):
    json.dump(settings, open("settings.json","w"), indent=4)

def load_leaderboard():
    try:
        return json.load(open("leaderboard.json"))
    except:
        return []

def save_score(name, score, distance):
    data = load_leaderboard()
    data.append({"name":name,"score":score})
    data = sorted(data, key=lambda x:x['score'], reverse=True)[:10]
    json.dump(data, open("leaderboard.json","w"), indent=4)