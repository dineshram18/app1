from flask import Flask, render_template, request

app = Flask(__name__)

QUESTIONS = [
    {
        "question": "You find it takes effort to introduce yourself to other people.",
        "dimension": "I/E",
        "reverse": False
    },
    {
        "question": "You consider yourself more practical than creative.",
        "dimension": "S/N",
        "reverse": True
    },
    {
        "question": "Winning a debate matters less to you than making sure no one gets upset.",
        "dimension": "T/F",
        "reverse": True
    },
    {
        "question": "You get energized going to social events that involve many interactions.",
        "dimension": "I/E",
        "reverse": True
    },
    {
        "question": "You often spend time exploring unrealistic and impractical yet intriguing ideas.",
        "dimension": "S/N",
        "reverse": False
    },
    {
        "question": "Your travel plans are more likely to look like a rough list of ideas than a detailed itinerary.",
        "dimension": "J/P",
        "reverse": True
    },
    {
        "question": "You often think about what you should have said in a conversation long after it has taken place.",
        "dimension": "T/F",
        "reverse": False
    },
    {
        "question": "If your friend is sad about something, your first instinct is to support them emotionally, not try to solve their problem.",
        "dimension": "T/F",
        "reverse": False
    }
]

DIMENSIONS = {
    "I/E": ("I", "E"),
    "S/N": ("S", "N"),
    "T/F": ("T", "F"),
    "J/P": ("J", "P")
}

RESULT_DESCRIPTIONS = {
    "INTJ": "Imaginative and strategic thinkers, with a plan for everything.",
    "INTP": "Innovative inventors with an unquenchable thirst for knowledge.",
    "ENTJ": "Bold, imaginative and strong-willed leaders, always finding a way—or making one.",
    "ENTP": "Smart and curious thinkers who cannot resist an intellectual challenge.",
    "INFJ": "Quiet and mystical, yet very inspiring and tireless idealists.",
    "INFP": "Poetic, kind and altruistic people, always eager to help a good cause.",
    "ENFJ": "Charismatic and inspiring leaders, able to mesmerize their listeners.",
    "ENFP": "Enthusiastic, creative and sociable free spirits, who can always find a reason to smile.",
    "ISTJ": "Practical and fact-minded individuals, whose reliability cannot be doubted.",
    "ISFJ": "Very dedicated and warm protectors, always ready to defend their loved ones.",
    "ESTJ": "Excellent administrators, unsurpassed at managing things—or people.",
    "ESFJ": "Extraordinarily caring, social and popular people, always eager to help.",
    "ISTP": "Bold and practical experimenters, masters of all kinds of tools.",
    "ISFP": "Flexible and charming artists, always ready to explore and experience something new.",
    "ESTP": "Smart, energetic and very perceptive people, who truly enjoy living on the edge.",
    "ESFP": "Spontaneous, energetic and enthusiastic entertainers—life is never boring around them."
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = [int(request.form.get(f"q{i}", 0)) for i in range(len(QUESTIONS))]
        scores = {
            "I": 0, "E": 0,
            "S": 0, "N": 0,
            "T": 0, "F": 0,
            "J": 0, "P": 0
        }
        for i, answer in enumerate(answers):
            q = QUESTIONS[i]
            d1, d2 = DIMENSIONS[q["dimension"]]
            if (answer == 1 and not q["reverse"]) or (answer == 0 and q["reverse"]):
                scores[d1] += 1
            else:
                scores[d2] += 1
        mbti = (
            ("I" if scores["I"] >= scores["E"] else "E") +
            ("S" if scores["S"] >= scores["N"] else "N") +
            ("T" if scores["T"] >= scores["F"] else "F") +
            ("J" if scores["J"] >= scores["P"] else "P")
        )
        description = RESULT_DESCRIPTIONS.get(mbti, "No description available.")
        return render_template("result.html", mbti=mbti, description=description)
    return render_template("index.html", questions=QUESTIONS)

if __name__ == "__main__":
    app.run(debug=True)