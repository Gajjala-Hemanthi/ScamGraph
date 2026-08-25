from flask import Flask, render_template, request
from database import driver

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    results = None
    username = ""
    risk_score = 0
    risk_level = ""
    error = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        if username:

            query = """
            MATCH (u:User {name: $username})
                  -[:RECEIVED]->(m:Message)
                  -[:MENTIONS_PHONE]->(p:Phone)
                  <-[:MENTIONS_PHONE]-(m2:Message)
                  <-[:RECEIVED]-(u2:User)

            WHERE u.name <> u2.name

            RETURN DISTINCT
                m.text AS message,
                m.label AS label,
                p.number AS phone,
                u2.name AS connected_user
            """

            try:

                with driver.session() as session:

                    result = session.run(
                        query,
                        username=username
                    )

                    results = [
                        record.data()
                        for record in result
                    ]

                if results:

                    scam_count = sum(
                        1 for record in results
                        if str(record["label"]).lower() == "scam"
                    )

                    risk_score = min(
                        100,
                        50 + (scam_count * 50)
                    )

                    if risk_score >= 80:
                        risk_level = "HIGH RISK"
                    else:
                        risk_level = "LOW RISK"

                else:
                    risk_level = "NO DATA"

            except Exception as e:

                print("DATABASE ERROR:", e)

                error = (
                    "Unable to connect to the database. "
                    "Please try again later."
                )

                results = None


    return render_template(
        "index.html",
        results=results,
        username=username,
        risk_score=risk_score,
        risk_level=risk_level,
        error=error
    )


if __name__ == "__main__":

    print("Starting ScamGraph...")
    print("Open: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )