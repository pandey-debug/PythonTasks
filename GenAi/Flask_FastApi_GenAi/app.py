from flask import Flask, render_template, request, Response, stream_with_context
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

FASTAPI_URL = "http://localhost:8000/generate"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "").strip()

    def generate():

        try:
            response = requests.post(
                FASTAPI_URL,
                json={"prompt": question},
                stream=True
            )

            for chunk in response.iter_lines():

                if chunk:
                    yield chunk.decode("utf-8") + "\n"

        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(
        stream_with_context(generate()),
        content_type="text/plain"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)