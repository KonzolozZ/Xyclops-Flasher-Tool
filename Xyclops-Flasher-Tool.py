import os
import sys
import re
import time
import math
import serial
import serial.tools.list_ports
import threading
from datetime import datetime
import requests
import webbrowser

# --- Többnyelvű szövegek ---
translations = {
    'hu': {
        'lang_name': 'Magyar',
        'select_language': 'Válassz nyelvet:',
        'main_title': 'Xyclops Flasher Tool v1.1 (250523)',
        'pandafix': 'Pandafix',
        'pandafix_url': 'pandafix.hu',
        'thanks': 'Köszönet Prehistoricman-nek a Githubra feltöltött munkájáért: github.com/Prehistoricman/Xbox_SMC',
        'warning1': 'Csak Xbox 1.6 flashelésére használható! Az Xyclops A-B01 IC-t NEM támogatja.',
        'warning2': 'A megfelelő írás/olvasáshoz az AV csatlakozó közelében el kell távolítani az R5M3, R4M10 0Ohm ellenállásokat.',
        'warning3': 'A Xyclops IC 29-es lába DEBUG (3.3V-ra kell beforrasztani).',
        'warning4': 'A 64-es láb a TXD (adapter RX), 63-as az RXD (adapter TX), GND-t is be kell forrasztani.',
        'menu': 'Főmenü:',
        'menu1': '1. Xyclops Dump (kiolvasás)',
        'menu2': '2. Xyclops Write (írás)',
        'menu3': '3. BIOS letöltés',
        'menu4': '4. Támogatás',
        'menu5': '5. Kilépés',
        'support_menu': 'Támogatási lehetőségek:',
        'support1': '1. PayPal',
        'support2': '2. BuyMeaCoffee',
        'support3': '3. Patreon',
        'support4': '4. GitHub',
        'support5': '5. éhezni hagylak',
        'support_opening': 'Megnyitás böngészőben...',
        'select_option': 'Válassz menüpontot:',
        'dump_start': 'BIOS kiolvasás folyamatban...',
        'dump_success': 'Kiolvasás sikeres! ({})',
        'dump_fail': 'Kiolvasás sikertelen!',
        'dump_exists': 'Már létezik dump.bin. Felülírja (f) vagy új néven menti (ú)?',
        'dump_invalid_magic': 'Érvénytelen mágikus fejléc! Sérült vagy már módosított BIOS.',
        'erase_start': 'BIOS törlése folyamatban...',
        'write_start': 'BIOS programozás folyamatban...',
        'write_success': 'Írás sikeres!',
        'write_fail': 'Írás sikertelen!',
        'bin_list': 'Elérhető .bin fájlok (max 256KiB):',
        'no_bin': 'Nincs megfelelő .bin fájl a Bios mappában!',
        'select_bin': 'Válassz fájlt (szám):',
        'warn_no_dump': 'Nincs dump! A BIOS törölve lesz. Erősen ajánlott előbb menteni. Kérsz mentést? (i/n):',
        'warn_erase': 'A BIOS törölve lesz! A folyamat megszakítása adatvesztéssel járhat. Folytatod? (i/n):',
        'write_verification': 'Ellenőrzés folyamatban...',
        'write_verify_success': 'Ellenőrzés sikeres!',
        'write_verify_fail': 'Ellenőrzés sikertelen!',
        'bios_download': 'Letölthető BIOS-ok:',
        'download_success': 'Letöltés sikeres: {}',
        'download_fail': 'Letöltés sikertelen!',
        'bios_list_empty': 'Nincs letölthető BIOS.',
        'log_header': 'Előző műveletek:',
        'log_entry': '{time} - {action} - {result}',
        'exit': 'Kilépés...',
        'invalid_option': 'Érvénytelen választás!',
        'press_enter': 'Nyomj Enter-t a folytatáshoz...',
        'yes': 'i',
        'no': 'n',
        'overwrite': 'f',
        'newname': 'ú',
        'bios_folder': 'Bios/Original dump',
        'bios_folder2': 'Bios',
        'magic': b'   <Copyright 2001-2003 Microsoft, Revision P2L>',
        'anim': '*',
        'back': 'Visszalépés a főmenübe',
    },
    'en': {
        'lang_name': 'English',
        'select_language': 'Select language:',
        'main_title': 'Xyclops Flasher Tool v1.1 (250523)',
        'pandafix': 'Pandafix',
        'pandafix_url': 'pandafix.hu',
        'thanks': 'Thanks to Prehistoricman for the work on Github: github.com/Prehistoricman/Xbox_SMC',
        'warning1': 'Only for flashing Xbox 1.6! Xyclops A-B01 IC is NOT supported.',
        'warning2': 'For correct operation, remove R5M3, R4M10 0 Ohm resistors near the AV connector.',
        'warning3': 'Xyclops IC pin 29 is DEBUG (must be soldered to 3.3V).',
        'warning4': 'Pin 64 = TXD (adapter RX), pin 63 = RXD (adapter TX), GND must be soldered.',
        'menu': 'Main menu:',
        'menu1': '1. Xyclops Dump (read)',
        'menu2': '2. Xyclops Write (write)',
        'menu3': '3. BIOS download',
        'menu4': '4. Support',
        'menu5': '5. Exit',
        'support_menu': 'Support options:',
        'support1': '1. PayPal',
        'support2': '2. BuyMeaCoffee',
        'support3': '3. Patreon',
        'support4': '4. GitHub',
        'support5': '5. I let you starve',
        'support_opening': 'Opening in browser...',
        'select_option': 'Select option:',
        'dump_start': 'BIOS dump in progress...',
        'dump_success': 'Dump successful! ({})',
        'dump_fail': 'Dump failed!',
        'dump_exists': 'dump.bin already exists. Overwrite (o) or save as new (n)?',
        'dump_invalid_magic': 'Invalid magic header! Damaged or modified BIOS.',
        'erase_start': 'Erasing BIOS...',
        'write_start': 'BIOS programming in progress...',
        'write_success': 'Write successful!',
        'write_fail': 'Write failed!',
        'bin_list': 'Available .bin files (max 256KiB):',
        'no_bin': 'No valid .bin files in Bios folder!',
        'select_bin': 'Select file (number):',
        'warn_no_dump': 'No dump! BIOS will be erased. Strongly recommended to backup first. Backup now? (y/n):',
        'warn_erase': 'BIOS will be erased! Do not interrupt the process. Continue? (y/n):',
        'write_verification': 'Verification in progress...',
        'write_verify_success': 'Verification successful!',
        'write_verify_fail': 'Verification failed!',
        'bios_download': 'Downloadable BIOS files:',
        'download_success': 'Download successful: {}',
        'download_fail': 'Download failed!',
        'bios_list_empty': 'No downloadable BIOS.',
        'log_header': 'Previous operations:',
        'log_entry': '{time} - {action} - {result}',
        'exit': 'Exiting...',
        'invalid_option': 'Invalid option!',
        'press_enter': 'Press Enter to continue...',
        'yes': 'y',
        'no': 'n',
        'overwrite': 'o',
        'newname': 'n',
        'bios_folder': 'Bios/Original dump',
        'bios_folder2': 'Bios',
        'magic': b'   <Copyright 2001-2003 Microsoft, Revision P2L>',
        'anim': '*',
        'back': 'Back to main menu',
    },
    'de': {
        'lang_name': 'Deutsch',
        'select_language': 'Sprache auswählen:',
        'main_title': 'Xyclops Flasher Tool v1.1 (250523)',
        'pandafix': 'Pandafix',
        'pandafix_url': 'pandafix.hu',
        'thanks': 'Danke an Prehistoricman für die Arbeit auf Github: github.com/Prehistoricman/Xbox_SMC',
        'warning1': 'Nur für Xbox 1.6! Xyclops A-B01 IC wird NICHT unterstützt.',
        'warning2': 'Für korrekten Betrieb entfernen Sie die 0-Ohm-Widerstände R5M3, R4M10 beim AV-Anschluss.',
        'warning3': 'Pin 29 des Xyclops IC ist DEBUG (an 3.3V anlöten).',
        'warning4': 'Pin 64 = TXD (Adapter RX), Pin 63 = RXD (Adapter TX), GND anlöten.',
        'menu': 'Hauptmenü:',
        'menu1': '1. Xyclops Dump (Lesen)',
        'menu2': '2. Xyclops Write (Schreiben)',
        'menu3': '3. BIOS herunterladen',
        'menu4': '4. Unterstützung',
        'menu5': '5. Beenden',
        'support_menu': 'Unterstützungsmöglichkeiten:',
        'support1': '1. PayPal',
        'support2': '2. BuyMeaCoffee',
        'support3': '3. Patreon',
        'support4': '4. GitHub',
        'support5': '5. Ich lasse dich hungern',
        'support_opening': 'Im Browser öffnen...',
        'select_option': 'Option auswählen:',
        'dump_start': 'BIOS-Auslesen läuft...',
        'dump_success': 'Dump erfolgreich! ({})',
        'dump_fail': 'Dump fehlgeschlagen!',
        'dump_exists': 'dump.bin existiert bereits. Überschreiben (ü) oder neu speichern (n)?',
        'dump_invalid_magic': 'Ungültiger magischer Header! BIOS beschädigt oder verändert.',
        'erase_start': 'BIOS wird gelöscht...',
        'write_start': 'BIOS-Programmierung läuft...',
        'write_success': 'Schreiben erfolgreich!',
        'write_fail': 'Schreiben fehlgeschlagen!',
        'bin_list': 'Verfügbare .bin-Dateien (max 256KiB):',
        'no_bin': 'Keine gültigen .bin-Dateien im Bios-Ordner!',
        'select_bin': 'Datei auswählen (Nummer):',
        'warn_no_dump': 'Kein Dump! Das BIOS wird gelöscht. Backup dringend empfohlen. Jetzt sichern? (j/n):',
        'warn_erase': 'Das BIOS wird gelöscht! Vorgang nicht unterbrechen. Fortfahren? (j/n):',
        'write_verification': 'Verifikation läuft...',
        'write_verify_success': 'Verifikation erfolgreich!',
        'write_verify_fail': 'Verifikation fehlgeschlagen!',
        'bios_download': 'Verfügbare BIOS-Dateien:',
        'download_success': 'Download erfolgreich: {}',
        'download_fail': 'Download fehlgeschlagen!',
        'bios_list_empty': 'Keine BIOS zum Download.',
        'log_header': 'Vorherige Operationen:',
        'log_entry': '{time} - {action} - {result}',
        'exit': 'Beenden...',
        'invalid_option': 'Ungültige Option!',
        'press_enter': 'Drücken Sie Enter zum Fortfahren...',
        'yes': 'j',
        'no': 'n',
        'overwrite': 'ü',
        'newname': 'n',
        'bios_folder': 'Bios/Original dump',
        'bios_folder2': 'Bios',
        'magic': b'   <Copyright 2001-2003 Microsoft, Revision P2L>',
        'anim': '*',
        'back': 'Zurück zum Hauptmenü',
    },
    'fr': {
        'lang_name': 'Français',
        'select_language': 'Choisissez la langue :',
        'main_title': 'Xyclops Flasher Tool v1.1 (250523)',
        'pandafix': 'Pandafix',
        'pandafix_url': 'pandafix.hu',
        'thanks': 'Merci à Prehistoricman pour son travail sur Github : github.com/Prehistoricman/Xbox_SMC',
        'warning1': 'Uniquement pour Xbox 1.6 ! Xyclops A-B01 IC NON supporté.',
        'warning2': 'Pour un fonctionnement correct, retirez les résistances R5M3, R4M10 0 Ohm près du connecteur AV.',
        'warning3': 'La broche 29 du Xyclops IC est DEBUG (à souder au 3.3V).',
        'warning4': 'Broche 64 = TXD (RX adaptateur), 63 = RXD (TX adaptateur), GND à souder.',
        'menu': 'Menu principal :',
        'menu1': '1. Xyclops Dump (lecture)',
        'menu2': '2. Xyclops Write (écriture)',
        'menu3': '3. Téléchargement BIOS',
        'menu4': '4. Soutien',
        'menu5': '5. Quitter',
        'support_menu': 'Options de soutien :',
        'support1': '1. PayPal',
        'support2': '2. BuyMeaCoffee',
        'support3': '3. Patreon',
        'support4': '4. GitHub',
        'support5': '5. Je te laisse mourir de faim',
        'support_opening': 'Ouverture dans le navigateur...',
        'select_option': 'Choisissez une option :',
        'dump_start': 'Lecture du BIOS en cours...',
        'dump_success': 'Lecture réussie ! ({})',
        'dump_fail': 'Lecture échouée !',
        'dump_exists': 'dump.bin existe déjà. Écraser (é) ou enregistrer sous un autre nom (n) ?',
        'dump_invalid_magic': 'En-tête magique invalide ! BIOS endommagé ou modifié.',
        'erase_start': 'Suppression du BIOS en cours...',
        'write_start': 'Programmation du BIOS en cours...',
        'write_success': 'Écriture réussie !',
        'write_fail': 'Écriture échouée !',
        'bin_list': 'Fichiers .bin disponibles (max 256Ko) :',
        'no_bin': 'Aucun fichier .bin valide dans le dossier Bios !',
        'select_bin': 'Choisissez le fichier (numéro) :',
        'warn_no_dump': 'Pas de dump ! Le BIOS sera effacé. Sauvegarde fortement recommandée. Sauvegarder maintenant ? (o/n) :',
        'warn_erase': 'Le BIOS sera effacé ! Ne pas interrompre le processus. Continuer ? (o/n) :',
        'write_verification': 'Vérification en cours...',
        'write_verify_success': 'Vérification réussie !',
        'write_verify_fail': 'Vérification échouée !',
        'bios_download': 'BIOS disponibles :',
        'download_success': 'Téléchargement réussi : {}',
        'download_fail': 'Échec du téléchargement !',
        'bios_list_empty': 'Aucun BIOS à télécharger.',
        'log_header': 'Opérations précédentes :',
        'log_entry': '{time} - {action} - {result}',
        'exit': 'Quitter...',
        'invalid_option': 'Option invalide !',
        'press_enter': 'Appuyez sur Entrée pour continuer...',
        'yes': 'o',
        'no': 'n',
        'overwrite': 'é',
        'newname': 'n',
        'bios_folder': 'Bios/Original dump',
        'bios_folder2': 'Bios',
        'magic': b'   <Copyright 2001-2003 Microsoft, Revision P2L>',
        'anim': '*',
        'back': 'Retour au menu principal',
    },
    'es': {
        'lang_name': 'Español',
        'select_language': 'Seleccione idioma:',
        'main_title': 'Xyclops Flasher Tool v1.1 (250523)',
        'pandafix': 'Pandafix',
        'pandafix_url': 'pandafix.hu',
        'thanks': 'Gracias a Prehistoricman por su trabajo en Github: github.com/Prehistoricman/Xbox_SMC',
        'warning1': '¡Solo para Xbox 1.6! Xyclops A-B01 IC NO es compatible.',
        'warning2': 'Para un funcionamiento correcto, retire las resistencias R5M3, R4M10 de 0 Ohm cerca del conector AV.',
        'warning3': 'El pin 29 del Xyclops IC es DEBUG (debe soldarse a 3.3V).',
        'warning4': 'Pin 64 = TXD (RX adaptador), 63 = RXD (TX adaptador), conectar GND.',
        'menu': 'Menú principal:',
        'menu1': '1. Xyclops Dump (lectura)',
        'menu2': '2. Xyclops Write (escritura)',
        'menu3': '3. Descargar BIOS',
        'menu4': '4. Soporte',
        'menu5': '5. Salir',
        'support_menu': 'Opciones de soporte:',
        'support1': '1. PayPal',
        'support2': '2. BuyMeaCoffee',
        'support3': '3. Patreon',
        'support4': '4. GitHub',
        'support5': '5. Te dejo pasar hambre',
        'support_opening': 'Abriendo en el navegador...',
        'select_option': 'Seleccione opción:',
        'dump_start': 'Volcado de BIOS en curso...',
        'dump_success': '¡Volcado exitoso! ({})',
        'dump_fail': '¡Volcado fallido!',
        'dump_exists': 'dump.bin ya existe. ¿Sobrescribir (s) o guardar como nuevo (n)?',
        'dump_invalid_magic': '¡Encabezado mágico inválido! BIOS dañado o modificado.',
        'erase_start': 'Borrando BIOS...',
        'write_start': 'Programación de BIOS en curso...',
        'write_success': '¡Escritura exitosa!',
        'write_fail': '¡Escritura fallida!',
        'bin_list': 'Archivos .bin disponibles (máx 256KiB):',
        'no_bin': '¡No hay archivos .bin válidos en la carpeta Bios!',
        'select_bin': 'Seleccione archivo (número):',
        'warn_no_dump': '¡No hay dump! El BIOS será borrado. Se recomienda hacer una copia. ¿Hacer copia ahora? (s/n):',
        'warn_erase': '¡El BIOS será borrado! No interrumpa el proceso. ¿Continuar? (s/n):',
        'write_verification': 'Verificación en curso...',
        'write_verify_success': '¡Verificación exitosa!',
        'write_verify_fail': '¡Verificación fallida!',
        'bios_download': 'BIOS disponibles:',
        'download_success': 'Descarga exitosa: {}',
        'download_fail': '¡Descarga fallida!',
        'bios_list_empty': 'No hay BIOS para descargar.',
        'log_header': 'Operaciones previas:',
        'log_entry': '{time} - {action} - {result}',
        'exit': 'Saliendo...',
        'invalid_option': '¡Opción inválida!',
        'press_enter': 'Pulse Enter para continuar...',
        'yes': 's',
        'no': 'n',
        'overwrite': 's',
        'newname': 'n',
        'bios_folder': 'Bios/Original dump',
        'bios_folder2': 'Bios',
        'magic': b'   <Copyright 2001-2003 Microsoft, Revision P2L>',
        'anim': '*',
        'back': 'Volver al menú principal',
    }
}

