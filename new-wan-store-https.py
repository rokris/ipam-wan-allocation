from flask import Flask, render_template, request
import base64
import requests
import ssl

app = Flask(__name__)

def sjekk_eksistens(virk_id, vlan, username, password):
    # Konstruerer autentiseringstoken
    credentials = f"{username}:{password}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    # Setter opp header med autentisering
    headers = {
        "Authorization": f"Basic {base64_credentials}"
    }

    # Utfører GET-forespørsel for å sjekke eksistensen av VirkID og Vlan
    response = requests.get(f"https://ngipam.joh.no/wapi/v2.7/network?_return_fields%2B=extattrs&*VirkID={virk_id}&*Vlan={vlan}", headers=headers, verify=False)

    # Sjekker statuskoden
    if response.status_code == 401:
        return "auth_error"
    elif response.status_code == 200:
        data = response.json()
        if data and 'extattrs' in data[0]:
            if data[0]['extattrs'].get('VirkID', {}).get('value') == int(virk_id) and data[0]['extattrs'].get('Vlan', {}).get('value') == int(vlan):
                return "exist"
        else:
            return "not_exist"
    else:
        return f"something_wrong2: {response.status_code}"

def opprett_nytt_nettverk(virk_id, vlan, storename, username, password):
    # Konstruerer autentiseringstoken
    credentials = f"{username}:{password}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    # Setter opp header med autentisering og Content-Type
    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/json"
    }

    # Data for å opprette nytt nettverk
    data = {
        "network": "func:nextavailablenetwork:172.22.128.0/17,default,29",
        "network_view": "default",
        "comment": storename,
        "extattrs": {
            "VirkID": {"value": virk_id},
            "Vlan": {"value": vlan}
        }
    }

    # Utfører POST-forespørsel for å opprette nytt nettverk
    response = requests.post("https://ngipam.joh.no/wapi/v2.7/network?_return_fields%2B=network,members,extattrs", json=data, headers=headers, verify=False)

    # Sjekker statuskoden
    if response.status_code == 201:
        print("Nytt nettverk opprettet.")
        return response.json()["network"]  # Henter network-verdien fra responsen
    else:
        print("Feil ved oppretting av nettverk. Statuskode:", response.status_code)
        return None

# Angi stien til SSL-sertifikatet og nøkkelen
ssl_cert = 'cert.pem'
ssl_key = 'key.pem'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        storename = request.form['storename']
        vlan = 155  # Sett vlan til ønsket fast verdi her
        
        sjekkresultat = sjekk_eksistens(request.form['virk_id'], vlan, username, password)
        
        try:
            virk_id = int(request.form['virk_id'])
        except ValueError:
            result = "Virk ID må være heltall."
            return render_template('index.html', result=result)
        if sjekkresultat == "exist":
            result = "VirkID eksisterer allerede."
        
        elif sjekkresultat == "auth_error":
            result = "Feil brukernavn eller passord"        
        
        elif sjekkresultat == "not_exist":
            network_value = opprett_nytt_nettverk(virk_id, vlan, storename, username, password)
            if network_value:
                result = f"Nytt nettverk opprettet. Network: {network_value}, VirkID: {virk_id}, Vlan: {vlan}, Butikknavn: {storename}"
            else:
                result = "Feil ved oppretting av nettverk."
        else:
            result = sjekkresultat
                
        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    # Opprett et SSL-kontekstobjekt
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(ssl_cert, ssl_key)

    # Start Flask-appen med HTTPS
    app.run(debug=True, ssl_context=context)
