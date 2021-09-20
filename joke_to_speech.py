import asyncio
import json
from sys import stderr
from gtts import gTTS
from pathlib import Path
import httpx

URL = "https://v2.jokeapi.dev/joke/Any?type=single"


async def get_call() -> dict:
    deserialized_json = {}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
            assert response.status_code == 200
            deserialized_json = json.loads(response.text)
    except AssertionError:
        print("Error calling {}. HTTP status code: {}".format(URL, response.status_code), file=stderr)
        exit(1)
    except json.decoder.JSONDecodeError as e:
        print("JSON decode error: {}".format(e), file=stderr)
        exit(1)
    return deserialized_json


def joke_to_mp3(joke_str, joke_id) -> None:
    path_file = "mp3s/joke-{}.mp3".format(joke_id)
    mp3_file_path = Path(path_file)
    if mp3_file_path.is_file():
        print("This joke ID already exists")
        return
    try:
        tts = gTTS(joke_str, lang='en')
        with open(path_file, "wb") as mp3:
            tts.write_to_fp(mp3)
    except Exception as e:
        print(e, file=stderr)
        exit(1)


async def main() -> None:
    joke = await get_call()
    joke_str = joke["joke"]
    joke_id = joke["id"]
    joke_to_mp3(joke_str, joke_id)


if __name__ == "__main__":
    asyncio.run(main())