LANGS = ['hu', 'en', 'de', 'fr', 'es']
log_entries = []

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ascii_logo():
    return r"""
 ____   __   __ _  ____   __   ____  __  _  _ 
(  _ \ / _\ (  ( \(    \ / _\ (  __)(  )( \/ )
 ) __//    \/    / ) D (/    \ ) _)  )(  )  ( 
(__)  \_/\_/\_)__)(____/\_/\_/(__)  (__)(_/\_)
"""

def print_panda_image():
    print(ascii_logo())

def print_header(tr):
    clear()
    print_panda_image()
    print(f"{tr['pandafix']} ({tr['pandafix_url']}) | {tr['main_title']}")
    print()
    print(tr['thanks'])
    print(tr['warning1'])
    print(tr['warning2'])
    print(tr['warning3'])
    print(tr['warning4'])
    print()

def select_language():
    print("Select language / Válassz nyelvet / Sprache auswählen / Choisissez la langue / Seleccione idioma:")
    for idx, code in enumerate(LANGS):
        print(f"{idx+1}. {translations[code]['lang_name']}")
    while True:
        choice = input(">").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(LANGS):
            return LANGS[int(choice)-1]
        else:
            print("Invalid selection!")

def auto_select_port(tr):
    com_ini_file = 'com.ini'
    if os.path.exists(com_ini_file):
        with open(com_ini_file, 'r') as f:
            first_line = f.readline().strip()
            if re.match(r'^COM[1-9][0-9]?$', first_line, re.IGNORECASE):
                print(f"Using port from settings: {first_line}")
                time.sleep(1)
                return first_line
    pattern = re.compile(r"^(USB-?Serial|USB Serial)\b", re.IGNORECASE)
    ports = list(serial.tools.list_ports.comports())
    filtered_ports = [port for port in ports if pattern.search(port.description)]
    def com_number(port):
        match = re.search(r'COM(\d+)', port.device, re.IGNORECASE)
        return int(match.group(1)) if match else float('inf')
    if filtered_ports:
        sorted_ports = sorted(filtered_ports, key=com_number)
        if len(sorted_ports) > 1:
            print("Multiple UART devices found:")
            for port in sorted_ports:
                print(f" {com_number(port)}: {port.device} - {port.description}")
            while True:
                choice = input("\nSelect port (COM number): ").strip()
                if choice.isdigit():
                    chosen = int(choice)
                    matching = [port for port in sorted_ports if com_number(port) == chosen]
                    if matching:
                        selected_port = matching[0].device
                        print(f"\nSelected port: {selected_port}")
                        time.sleep(1)
                        return selected_port
                    else:
                        print("Invalid COM number.")
                else:
                    print("Enter a number.")
        else:
            selected_port = sorted_ports[0].device
            print(f"Auto-selected port: {selected_port} - {sorted_ports[0].description}")
            time.sleep(1)
            return selected_port
    else:
        selected_port = input("Enter COM port (e.g. COM4): ").strip()
        digits = ''.join(filter(str.isdigit, selected_port))
        selected_port = 'COM' + digits if digits else selected_port
        if not selected_port:
            print("No port specified. Exiting.")
            sys.exit(1)
        return selected_port

