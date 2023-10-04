import os
from authflowapp import runner, engine, Base
from authflowapp.config import SECRET_KEY, DATABASE_URI



os.environ["SECRET_KEY"] = os.getenv("SECRET_KEY", SECRET_KEY)
os.environ["DATABASE_URI"] = os.getenv("DATABASE_URI", DATABASE_URI)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(runner, debug=True)