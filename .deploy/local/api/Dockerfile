FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip
RUN if [ ${MODE} = prod ]; \
    then pip install -r requirements/prod.txt; \
    else pip install -r requirements/dev.txt; \
    fi

