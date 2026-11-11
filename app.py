from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)


# --------------------------------------------------
# Waste Database
# --------------------------------------------------

waste_database = {

    "plastic bottle": {
        "type": "Recyclable",
        "reuse": "Can be reused as a plant pot, storage container, or craft item.",
        "score": 80
    },

    "banana peel": {
        "type": "Biodegradable",
        "reuse": "Can be added to compost or used to make organic manure.",
        "score": 85
    },

    "newspaper": {
        "type": "Recyclable",
        "reuse": "Can be reused for paper crafts, packing material, or cleaning windows.",
        "score": 80
    },

    "glass bottle": {
        "type": "Reusable",
        "reuse": "Can be reused as a storage bottle, flower vase, or decorative item.",
        "score": 90
    },

    "cardboard": {
        "type": "Recyclable",
        "reuse": "Can be reused for storage boxes, crafts, or packaging.",
        "score": 80
    },

    "old clothes": {
        "type": "Reusable",
        "reuse": "Can be donated, converted into cleaning cloths, or used for crafts.",
        "score": 90
    },

    "metal can": {
        "type": "Recyclable",
        "reuse": "Can be reused as a pen holder, storage container, or craft item.",
        "score": 80
    },

    "food waste": {
        "type": "Biodegradable",
        "reuse": "Can be composted and converted into organic manure.",
        "score": 85
    },

    "wooden box": {
        "type": "Reusable",
        "reuse": "Can be reused as a storage box, plant holder, or decoration.",
        "score": 90
    },

    "paper cup": {
        "type": "Recyclable",
        "reuse": "Can be reused for small crafts or disposed of through suitable recycling.",
        "score": 80
    }
}


# --------------------------------------------------
# History File
# --------------------------------------------------

HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "eco_history.json"
)


# --------------------------------------------------
# Save Waste History
# --------------------------------------------------

def save_history(waste_item, data):

    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    record = {
        "item": waste_item,
        "type": data["type"],
        "score": data["score"]
    }

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


# --------------------------------------------------
# Get Statistics
# --------------------------------------------------

def get_statistics():

    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    total = len(history)

    recyclable = 0
    reusable = 0
    biodegradable = 0

    scores = []

    for record in history:

        if "type" not in record or "score" not in record:
            continue

        if record["type"] == "Recyclable":
            recyclable += 1

        elif record["type"] == "Reusable":
            reusable += 1

        elif record["type"] == "Biodegradable":
            biodegradable += 1

        scores.append(record["score"])

    if scores:
        average_score = round(
            sum(scores) / len(scores),
            2
        )
    else:
        average_score = 0

    return (
        total,
        recyclable,
        reusable,
        biodegradable,
        average_score
    )


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        waste_item = request.form.get(
            "waste",
            ""
        ).strip().lower()

        if waste_item in waste_database:

            data = waste_database[waste_item]

            save_history(
                waste_item,
                data
            )

            result = (
                f"<strong>Waste Item:</strong> {waste_item}<br>"
                f"<strong>Category:</strong> {data['type']}<br>"
                f"<strong>Reuse Suggestion:</strong> {data['reuse']}<br>"
                f"<strong>Eco Score:</strong> {data['score']} / 100"
            )

        else:

            result = (
                "<strong>Waste item not found.</strong><br>"
                "Please try items such as plastic bottle, "
                "banana peel, newspaper, glass bottle, "
                "cardboard, or old clothes."
            )

    # Get statistics for the same page

    (
        total,
        recyclable,
        reusable,
        biodegradable,
        average_score
    ) = get_statistics()

    return render_template(
        "index.html",
        result=result,
        total=total,
        recyclable=recyclable,
        reusable=reusable,
        biodegradable=biodegradable,
        average_score=average_score
    )


# --------------------------------------------------
# Statistics Page
# --------------------------------------------------

@app.route("/statistics")
def statistics():

    (
        total,
        recyclable,
        reusable,
        biodegradable,
        average_score
    ) = get_statistics()

    return render_template(
        "statistics.html",
        total=total,
        recyclable=recyclable,
        reusable=reusable,
        biodegradable=biodegradable,
        average_score=average_score
    )


# --------------------------------------------------
# Run Flask Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)