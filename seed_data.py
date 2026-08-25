from database import driver

query = """
MATCH (n)
DETACH DELETE n
"""

with driver.session() as session:
    session.run(query)

    session.run(
        """
        CREATE
        (h:User {name: "Hemanthi"}),
        (r:User {name: "Ravi"}),
        (a:User {name: "Anil"}),
        (s:User {name: "Suresh"}),

        (m1:Message {
            text: "Congratulations! You won a prize. Click the link now.",
            label: "scam"
        }),

        (m2:Message {
            text: "You have won ₹50,000. Share your bank details.",
            label: "scam"
        }),

        (m3:Message {
            text: "Hello! Let's meet tomorrow.",
            label: "not_scam"
        }),

        (m4:Message {
            text: "Urgent! Your account will be blocked. Verify now.",
            label: "scam"
        }),

        (p1:Phone {
            number: "+919876543210"
        }),

        (p2:Phone {
            number: "+919123456789"
        }),

        (h)-[:RECEIVED]->(m1),
        (r)-[:RECEIVED]->(m2),
        (a)-[:RECEIVED]->(m3),
        (s)-[:RECEIVED]->(m4),

        (m1)-[:MENTIONS_PHONE]->(p1),
        (m2)-[:MENTIONS_PHONE]->(p1),

        (m3)-[:MENTIONS_PHONE]->(p2),
        (m4)-[:MENTIONS_PHONE]->(p2)
        """
    )

print("Seed data added successfully!")

driver.close()