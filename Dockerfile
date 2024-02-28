# Bruk en baseimage med støtte for Python
FROM python:3.9-slim

# Sett arbeidskatalogen i kontaineren
WORKDIR /

# Kopier inn nødvendige filer og mapper til kontaineren
COPY . .

# Kopier inn SSL-sertifikat og nøkkel til kontaineren
COPY cert.pem .
COPY key.pem .

# Installer avhengigheter
RUN pip install --no-cache-dir flask requests

# Angi miljøvariabler for Flask-appen
ENV FLASK_APP=new-wan-store-https.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=443

# Angi stien til SSL-sertifikat og nøkkel
ENV SSL_CERT=cert.pem
ENV SSL_KEY=key.pem

# Bygg og installer SSL-bibliotek
RUN apt-get update && apt-get install -y libssl-dev && rm -rf /var/lib/apt/lists/*

# Eksponer porten for Flask-appen
EXPOSE 443

# Kjør Flask-applikasjonen
CMD ["flask", "run", "--cert", "./cert.pem", "--key", "./key.pem"]
