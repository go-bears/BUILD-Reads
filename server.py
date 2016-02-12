import os
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

    # app config for Cloud9
    # app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))