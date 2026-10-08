import datetime
import json
import urllib.error
import urllib.parse
import urllib.request
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Integrated API Key
API_KEY = "d3faacc7d17546cf8ddce6b3d7264343"
BASE_URL = "https://newsapi.org/v2/top-headlines"
OUTPUT_FILE = "headlines_summary.txt"


def fetch_live_news(region="in", category="general", query=""):
    """Fetches news based on region (in = India, world = global),

    category, or custom search query.
    """
    params = {"apiKey": API_KEY, "pageSize": 25}

    if query:
        # Search query across world news
        url = "https://newsapi.org/v2/everything"
        params["q"] = query
        params["sortBy"] = "publishedAt"
        params["language"] = "en"
    else:
        url = BASE_URL
        if region == "world":
            params["language"] = "en"
        else:
            # Defaults to India
            params["country"] = "in"

        if category and category != "all":
            params["category"] = category

    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        full_url, headers={"User-Agent": "NewsAggregator/1.0"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("articles", [])
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


def save_to_summary_file(articles, category_or_region):
    """Saves top fetched news items into headlines_summary.txt file."""
    if not articles:
        return

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    header = f"LATEST {category_or_region.upper()} HEADLINES - {today_str}"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"{header}\n")
        f.write("=" * len(header) + "\n\n")

        for idx, art in enumerate(articles[:10], start=1):
            title = art.get("title", "No Title")
            source = (art.get("source") or {}).get("name", "Unknown")
            desc = art.get("description", "No summary available.")

            f.write(f"{idx}. {title}\n")
            f.write(f"Source: {source}\n")
            f.write(f"Summary: {desc}\n")
            f.write("-" * 40 + "\n\n")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/news")
def get_news():
    region = request.args.get("region", "in")
    category = request.args.get("category", "all")
    query = request.args.get("q", "").strip()

    articles = fetch_live_news(region=region, category=category, query=query)

    # Automatically save headlines to text report
    label = query if query else f"{region}_{category}"
    save_to_summary_file(articles, label)

    return jsonify(
        {"status": "ok", "total": len(articles), "articles": articles}
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
