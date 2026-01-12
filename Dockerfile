FROM python

RUN mkdir -p python-testapp

WORKDIR /python-testapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /python-testapp

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "container:app"]