def log(tr, action, result):
    now = datetime.now().strftime("%H:%M:%S")
    log_entries.append(tr['log_entry'].format(time=now, action=action, result=result))
    if len(log_entries) > 10:
        log_entries.pop(0)

def print_log(tr):
    print(tr['log_header'])
    for entry in log_entries:
        print("  " + entry)
    print()

def dump_filename(tr):
    folder = tr['bios_folder']
    os.makedirs(folder, exist_ok=True)
    base = os.path.join(folder, "dump.bin")
    if not os.path.exists(base):
        return base
    ans = input(tr['dump_exists'] + " ").strip().lower()
    if ans == tr['overwrite']:
        return base
    else:
        i = 2
        while True:
            fname = os.path.join(folder, f"dump{i}.bin")
            if not os.path.exists(fname):
                return fname
            i += 1

def animate(tr, text, stop_event):
    symbols = ['*', '.', 'o', '+', ' ']
    idx = 0
    print(text, end=' ')
    while not stop_event.is_set():
        print('\r' + text + ' |' + symbols[idx % len(symbols)] + '|', end='', flush=True)
        time.sleep(0.2)
        idx += 1
    print('\r' + text + ' | |', flush=True)

def check_magic(fname, tr):
    with open(fname, "rb") as f:
        f.seek(0x100)
        data = f.read(len(tr['magic']))
        return tr['magic'] in data

