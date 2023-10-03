import uvicorn

if __name__ == "__main__":
    uvicorn.run("core.core:app", reload=True)