from database import get_driver

driver = get_driver()

queries = [

    "MATCH (n) DETACH DELETE n",

    """
    CREATE (h:User {name: "Hemanthi"}),
           (r:User {name: "Ravi"}),
           (p:User {name: "Priya"}),
           (a:User {name: "Anil"})
    """,

    """
    CREATE (m1:Message {
        text: "Congratulations! You won a prize. Click the link now.",
        label: "scam"
    })
    """,

    """
    CREATE (m2:Message {
        text: "Limited-time reward. Contact this number to claim money.",
        label: "scam"
    })
    """,

    """
    CREATE (m3:Message {
        text: "Good morning! Shall we meet tomorrow?",
        label: "not_scam"
    })
    """,

    """
    CREATE (m4:Message {
        text: "Urgent! Your account will be blocked. Call now.",
        label: "scam"
    })
    """,

    """
    CREATE (ph1:Phone {number: "+919876543210"}),
           (ph2:Phone {number: "+919112223344"})
    """,

    """
    MATCH (h:User {name: "Hemanthi"}),
          (r:User {name: "Ravi"}),
          (p:User {name: "Priya"}),
          (a:User {name: "Anil"}),
          (m1:Message {
              text: "Congratulations! You won a prize. Click the link now."
          }),
          (m2:Message {
              text: "Limited-time reward. Contact this number to claim money."
          }),
          (m3:Message {
              text: "Good morning! Shall we meet tomorrow?"
          }),
          (m4:Message {
              text: "Urgent! Your account will be blocked. Call now."
          }),
          (ph1:Phone {number: "+919876543210"}),
          (ph2:Phone {number: "+919112223344"})

    CREATE (h)-[:RECEIVED]->(m1)
    CREATE (r)-[:RECEIVED]->(m2)
    CREATE (p)-[:RECEIVED]->(m3)
    CREATE (a)-[:RECEIVED]->(m4)

    CREATE (m1)-[:MENTIONS_PHONE]->(ph1)
    CREATE (m2)-[:MENTIONS_PHONE]->(ph1)
    CREATE (m4)-[:MENTIONS_PHONE]->(ph2)
    """
]

try:
    with driver.session() as session:
        for query in queries:
            session.run(query).consume()

    print("Seed data loaded successfully.")

except Exception as e:
    print("SEED DATA ERROR:", e)

finally:
    driver.close()