def xyclops_dump(tr, port_name):
    fname = dump_filename(tr)
    stop_event = threading.Event()
    anim_thread = threading.Thread(target=animate, args=(tr, tr['dump_start'], stop_event))
    anim_thread.start()
    try:
        port = serial.Serial(port_name, 9600, timeout=0.1)
        cmd = 0x15
        synced = False
        for i in range(5):
            port.write(b"o")
            if port.read(2):
                synced = True
                break
        if not synced:
            stop_event.set()
            anim_thread.join()
            print(tr['dump_fail'])
            log(tr, "Dump", tr['dump_fail'])
            input(tr['press_enter'])
            return
        with open(fname, "wb") as outfile:
            for i in range(0, 0x10000, 64):
                port.write([cmd, i >> 8, i & 0xFF, 0])
                response = port.read(1 + 64)
                if not response or response[0] != cmd:
                    stop_event.set()
                    anim_thread.join()
                    print(tr['dump_fail'])
                    log(tr, "Dump", tr['dump_fail'])
                    input(tr['press_enter'])
                    return
                payload = response[1:]
                outfile.write(payload)
                outfile.flush()
        stop_event.set()
        anim_thread.join()
        if check_magic(fname, tr):
            print(tr['dump_success'].format(os.path.basename(fname)))
            log(tr, "Dump", tr['dump_success'].format(os.path.basename(fname)))
        else:
            print(tr['dump_invalid_magic'])
            log(tr, "Dump", tr['dump_invalid_magic'])
        time.sleep(6)
    except Exception as e:
        stop_event.set()
        anim_thread.join()
        print(tr['dump_fail'])
        log(tr, "Dump", tr['dump_fail'])
        input(tr['press_enter'])

