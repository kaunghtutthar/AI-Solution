from app import create_app

app = None

try:
    app = create_app()
except Exception as e:
    print("APP FAILED TO START:", e)
    raise

if __name__ == "__main__":
    app.run(debug=True)
