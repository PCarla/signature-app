import os
# Sicherstellen, dass die Umgebungsvariablen korrekt gesetzt sind
os.environ['EMAIL_USER'] = 'carla.patzanovsky@gmail.com'
os.environ['EMAIL_PASS'] = 'Re$itaRe$ita71'
# Abrufen der Umgebungsvariablen
email_user = os.getenv('EMAIL_USER')
email_pass = os.getenv('EMAIL_PASS')
# Ausgabe der Umgebungsvariablen (Passwort wird aus Sicherheitsgründen nicht angezeigt)
print(f"EMAIL_USER: {email_user}")
print(f"EMAIL_PASS: {'*' * len(email_pass) if email_pass else 'Not Set'}")

