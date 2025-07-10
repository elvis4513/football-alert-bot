# Trigger redeploy
import requests
import time
import datetime

from telegram import Bot

# === CONFIGURATION ===
SPORTMONKS_API_TOKEN = "pPrBdWiUOtoEJyXcrYiwbbEADz59|gVLGJ4Z17kfvMxH|6CPwZy|KbgXcsl2"
TELEGRAM_BOT_TOKEN = "7692195219:AAHbR-7wZFcDK1t9GFj_I2gn_4J2_hCKp7A"
TELEGRAM_CHAT_ID = "1205297695"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# === FUNCTION TO GET TODAY'S FIXTURES ===
def get_today_fixtures():
    today = datetime.date.today()
    url = f"https://api.sportmonks.com/v3/football/fixtures/date/{today}?include=participants;stats&api_token={SPORTMONKS_API_TOKEN}"
    response = requests.get(url)
    data = response.json()
    return data.get("data", [])

# === FUNCTION TO FILTER MATCHES ===
def filter_matches(fixtures):
    filtered = []
    for match in fixtures:
        try:
            stats = match.get("stats", {})
            home = match["participants"][0]["name"]
            away = match["participants"][1]["name"]

            # Placeholder logic - adjust when stat fields are identified
            avg_goals = stats.get("avg_goals", 3.1)  # Simulated fallback
            btts_rate = stats.get("btts_rate", 72)    # Simulated fallback
            predicted_result = "1"  # Placeholder (1 = home win)

            if avg_goals >= 2.5 and btts_rate >= 65:
                filtered.append({
                    "match": f"{home} vs {away}",
                    "avg_goals": avg_goals,
                    "btts_rate": btts_rate,
                    "prediction": predicted_result
                })
        except Exception as e:
            print("Error filtering match:", e)
    return filtered

# === FUNCTION TO SEND MATCHES TO TELEGRAM ===
def send_matches(matches):
    if not matches:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="⚽ No trending matches today.")
        return

    for match in matches:
        message = (
            f"🔥 *Trending Match Alert!*\n"
            f"*Match:* {match['match']}\n"
            f"*Avg Goals:* {match['avg_goals']}\n"
            f"*BTTS Rate:* {match['btts_rate']}%\n"
            f"*1X2 Prediction:* {match['prediction']}"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')

# === MAIN SCRIPT ===
def main():
    print("Fetching today’s fixtures...")
    fixtures = get_today_fixtures()
    matches = filter_matches(fixtures)
    send_matches(matches)

if __name__ == "__main__":
    main()
