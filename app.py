import os
from dotenv import load_dotenv
from app import create_app

# 載入環境變數
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