def list_bin_files(tr):
    folder = tr['bios_folder2']
    os.makedirs(folder, exist_ok=True)
    files = [f for f in os.listdir(folder) if f.lower().endswith('.bin') and os.path.getsize(os.path.join(folder, f)) <= 256*1024]
    return files

class Xyclops:
    def __init__(self, port):
        self.port = port
    def sync(self):
        self.port.reset_input_buffer()
        synced = False
        for i in range(5):
            self.port.write([0])
            time.sleep(0.03)
            if self.port.in_waiting >= 2:
                self.port.read(2)
                synced = True
                break
            if self.port.in_waiting != 0:
                synced = False
        return synced
    def write_register(self, addr, value, skipread=False):
        self.port.write([0x2B, 0, addr, value])
        if not skipread:
            self.port.read(2)
    def enable_prog(self):
        self.port.write(b"C...")
        self.port.read(2)
    def erase_BIOS(self):
        self.port.write([0x84, 0, 0, 0])
        starttime = time.time()
        attempts = 0
        while self.port.in_waiting != 2:
            time.sleep(0.1)
            attempts += 1
            if attempts > 15:
                return False
        self.port.read(2)
        return True
    def read_BIOS(self, addr):
        self.port.write([0x14, (addr >> 8) & 0xFF, addr & 0xFF, 0])
        response = self.port.read(65)
        return response[1:]
    def high_speed(self):
        self.write_register(0xE9, 0xEC, skipread=True)
        time.sleep(0.03)
        self.port.baudrate = 38400
        self.port.reset_input_buffer()
        return self.sync()
    def low_speed(self):
        self.write_register(0xE9, 0xB0, skipread=True)
        time.sleep(0.03)
        self.port.baudrate = 9600
        self.port.reset_input_buffer()
        return self.sync()
    def exit_debug(self):
        self.port.write(b"B...")
        self.port.read(4)

