from fastapi import FastAPI
import uvicorn
import requests
import json

app = FastAPI()


@app.get("/")
def test_retry_request():
    response = request_retry('get', 'http://jsonplaceholder.typicode.com/users/5', {})
    return json.loads(response.text)


def token():
    return 'Bearer token'


def request_retry(method, url, payload, _header=None):
    counter = 0

    while True:

        try:
            headers = {
                'Accept': 'application/json',
                'Authorization': token()
            }

            if _header:
                for key, value in _header.items():
                    headers[key] = value

            response = requests.request(method, url, headers=headers, data=payload)

            # Return request object on success
            if response.status_code == 200:
                return response

            if response.status_code == 401:
                token()

            counter += 1

            # set max retry
            if counter == 5:
                print(f"Failed to connect. \nError code = {response.status_code}\nError text: {response.text}")
                break

            print(f'Failed request. Error code: {response.status_code}. Trying again...')

        except Exception as ex:
            print(ex)
            return request_retry(method, url, payload, _header)
    return request_retry(method, url, payload, _header)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)
