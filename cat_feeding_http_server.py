import json
import textwrap

from fastapi import FastAPI, HTTPException, Request
import socket
import logging

from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

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

UDP_IP = "127.0.0.1"
UDP_REVEIVER_PORT = 5174
API_PORT = 7070
INPUT_BUFF_SIZE = 8

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_udp_message(message: str):
    """Отправка сообщения через UDP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, 7071))
        data, addr = '', ''
        if len(message) > INPUT_BUFF_SIZE:
            split_list = textwrap.wrap(message, INPUT_BUFF_SIZE)
            split_list = [split_list[i] + '~' + str(i + 1) if i != len(split_list) - 1 else split_list[i] for i in
                          range(len(split_list))]
            for part in split_list:
                print(part)
                part = bytes(part, 'utf-8')
                sock.sendto(part, (UDP_IP, UDP_REVEIVER_PORT))
                data, addr = sock.recvfrom(1024)
                print("cat answer: %s" % data)
        else:
            message = bytes(message, 'utf-8')
            sock.sendto(message, (UDP_IP, UDP_REVEIVER_PORT))
            data, addr = sock.recvfrom(1024)
            print("cat answer: %s" % data)
        sock.close()
        return data
    except Exception as e:
        logger.error(f"Ошибка отправки UDP: {e}")


@app.post("/")
async def handle_post(request: Request):
    try:
        data = await request.json()
        cat_query = data.get("cat_query")

        if not cat_query:
            raise ValueError("Параметр 'cat_query' отсутствует в запросе")

        cat_response = send_udp_message(cat_query)

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