def xyclops_write(tr, port_name):
    files = list_bin_files(tr)
    while not files:
        print(tr['no_bin'])
        bios_list = [
            ("Cerbios Hybrid V2.4.2 Beta", "https://pandafix.hu/tool/xbox-classic/bios/Cerbios-Hybrid-V2.4.2-Beta.bin"),
            ("Evox M8 v.16", "https://pandafix.hu/tool/xbox-classic/bios/evox-m8-v16.bin"),
            ("Evox M8 Plus v1.6", "https://pandafix.hu/tool/xbox-classic/bios/evox-m8plus-v16.bin"),
            (tr['back'], None)
        ]
        for idx, (name, _) in enumerate(bios_list):
            print(f"{idx+1}. {name}")
        choice = input(tr['select_bin'] + " ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(bios_list):
            idx = int(choice)-1
            if bios_list[idx][1] is None:
                return
            name, url = bios_list[idx]
            folder = tr['bios_folder2']
            os.makedirs(folder, exist_ok=True)
            fname = os.path.join(folder, os.path.basename(url))
            if download_file(url, fname):
                print(tr['download_success'].format(os.path.basename(fname)))
                log(tr, "Download", tr['download_success'].format(os.path.basename(fname)))
            else:
                print(tr['download_fail'])
                log(tr, "Download", tr['download_fail'])
            files = list_bin_files(tr)
        else:
            print(tr['invalid_option'])
    print(tr['bin_list'])
    for idx, fname in enumerate(files):
        print(f"{idx+1}. {fname}")
    while True:
        choice = input(tr['select_bin'] + " ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            selected_file = files[int(choice)-1]
            break
        else:
            print(tr['invalid_option'])
    dump_path = os.path.join(tr['bios_folder'], "dump.bin")
    if not os.path.exists(dump_path):
        ans = input(tr['warn_no_dump'] + " ").strip().lower()
        if ans == tr['yes']:
            xyclops_dump(tr, port_name)
    ans = input(tr['warn_erase'] + " ").strip().lower()
    if ans != tr['yes']:
        print(tr['write_fail'])
        log(tr, "Write", tr['write_fail'])
        input(tr['press_enter'])
        return
    # --- BIOS törlés animáció ---
    stop_event = threading.Event()
    anim_thread = threading.Thread(target=animate, args=(tr, tr['erase_start'], stop_event))
    anim_thread.start()
    try:
        port = serial.Serial(port_name, 9600, timeout=0.15)
        xy = Xyclops(port)
        erase_ok = xy.sync() and xy.enable_prog() is None and xy.erase_BIOS()
        stop_event.set()
        anim_thread.join()
        if not erase_ok:
            print(tr['write_fail'])
            log(tr, "Write", tr['write_fail'])
            input(tr['press_enter'])
            return
        erase_check = xy.read_BIOS(0)
        if erase_check != (b"\xff" * 64):
            print(tr['write_fail'])
            log(tr, "Write", tr['write_fail'])
            input(tr['press_enter'])
            return
        # --- BIOS programozás animáció ---
        stop_event = threading.Event()
        anim_thread = threading.Thread(target=animate, args=(tr, tr['write_start'], stop_event))
        anim_thread.start()
        with open(os.path.join(tr['bios_folder2'], selected_file), "rb") as infile:
            filedata = infile.read()
        padding = (math.ceil(len(filedata) / 64) * 64) - len(filedata)
        if padding != 0:
            filedata = filedata + b"\xff" * padding
        if len(filedata) < 0x1000 or len(filedata) > 0x40000:
            stop_event.set()
            anim_thread.join()
            print(tr['write_fail'])
            log(tr, "Write", tr['write_fail'])
            input(tr['press_enter'])
            return
        if not xy.high_speed():
            stop_event.set()
            anim_thread.join()
            print(tr['write_fail'])
            log(tr, "Write", tr['write_fail'])
            input(tr['press_enter'])
            return
        for i in range(0, len(filedata), 64):
            if i & 0xFFFF == 0:
                xy.write_register(0x91, i >> 16)
            port.write([0x16, (i >> 8) & 0xFF, i & 0xFF])
            port.write(filedata[i:][:64])
            response = port.read(2)
            if not response or response[0] != 0x16:
                stop_event.set()
                anim_thread.join()
                print(tr['write_fail'])
                log(tr, "Write", tr['write_fail'])
                input(tr['press_enter'])
                return
        stop_event.set()
        anim_thread.join()
        # --- Ellenőrzés animáció ---
        stop_event = threading.Event()
        anim_thread = threading.Thread(target=animate, args=(tr, tr['write_verification'], stop_event))
        anim_thread.start()
        verif_failed = False
        for i in range(0, len(filedata), 64):
            if i & 0xFFFF == 0:
                xy.write_register(0x91, i >> 16)
            read = xy.read_BIOS(i)
            if read != filedata[i:][:64]:
                stop_event.set()
                anim_thread.join()
                print(tr['write_verify_fail'])
                log(tr, "Write", tr['write_verify_fail'])
                input(tr['press_enter'])
                verif_failed = True
                break
        stop_event.set()
        anim_thread.join()
        if not verif_failed:
            print(tr['write_success'])
            log(tr, "Write", tr['write_success'])
        else:
            print(tr['write_verify_fail'])
            log(tr, "Write", tr['write_verify_fail'])
        input(tr['press_enter'])
    except Exception as e:
        stop_event.set()
        anim_thread.join()
        print(tr['write_fail'])
        log(tr, "Write", tr['write_fail'])
        input(tr['press_enter'])

def download_file(url, dest):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        with requests.get(url, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as e:
        print("Letöltési hiba:", e)
        return False

def bios_download(tr):
    bios_list = [
        ("Cerbios Hybrid V2.4.2 Beta", "https://pandafix.hu/tool/xbox-classic/bios/Cerbios-Hybrid-V2.4.2-Beta.bin"),
        ("Evox M8 v.16", "https://pandafix.hu/tool/xbox-classic/bios/evox-m8-v16.bin"),
        ("Evox M8 Plus v1.6", "https://pandafix.hu/tool/xbox-classic/bios/evox-m8plus-v16.bin"),
        (tr['back'], None)
    ]
    print(tr['bios_download'])
    for idx, (name, _) in enumerate(bios_list):
        print(f"{idx+1}. {name}")
    while True:
        choice = input(tr['select_bin'] + " ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(bios_list):
            idx = int(choice)-1
            if bios_list[idx][1] is None:
                return
            name, url = bios_list[idx]
            folder = tr['bios_folder2']
            os.makedirs(folder, exist_ok=True)
            fname = os.path.join(folder, os.path.basename(url))
            if download_file(url, fname):
                print(tr['download_success'].format(os.path.basename(fname)))
                log(tr, "Download", tr['download_success'].format(os.path.basename(fname)))
            else:
                print(tr['download_fail'])
                log(tr, "Download", tr['download_fail'])
            input(tr['press_enter'])
            return
        else:
            print(tr['invalid_option'])

def support_menu(tr):
    support_links = [
        (tr['support1'], "https://www.paypal.com/donate/?hosted_button_id=7BRDHVYY98WK4"),
        (tr['support2'], "https://buymeacoffee.com/pandafix"),
        (tr['support3'], "https://www.patreon.com/pandafix"),
        (tr['support4'], "https://github.com/KonzolozZ"),
        (tr['support5'], None)
    ]
    while True:
        print()
        print(tr['support_menu'])
        for name, _ in support_links:
            print(name)
        choice = input(tr['select_option'] + " ").strip()
        if choice in [str(i+1) for i in range(len(support_links))]:
            idx = int(choice) - 1
            if support_links[idx][1] is None:
                return
            print(tr['support_opening'])
            webbrowser.open(support_links[idx][1])
            print()
        else:
            print(tr['invalid_option'])

def main():
    lang = select_language()
    tr = translations[lang]
    port = auto_select_port(tr)
    while True:
        print_header(tr)
        print(tr['menu'])
        print(tr['menu1'])
        print(tr['menu2'])
        print(tr['menu3'])
        print(tr['menu4'])
        print(tr['menu5'])
        print_log(tr)
        choice = input(tr['select_option'] + " ").strip()
        if choice == "1":
            xyclops_dump(tr, port)
        elif choice == "2":
            xyclops_write(tr, port)
        elif choice == "3":
            bios_download(tr)
        elif choice == "4":
            support_menu(tr)
        elif choice == "5":
            print(tr['exit'])
            time.sleep(1)
            break
        else:
            print(tr['invalid_option'])
            time.sleep(1)

if __name__ == "__main__":
    main()
