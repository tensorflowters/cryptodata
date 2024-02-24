FROM python:3.11.8

# Install dependencies
RUN apt-get update
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    firefox-esr \
    gcc \
    libc-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*


# Create application directory
RUN mkdir /srv/app
WORKDIR /srv/app

# Copy application files
COPY ./sentiment_analysis .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry config installer.max-workers 10 \
    && poetry install --only ai,db,kafka,scraper --no-interaction --no-ansi --no-root