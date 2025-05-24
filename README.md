# 🐼 Xyclops Flasher Tool v1.1 (250523)

**Pandafix** ([pandafix.hu](https://pandafix.hu))

---

> **A Xyclops Flasher Tool egy többnyelvű, platformfüggetlen Python konzolos alkalmazás, amellyel egyszerűen kiolvashatod, írhatod és ellenőrizheted az Xbox 1.6 alaplapokon található Xyclops IC BIOS-t.**  
> A program támogatja az automatikus COM port kiválasztást, a BIOS dump mágikus fejlécének ellenőrzését, animált visszajelzést ad a folyamatok során, naplózza a műveleteket, lehetővé teszi BIOS-ok letöltését, és **beépített támogatási menüpontot** is kínál.

---

## ✨ Főbb funkciók

- 🌍 **Többnyelvű menü**: magyar, angol, német, francia, spanyol
- 🎨 **Grafikus fejléc**: Pandafix ASCII logó, [pandafix.hu](https://pandafix.hu) felirattal
- 🔌 **Automatikus COM port kiválasztás**
- 📥 **Xyclops Dump**: BIOS kiolvasás, fájlmentés, mágikus fejléc ellenőrzés (0x100 offseten)
- 📝 **Xyclops Write**: BIOS írás, törlés, ellenőrzés, csak 256KiB-nál nem nagyobb .bin fájlokkal
- 🌐 **BIOS letöltés**: BIOS-ok letöltése (User-Agent fejléccel)
- 🕹️ **Animáció minden folyamatnál** (|*|, |o| stb.) és részletes visszajelzés
- 🕒 **Műveleti naplózás**: főmenüben látható, időbélyeggel
- 💖 **Támogatás menüpont**: PayPal, BuyMeaCoffee, Patreon, GitHub támogatási lehetőségek közvetlenül a programból

---

## 🚀 Használat
### Telepítés
pip install pyserial requests
### Futtatás
python Xyclops-Flasher-Tool.py


### Nyelv kiválasztása

A program indításakor válaszd ki a kívánt nyelvet.

### Főmenü

1. **Xyclops Dump** (kiolvasás)
2. **Xyclops Write** (írás)
3. **BIOS letöltés**
4. **Támogatás**
5. **Kilépés**

---

## 🛠️ Funkciók részletesen

### 📥 Dump

- Kiolvassa a BIOS-t a Xyclops IC-ből, ellenőrzi a mágikus fejlécet (0x100 offseten).
- Ha már van `dump.bin`, felülírja vagy új néven menti (`dump2.bin`, `dump3.bin`...).
- A fájlokat a `Bios/Original dump` mappába menti.

### 📝 Write

- Csak a `Bios` mappában található, max. 256KiB méretű `.bin` fájlokkal működik.
- Ha nincs BIOS fájl, letölthető a menüből.
- Írás előtt ellenőrzi, van-e `dump.bin`, szükség esetén mentést ajánl.
- Törlés, írás, ellenőrzés animációval, minden lépés naplózva.

### 🌐 BIOS letöltés

- Eredeti BIOS-ok (Cerbios Hybrid, Evox M8 stb.) letöltése a programból.

### 💖 Támogatás menüpont

A főmenü **Támogatás** pontjában az alábbi lehetőségek közül választhatsz, melyek kiválasztásakor automatikusan megnyílik a böngésződ:

- [PayPal](https://www.paypal.com/donate/?hosted_button_id=7BRDHVYY98WK4)
- [BuyMeaCoffee](https://buymeacoffee.com/pandafix)
- [Patreon](https://www.patreon.com/pandafix)
- [GitHub](https://github.com/KonzolozZ)
- Visszalépés: **éhezni hagylak** (vicces visszalépés a főmenübe)

### 🕒 Naplózás

- Minden sikeres/sikertelen művelet időponttal, a főmenüben visszanézhető.

---

## ⚡ Követelmények

- **Python 3.8+**
- `pyserial`, `requests`

---

## ⚠️ Fontos információk

- **Csak Xbox 1.6 alaplaphoz használható!**
- Az Xyclops A-B01 IC-t nem támogatja!
- Az AV csatlakozó közelében az R5M3, R4M10 0Ohm ellenállásokat el kell távolítani.
- A Xyclops IC 29-es lábát 3.3V-ra, a 64-es lábat az adapter RX, a 63-ast az adapter TX pontjára, a GND-t az alaplap GND-jára kell kötni.

---

## 🙏 Köszönet

Külön köszönet [Prehistoricman](https://github.com/Prehistoricman/Xbox_SMC) reverse engineering munkájáért!

---

## 💡 Teljes mértékben AI felhasználásával készült 😅

---

# 🇬🇧 English version

> **Xyclops Flasher Tool is a multilingual, cross-platform Python console app for reading, writing, and verifying the Xyclops IC BIOS on Xbox 1.6 motherboards.**  
> It features automatic COM port selection, magic header verification (at 0x100 offset), animated feedback, operation logging, BIOS download support, and a built-in support menu.

### ✨ Main Features

- 🌍 **Multilingual menu**: Hungarian, English, German, French, Spanish
- 🔌 **Automatic COM port selection**
- 📥 **Xyclops Dump**: BIOS read, file save, magic header check (at 0x100 offset)
- 📝 **Xyclops Write**: BIOS write, erase, verify, only for .bin files up to 256KiB
- 🌐 **BIOS Download**: Download BIOS files (with User-Agent header)
- 🕹️ **Animated feedback** for all processes (|*|, |o| etc.)
- 🕒 **Operation log**: visible in the main menu with timestamps
- 💖 **Support menu**: PayPal, BuyMeaCoffee, Patreon, GitHub links directly from the program

### 🚀 Usage
### Install
pip install pyserial requests
### Run
python Xyclops-Flasher-Tool.py


#### Main menu

1. **Xyclops Dump** (read)
2. **Xyclops Write** (write)
3. **BIOS download**
4. **Support**
5. **Exit**

#### Details

- **Dump**: Reads BIOS, checks magic header at 0x100, saves to `Bios/Original dump`.
- **Write**: Works with `.bin` files in `Bios` folder (max 256KiB), offers backup, shows all steps with animation.
- **BIOS download**: Download original BIOS files from menu.
- **Support**: Choose from PayPal, BuyMeaCoffee, Patreon, GitHub (opens browser).
- **Logging**: All operations logged with timestamp in the main menu.

### ⚠️ Important

- **Only for Xbox 1.6 motherboards!**
- Xyclops A-B01 IC is NOT supported!
- Remove R5M3, R4M10 0 Ohm resistors near the AV connector.
- Pin 29 to 3.3V, pin 64 to adapter RX, pin 63 to adapter TX, GND to motherboard GND.

---

**Special thanks to [Prehistoricman](https://github.com/Prehistoricman/Xbox_SMC) for his Xyclops research!**

---

*Made possible with AI assistance 😅*
