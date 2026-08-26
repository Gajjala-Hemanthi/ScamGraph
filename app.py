from flask import Flask, render_template, request
from database import get_driver

app = Flask(__name__)


def calculate_risk(records):
    if not records:
        return 0, "NO DATA"

    scam_count = sum(
        1 for r in records
        if str(r["label"]).lower() == "scam"
    )

    connections = {
        r["connected_user"]
        for r in records
        if r["connected_user"]
    }

    if scam_count >= 2 or (scam_count >= 1 and connections):
        return 100, "HIGH RISK"
    elif scam_count >= 1:
        return 70, "MEDIUM RISK"

    return 20, "LOW RISK"


@app.route("/", methods=["GET", "POST"])
def index():

    results = None
    username = ""
    risk_score = 0
    risk_level = ""
    error = None

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        if username:

            query = """
            MATCH (u:User)
            WHERE toLower(u.name) = toLower($username)

            OPTIONAL MATCH (u)-[:RECEIVED]->(m:Message)
            OPTIONAL MATCH (m)-[:MENTIONS_PHONE]->(p:Phone)

            CALL {
                WITH p, u

                OPTIONAL MATCH
                    (p)<-[:MENTIONS_PHONE]-(m2:Message)
                    <-[:RECEIVED]-(other:User)

                WHERE other <> u

                RETURN collect(DISTINCT other.name) AS connected_users
            }

            RETURN DISTINCT
                coalesce(m.text, "") AS message,
                coalesce(m.label, "unknown") AS label,
                coalesce(p.number, "Not available") AS phone,
                CASE
                    WHEN size(connected_users) > 0
                    THEN connected_users[0]
                    ELSE NULL
                END AS connected_user
            """

            try:
                driver = get_driver()

                with driver.session() as session:

                    results = [
                        record.data()
                        for record in session.run(
                            query,
                            username=username
                        )
                    ]

                results = [
                    r for r in results
                    if r["message"]
                    or r["phone"] != "Not available"
                ]

                risk_score, risk_level = calculate_risk(results)

                driver.close()

            except Exception as e:

                print("DATABASE ERROR:", e)

                results = []
                error = (
                    "Database connection failed. "
                    "Please check the CognoDB instance and try again."
                )

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