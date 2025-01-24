#!/usr/bin/env python
import socket
import struct
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID = "id"  # Deine Spotify-Geräte-ID
CLIENT_ID = "id"  # Deine Spotify-Client-ID
CLIENT_SECRET = "id" 

# Funktion zum Wecken des Geräts (Wake-on-LAN)
def wake_on_lan(mac_address):
    if len(mac_address) == 17:
        sep = mac_address[2]
        mac_address = mac_address.replace(sep, '')
    mac_bytes = bytes.fromhex(mac_address)
    packet = b'\xff' * 6 + mac_bytes * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(packet, ('<broadcast>', 9))

# Funktion zum Übertragen der Wiedergabe, wenn kein Gerät aktiv ist
def transfer_playback(sp, device_id):
    devices = sp.devices()
    if devices['devices']:
        active_device = None
        for device in devices['devices']:
            if device['is_active']:
                active_device = device
                break
        if active_device is None:
            print("Kein aktives Gerät. Versuche, das Gerät zu aktivieren...")
            sp.transfer_playback(device_id=device_id, force_play=True)
        else:
            print(f"Aktives Gerät gefunden: {active_device['name']}.")
    else:
        print("Keine Geräte verfügbar. Versuche, die Wiedergabe zu übertragen...")
        sp.transfer_playback(device_id=device_id, force_play=True)

# RFID-Datenbank mit zusätzlichen Steuerungsfunktionen
rfid_to_spotify = {

    RFID: 'spotify:track:2vSLxBSZoK0eha4AuhZlXV',  # Song
    

    # (Hier die gleichen RFID-Einträge wie zuvor)
    RFID: 'control:pause',  # Pause
    RFID: 'control:resume', # Wiedergabe fortsetzen
    RFID: 'control:skip',   # Nächster Song
    RFID: 'control:back',   # Vorheriger Song
    RFID: 'control:volume_up',   # Lauter
    RFID: 'control:volume_down'  # Leiser
}

mac_address = "mac-adresse"  # MAC-Adresse deines Spotify-Geräts hier einfügen
last_rfid = None  # Zuletzt gescanntes RFID zur Vermeidung von Dopplungen

def main():
    global last_rfid  # Deklarieren der globalen Variable
    try:
        reader = SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://localhost:8080",
            scope="user-read-playback-state,user-modify-playback-state",
            cache_path="/home/pi/Desktop/RFIDPLAYER/spotify_token.json"))

        print("Warten auf RFID-Scan...")
        while True:
            rfid_id = reader.read()[0]
            
            # Prüfen, ob die gleiche Karte nicht doppelt hintereinander gescannt wird
            if rfid_id != last_rfid:
                last_rfid = rfid_id
                print(f"Neue Karte erkannt: {rfid_id}")

                # Wake-on-LAN senden, um das Gerät aufzuwecken
                wake_on_lan(mac_address)

                # Wiedergabe auf das angegebene Gerät übertragen
                transfer_playback(sp, DEVICE_ID)

                # Überprüfen, ob die RFID-Karte mit einer Spotify-URI oder Steuerungsfunktion übereinstimmt
                if rfid_id in rfid_to_spotify:
                    action = rfid_to_spotify[rfid_id]

                    # Steuerungsfunktionen
                    if action.startswith('control:'):
                        control_command = action.split(':')[1]
                        if control_command == 'pause':
                            print("Wiedergabe pausieren...")
                            sp.pause_playback(device_id=DEVICE_ID)
                        elif control_command == 'resume':
                            print("Wiedergabe fortsetzen...")
                            sp.start_playback(device_id=DEVICE_ID)
                        elif control_command == 'skip':
                            print("Nächster Track...")
                            sp.next_track(device_id=DEVICE_ID)
                        elif control_command == 'back':
                            print("Vorheriger Track...")
                            sp.previous_track(device_id=DEVICE_ID)
                        elif control_command == 'volume_up':
                            current_volume = sp.current_playback()['device']['volume_percent']
                            new_volume = min(current_volume + 10, 100)  # Lautstärke um 10 erhöhen
                            print(f"Lautstärke erhöhen: {new_volume}%")
                            sp.volume(new_volume, device_id=DEVICE_ID)
                        elif control_command == 'volume_down':
                            current_volume = sp.current_playback()['device']['volume_percent']
                            new_volume = max(current_volume - 10, 0)  # Lautstärke um 10 verringern
                            print(f"Lautstärke verringern: {new_volume}%")
                            sp.volume(new_volume, device_id=DEVICE_ID)
                    else:
                        # Prüfen, ob der gewünschte Inhalt bereits läuft, um doppeltes Starten zu vermeiden
                        current_playback = sp.current_playback()
                        if current_playback and current_playback['is_playing'] and current_playback['context']:
                            current_uri = current_playback['context'].get('uri')
                            if current_uri == action:
                                print("Inhalt wird bereits abgespielt, kein Neustart erforderlich.")
                                continue  # Überspringt den Startbefehl, wenn der Inhalt bereits läuft

                        # Spotify-Inhalt abspielen
                        if action.startswith('spotify:track'):
                            print(f"Spiele Track: {action}")
                            sp.start_playback(device_id=DEVICE_ID, uris=[action])
                        elif action.startswith('spotify:album') or action.startswith('spotify:playlist'):
                            print(f"Spiele Album/Playlist: {action}")
                            try:
                                sp.start_playback(device_id=DEVICE_ID, context_uri=action)
                            except spotipy.exceptions.SpotifyException as e:
                                print(f"Fehler beim Abspielen des Inhalts: {e}")
            else:
                print(f"Karte {rfid_id} bereits ausgeführt, auflegen für neuen Scan...")

            # Reduziere die Zeitverzögerung
            sleep(0.5)

    except Exception as e:
        print(f"Fehler aufgetreten: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()                  
