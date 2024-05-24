# Abfahrtsmonitor

## Requirements

Man kann sich auf der VRS-Seite einen eigenen Abfahrtsmonitor für eine Haltestelle erstellen, den man z.B. in einem Browser im Kiosk-Mode zur Verfügung stellen kann. Allerdings wollen wir ein kleines OLED Display verwenden und da es keine andere Möglichkeit gibt an die echtzeit IST-Daten zu kommen. Es gibt **keine** API von der KVB...
Man bekommt dann einen Link zugesendet, den man im Script hinterlegen kann welcher durch den Headless browser (danke an die Entwickler, die java nehmen mussten...) geöffnet wird. Darauas kann man sich die relevanten Daten holen.

### Packages

```bash
apt install swig python3-dev python3-setuptools python3-pip python3-pil python3-numpy python3-smbus python3-spidev p7zip-full python3-selenium
```

### Display

```bash
wget https://github.com/joan2937/lg/archive/master.zip
unzip master.zip
cd lg-master/
make install
```

## Service starten

```bash
python oled_display.py --url "https://www.vrs.de/am/s/XXX" --line "18" --log
```
