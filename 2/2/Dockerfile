
FROM python:2

RUN pip install requests

RUN python -c "import requests; print(requests.get('https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py').text)"

ENV PATH=/root/.poetry/bin/:$PATH

CMD ["python"]