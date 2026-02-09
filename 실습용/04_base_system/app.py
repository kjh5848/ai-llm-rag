from main import app


if __name__ == "__main__":
    import uvicorn

    print("FastAPI 서버 시작: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
