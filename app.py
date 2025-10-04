from flask import Flask, request, render_template, send_from_directory
import google.generativeai as genai
import os
import json

app = Flask(__name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

# Load override database
with open('override_db.json', 'r') as f:
    override_db = json.load(f)

# Improved override matching logic
def search_local_override(lyrics_input):
    normalized_input = lyrics_input.lower().strip()
    for entry in override_db:
        snippet = entry['lyrics_snippet'].lower().strip()
        if snippet in normalized_input or normalized_input in snippet:
            return f"{entry['correct_title']} by {entry['correct_artist']}"
    return None

def get_song_match_from_gemini(lyrics):
    prompt = (
        f"From these lyrics: '{lyrics}', identify the exact song title and artist name and please double check before giving your final answer. "
        "And if you are unsure, use your intelligency to give two or three possible matches. "
        "Respond only in this format: 'Song Title by Artist Name'. Do not explain your answer."
    )

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()

        if result and "by" in result.lower():
            return result

        fallback_prompt = (
            f"Who sings the song with these lyrics: '{lyrics}'? Respond only with: 'Song Title by Artist Name'."
        )
        fallback_response = model.generate_content(fallback_prompt)
        fallback_result = fallback_response.text.strip()

        if fallback_result and "by" in fallback_result.lower():
            return fallback_result

        return None

    except Exception as e:
        print("Gemini API Error:", e)
        return None

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_lyrics = request.form.get("lyrics")
        lyrics_input = user_lyrics.lower().strip()

        # First check override DB
        match = search_local_override(lyrics_input)

        # If no override match, use Gemini
        if not match:
            match = get_song_match_from_gemini(lyrics_input)

        if match:
            message = f"Match found: {match}"
        else:
            message = f"No match found for: '{user_lyrics}'"

        return render_template("index.html", message=message, loading=False)

    return render_template("index.html", loading=False)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('.', 'sw.js')

@app.route('/google1234567890abcdef.html')  # Replace with your actual filename
def serve_google_verification():
    return send_from_directory('.', 'google1234567890abcdef.html')

@app.route('/robots.txt')
def serve_robots():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def serve_sitemap():
    return send_from_directory('.', 'sitemap.xml')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)