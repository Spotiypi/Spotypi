RFID-Spotify-Controller
Dieses Python-Skript ermöglicht es, Spotify mit einer RFID-Karte zu steuern, indem es eine Verbindung zwischen einem RFID-Leser und dem Spotify-Account über die Spotipy-Bibliothek herstellt. Es bietet Funktionen wie das Abspielen von Musik, das Steuern der Wiedergabe und die Lautstärkeregelung durch das Scannen von RFID-Karten.

Voraussetzungen
Raspberry Pi: Das Skript wurde auf einem Raspberry Pi getestet, aber es kann auch auf anderen Geräten mit entsprechenden Anpassungen ausgeführt werden.
Python 3: Stelle sicher, dass Python 3 installiert ist.
Bibliotheken: Du musst die folgenden Python-Bibliotheken installieren:
mfrc522 (für den RFID-Leser)
RPi.GPIO (für die GPIO-Steuerung des Raspberry Pi)
spotipy (für die Spotify-API)
Du kannst die benötigten Bibliotheken mit pip installieren:

bash
Kopieren
Bearbeiten
pip install mfrc522 RPi.GPIO spotipy
Funktionsweise
Das Skript verbindet sich mit einem Spotify-Konto und einem Spotify-fähigen Gerät (z. B. einem Raspberry Pi oder einem anderen Gerät, das Spotify unterstützt). Es liest die RFID-Karten und führt die entsprechende Aktion auf Spotify aus, basierend auf der ID der Karte.

Hauptfunktionen
Wiedergabe starten oder fortsetzen: Das Skript sorgt dafür, dass die Wiedergabe auf einem bestimmten Spotify-Gerät startet oder fortgesetzt wird, wenn das Gerät nicht aktiv ist.
Wiedergabesteuerung: Du kannst mit RFID-Karten die Wiedergabe pausieren, fortsetzen, zum nächsten Track wechseln oder zum vorherigen zurückkehren.
Lautstärkeregelung: Ändere die Lautstärke, indem du RFID-Karten scannst, die mit den Befehlen volume_up oder volume_down verknüpft sind.
Musik abspielen: Du kannst Songs, Alben oder Playlists starten, indem du spezifische RFID-Karten scannst, die mit den entsprechenden Spotify-URIs verknüpft sind.
Steuerung über RFID
Spotify-URI: Jede RFID-Karte kann einem spezifischen Spotify-Track, -Album oder -Playlist zugeordnet werden.
Kontrollbefehle: Karten können auch Befehle wie pause, resume, skip, back, volume_up, und volume_down enthalten, um die Wiedergabe zu steuern.
Installation
Spotify Developer Account: Erstelle ein Spotify Developer-Konto, wenn du noch keines hast, und registriere eine Anwendung, um deine CLIENT_ID und CLIENT_SECRET zu erhalten. Diese Werte müssen im Skript angegeben werden.

Einrichtung des RFID-Lesers: Schließe den MFRC522 RFID-Leser an deinen Raspberry Pi an. Die Pinbelegung des RFID-Lesers muss in der mfrc522-Bibliothek korrekt konfiguriert sein.

Verbindung zu deinem Spotify-Konto: Das Skript verwendet OAuth, um Zugriff auf dein Spotify-Konto zu erhalten. Beim ersten Ausführen des Skripts wirst du aufgefordert, dich bei Spotify anzumelden und Zugriff zu gewähren.

Konfiguration: Trage deine DEVICE_ID, CLIENT_ID, CLIENT_SECRET und die MAC-Adresse deines Spotify-Geräts in das Skript ein. Die MAC-Adresse ist erforderlich, um das Gerät über Wake-on-LAN zu wecken, falls es nicht aktiv ist.

Nutzung
Lade das Skript auf deinem Raspberry Pi oder einem anderen kompatiblen Gerät.
Stelle sicher, dass alle erforderlichen Bibliotheken installiert sind.
Führe das Skript aus:
bash
Kopieren
Bearbeiten
python3 rfid_spotify_controller.py
Scanne RFID-Karten, um die Wiedergabe zu steuern.
Beispiel für eine RFID-Datenbank
Die RFID-Datenbank im Skript (rfid_to_spotify) enthält Zuordnungen von RFID-Karten zu Spotify-URI-Strings oder Steuerbefehlen:

python
Kopieren
Bearbeiten
rfid_to_spotify = {
    '1234567890': 'spotify:track:2vSLxBSZoK0eha4AuhZlXV',  # Beispiel für Track
    '9876543210': 'control:pause',  # Pausieren
    '1122334455': 'control:skip',   # Nächster Track
    # Weitere Einträge hier...
}
Beispiel für Befehle
Spotify-URI: 'spotify:track:2vSLxBSZoK0eha4AuhZlXV' (Startet den Track mit der angegebenen URI)
Steuerbefehle:
control:pause → Pausiert die Wiedergabe
control:resume → Setzt die Wiedergabe fort
control:skip → Überspringt zum nächsten Track
control:volume_up → Erhöht die Lautstärke
control:volume_down → Verringert die Lautstärke
Fehlerbehebung
Spotify-Gerät nicht gefunden: Überprüfe, ob dein Spotify-Gerät eingeschaltet und mit dem Internet verbunden ist.
Fehler bei der Authentifizierung: Stelle sicher, dass die CLIENT_ID und CLIENT_SECRET korrekt sind und du die richtigen Berechtigungen erteilt hast.
Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die LICENSE für weitere Details.
