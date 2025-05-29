import json
import textwrap

from fastapi import FastAPI, HTTPException, Request
import socket
import logging

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TCP_IP = "127.0.0.1"
TCP_RECIEVER_PORT = 5175
API_PORT = 8080
INPUT_BUFF_SIZE = 8

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_tcp_data(message: str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_IP, TCP_RECIEVER_PORT))
            if len(message) > INPUT_BUFF_SIZE:
                    split_list = textwrap.wrap(message, INPUT_BUFF_SIZE)
                    for part in split_list:
                        part = bytes(part, 'utf-8')
                        s.sendall(part)
                    data = s.recv(1024)
                    print('Received', repr(data))
            else:
                    message = bytes(message, 'utf-8')
                    s.sendall(message)
                    data = s.recv(1024)
                    print('Received', repr(data))

        return data
    except Exception as e:
        logger.error(f"Ошибка установления соединения TCP: {e}")


@app.post("/")
async def handle_post(request: Request):
    try:
        data = await request.json()
        cat_query = data.get("cat_query")

        if not cat_query:
            raise ValueError("Параметр 'cat_query' отсутствует в запросе")

        cat_response = send_tcp_data(cat_query)

        res = {"status": "success", "message": cat_response}

        return res

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Неверный JSON формат")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=API_PORT)