
FROM python:3.7.0b5-slim

RUN pip install requests

RUN python -c "import requests; print(requests.get('https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py').text)" | python

ENV PATH=/root/.poetry/bin/:$PATH

CMD ["python"]