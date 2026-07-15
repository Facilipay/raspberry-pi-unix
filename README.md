# Raspberry Pi UNIX Clock

Affiche le timestamp UNIX et l'heure sur un ecran LCD 20x4.

## Materiel
- Raspberry Pi 3
- Ecran LCD 20x4 (RoHS 2004A)
- Adafruit USB & Serial RGB Character LCD Backpack

## Installation
pip3 install pyserial

## Lancement
python3 clock.py

## Lancement automatique
Ajouter dans /etc/rc.local avant exit 0 :
python3 /home/pi/clock.py &

## Note
Regler l'heure manuellement au branchement :
sudo date -s "YYYY-MM-DD HH:MM:SS"
