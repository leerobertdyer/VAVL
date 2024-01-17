FROM python:3.9.6-slim

RUN apt-get update && apt-get install -y chromium
ENV CHROMIUM_EXECUTABLE_PATH /usr/bin/chromium

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcb1 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2

RUN playwright install

EXPOSE 80

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]


