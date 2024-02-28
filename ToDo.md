1. **Opprett Docker Secrets:** Bruk Docker CLI til å opprette Docker Secrets for TLS-sertifikatet og nøkkelen. Du kan gjøre dette ved å kjøre følgende kommandoer:


```bash
$ echo "innholdet_av_tls_cert.pem" | docker secret create tls_cert -
$ echo "innholdet_av_tls_key.pem" | docker secret create tls_key -


2. **Oppdater oppstartskriptet for Flask-appen:** Oppdater oppstartskriptet for Flask-appen din for å laste inn TLS-sertifikatet og nøkkelen fra Docker Secrets. Du kan bruke Docker SDK for Python til å hente secret-verdiene. For eksempel:

```python
import docker
client = docker.from_env()

# Hent TLS-sertifikat og nøkkel fra Docker Secrets
tls_cert = client.secrets.get('tls_cert').data.decode('utf-8')
tls_key = client.secrets.get('tls_key').data.decode('utf-8')

# Angi stien til SSL-sertifikatet og nøkkelen
ssl_cert = '/run/secrets/tls_cert'
ssl_key = '/run/secrets/tls_key'

Du må sørge for at Flask-appen din har tilgang til Docker Daemon API for å kunne hente Docker Secrets på denne måten.

Start Flask-appen: Start Flask-appen din som vanlig, og den vil nå bruke TLS-sertifikatet og nøkkelen som er hentet fra Docker Secrets.
Ved å følge disse trinnene, vil du integrere Docker Secrets for å beskytte private nøkler for TLS i din Flask-applikasjon som kjører i Docker-containere, uten behov for Docker Compose. Dette gir en sikker måte å administrere sensitive data på i Docker-miljøet ditt.
