# ScamGraph

A graph-based scam network investigation application built with Flask and CognoDB.

## Project idea

ScamGraph investigates how users can be connected through suspicious messages and shared phone numbers. Instead of viewing data as isolated rows, the application traverses relationships in a graph.

Example:

```text
(User:Hemanthi)
      |
   RECEIVED
      v
(Message: scam)
      |
 MENTIONS_PHONE
      v
(Phone:+919876543210)
      ^
 MENTIONS_PHONE
      |
(Message: scam)
      ^
   RECEIVED
      |
(User:Ravi)
```

## Why a graph database?

A graph database is useful because the important part of this problem is the relationship between entities. A multi-hop query can start with a user, find a message, find a shared phone number, and then find other users connected to that same phone number.

This traversal is naturally expressed as:

```text
User -> Message -> Phone <- Message <- User
```

## Data model

### Nodes

- `User`
  - `name`
- `Message`
  - `text`
  - `label`
- `Phone`
  - `number`

### Relationships

- `(User)-[:RECEIVED]->(Message)`
- `(Message)-[:MENTIONS_PHONE]->(Phone)`

## Main multi-hop query

The application searches for a user and follows relationships to messages and shared phone numbers:

```cypher
MATCH (u:User)
WHERE toLower(u.name) = toLower($username)

OPTIONAL MATCH (u)-[:RECEIVED]->(m:Message)
OPTIONAL MATCH (m)-[:MENTIONS_PHONE]->(p:Phone)
OPTIONAL MATCH (p)<-[:MENTIONS_PHONE]-(m2:Message)
OPTIONAL MATCH (other:User)-[:RECEIVED]->(m2)

WHERE other IS NULL
   OR toLower(other.name) <> toLower(u.name)

RETURN DISTINCT
    coalesce(m.text, "") AS message,
    coalesce(m.label, "unknown") AS label,
    coalesce(p.number, "Not available") AS phone,
    other.name AS connected_user
```

The query is parameterized using `$username`.

## Features

- Search for a user
- Find scam or non-scam messages
- Find shared phone numbers
- Discover connected users through graph traversal
- Calculate a simple network risk score
- Show empty and error states
- Keep database credentials in environment variables

## Technology stack

- Python
- Flask
- CognoDB
- openCypher
- Official Neo4j Python driver
- HTML and CSS

## Setup

### 1. Create and activate a virtual environment (optional)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env`

Copy `.env.example` to `.env` and add your real CognoDB connection details:

```text
COGNODB_URI=bolt+s://your-real-instance.databases.cognodb.cloud
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=your-real-password
```

Do not commit `.env` to GitHub.

### 4. Load the seed data

```bash
python seed_data.py
```

Expected output:

```text
Seed data loaded successfully.
```

### 5. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Demo test cases

### Hemanthi

Expected: scam message, shared phone number, and connection to Ravi.

### Ravi

Expected: scam message, the same shared phone number, and connection to Hemanthi.

### Priya

Expected: non-scam message and low risk.

### UnknownUser

Expected: no investigation results.

## Project structure

```text
ScamGraph/
├── app.py
├── database.py
├── seed_data.py
├── requirements.txt
├── .env                 # not committed
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```
## Screen Recording

A short screen recording demonstrating the ScamGraph application:

[▶ Watch the Live Recording](./Live%20recording.mp4)
## Screenshots

Add screenshots of:

1. Home page
2. Hemanthi investigation result
3. Unknown user / empty state

## Notes

This project uses realistic seed data only for demonstration. The risk score is a simple rule-based demonstration score based on scam labels and graph connections.
