# Abfahrtsmonitor

## Übersicht

Dieser Leitfaden beschreibt, wie man einen Abfahrtsmonitor für eine bestimmte Haltestelle erstellt, der auf einem kleinen OLED-Display anstatt eines Browsers im Kiosk-Modus angezeigt wird. Da es keine API von der KVB gibt, wird ein Headless-Browser verwendet, um die Echtzeit-IST-Daten von der VRS-Seite zu extrahieren.

## Anforderungen

Man kann sich auf der VRS-Seite einen eigenen Abfahrtsmonitor für eine Haltestelle erstellen, den man z.B. in einem Browser im Kiosk-Mode zur Verfügung stellen kann. Allerdings wollen wir ein kleines OLED Display verwenden und da es keine andere Möglichkeit gibt an die Echtzeit-IST-Daten zu kommen. Es gibt **keine** API von der KVB.
Man bekommt dann einen Link zugesendet, den man im Script hinterlegen kann, welcher durch den Headless Browser geöffnet wird. Daraus kann man sich die relevanten Daten holen.

## Installation der notwendigen Pakete

Installiere die notwendigen Pakete mit folgendem Befehl:

```bash
sudo apt install swig python3-dev python3-setuptools python3-pip python3-pil python3-numpy python3-smbus python3-spidev p7zip-full python3-selenium
```

## Einrichtung des Displays

Lade und installiere die LG-Display-Treiber:

```bash
wget https://github.com/joan2937/lg/archive/master.zip
unzip master.zip
cd lg-master/
make install
```

## Ausführen des Skripts

Verwende den folgenden Befehl, um das Skript mit der URL des Abfahrtsmonitors und der gewünschten Liniennummer zu starten:

```bash
python kvb-abfahrt.py --url "https://www.vrs.de/am/s/XXX" --line "18" --log
```

## Erstellen eines systemd-Dienstes

### 1. Erstellen der Service-Datei

Erstelle eine neue Datei unter `/etc/systemd/system/kvb-abfahrt.service` mit folgendem Inhalt:

```ini
[Unit]
Description=KVB Abfahrtsmonitor Display Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/kvb-abfahrt.py --url "https://www.vrs.de/am/s/XXX" --line "18" --log
WorkingDirectory=/opt/kvb-abfahrt
StandardOutput=journal
StandardError=journal
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
```

Passe den Pfad zum Skript und die Arbeitsverzeichnisse entsprechend an.

### 2. Neuladen und Starten des Dienstes

Lade systemd neu und starte den Dienst:

```bash
sudo systemctl daemon-reload
sudo systemctl start kvb-abfahrt.service
sudo systemctl enable kvb-abfahrt.service
```

### 3. Überprüfen des Dienststatus

Überprüfe den Dienststatus, um sicherzustellen, dass er läuft:

```bash
sudo systemctl status kvb-abfahrt.service
```

Mit dieser Anleitung kannst du sicherstellen, dass dein Abfahrtsmonitor korrekt eingerichtet ist und beim Systemstart automatisch ausgeführt wird.
