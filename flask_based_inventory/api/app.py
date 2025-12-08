from flask import Flask, request, jsonify
from db_connection import get_db_connection
import google.generativeai as genai

# -----------------------------------------
# Configure Gemini API Key
# -----------------------------------------
genai.configure(api_key="Api-key")

# Choose a supported model (safer + fast)
MODEL_NAME = "models/gemini-2.5-flash"

app = Flask(__name__)

# -----------------------------------------
# Helper: Convert NL → SQL (Clean + Safe)
# -----------------------------------------
def generate_sql_from_question(question):
    prompt = f"""
    Convert the following natural language question into a valid
    SQLite SELECT query.

    Table: inventory
    Columns: id, item, description, quantity, location

    Rules:
    - Only generate SELECT queries.
    - No DELETE, UPDATE, INSERT, DROP, ALTER.
    - No markdown format like ```sql.
    - Return a single clean SQL line only.

    Question: "{question}"
    """

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    sql_query = response.text.strip()

    # -----------------------------------------
    # CLEAN SQL: remove markdown ```
    # -----------------------------------------
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```sqlite", "")
    sql_query = sql_query.replace("```", "")
    sql_query = sql_query.strip()

    # Remove extra newlines; keep first valid SQL line
    lines = sql_query.splitlines()
    sql_query = ""
    for line in lines:
        if line.strip():
            sql_query = line.strip()
            break

    # -----------------------------------------
    # SAFETY CHECK
    # -----------------------------------------
    if not sql_query.lower().startswith("select"):
        raise ValueError(f"Unsafe SQL generated! -> {sql_query}")

    return sql_query


# -----------------------------------------
# API: /query?question=...
# -----------------------------------------
@app.route("/query", methods=["GET"])
def query_inventory():
    question = request.args.get("question")

    if not question:
        return jsonify({
            "error": "Please provide a question in the URL. Example: /query?question=Show all laptops"
        }), 400

    try:
        # Convert NL → SQL
        sql = generate_sql_from_question(question)
        print("Generated SQL:", sql)

        # Execute SQL
        conn = get_db_connection()
        rows = conn.execute(sql).fetchall()
        conn.close()

        # Convert rows to JSON
        result = [dict(row) for row in rows]

        return jsonify({
            "question": question,
            "generated_sql": sql,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------
# Home Page
# -----------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Inventory NLP API!",
        "usage_example": "/query?question=Show items with low stock"
    })


if __name__ == "__main__":
    app.run(debug=True)

