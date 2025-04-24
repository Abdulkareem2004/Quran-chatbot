from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set paths
ARABIC_CSV_PATH = r"Arabic-Original.csv"  # Update with actual path
TAMIL_QURAN_FOLDER = r"quran"  # Update with actual path

# Load Arabic Quran data
df = pd.read_csv(ARABIC_CSV_PATH, encoding="utf-8", sep="|", header=None,
                 names=["SurahNumber", "AyahNumber", "AyahText"])

# Surah name mapping
surah_names = {
    1: ["Al-Fatiha", "அல்-பாத்திஹா"],
    2: ["Al-Baqarah", "அல்-பகரா"],
    3: ["Al-Imran", "ஆல்-இம்ரான்"],
    4: ["An-Nisa", "அன்-நிசா"],
    5: ["Al-Ma'idah", "அல்-மாயிதா"],
    6: ["Al-An'am", "அல்-அன்ஆம்"],
    7: ["Al-A'raf", "அல்-அராஃப்"],
    8: ["Al-Anfal", "அல்-அன்ஃபால்"],
    9: ["At-Tawbah", "அத்-தவ்பா"],
    10: ["Yunus", "யூனுஸ்"],
    11: ["Hud", "ஹூத்"],
    12: ["Yusuf", "யூசுப்"],
    13: ["Ar-Ra'd", "அர்ரஅத்"],
    14: ["Ibrahim", "இப்ராஹீம்"],
    15: ["Al-Hijr", "அல்-ஹிஜ்ர்"],
    16: ["An-Nahl", "அன்-நஹ்ல்"],
    17: ["Al-Isra", "அல்-இஸ்ரா"],
    18: ["Al-Kahf", "அல்-கஹ்ப்"],
    19: ["Maryam", "மர்யம்"],
    20: ["Taha", "தாஹா"],
    21: ["Al-Anbiya", "அல்-அன்பியா"],
    22: ["Al-Hajj", "அல்-ஹஜ்ஜ்"],
    23: ["Al-Mu’minun", "அல்-முமினூன்"],
    24: ["An-Nur", "அன்-நூர்"],
    25: ["Al-Furqan", "அல்-புர்கான்"],
    26: ["Ash-Shu’ara", "அஷ்-ஷுஅரா"],
    27: ["An-Naml", "அன்-நம்ல்"],
    28: ["Al-Qasas", "அல்-கசஸ்"],
    29: ["Al-Ankabut", "அல்-அங்கபூத்"],
    30: ["Ar-Rum", "அல்-ரூம்"],
    31: ["Luqman", "லுக்மான்"],
    32: ["As-Sajdah", "அல்-ஸஜ்தா"],
    33: ["Al-Ahzab", "அல்-அஹ்ழாப்"],
    34: ["Saba", "சபா"],
    35: ["Fatir", "ஃபாத்திர்"],
    36: ["Ya-Sin", "யாஸீன்"],
    37: ["As-Saffat", "அல்-ஸாஃப்ஃபாத்"],
    38: ["Sad", "ஸாத்"],
    39: ["Az-Zumar", "அல்-சுமர்"],
    40: ["Ghafir", "ஃகாஃபிர்"],
    41: ["Fussilat", "ஃபுஸ்ஸிலாத்"],
    42: ["Ash-Shura", "அஷ்-ஷூரா"],
    43: ["Az-Zukhruf", "அல்-சுக்ருஃப்"],
    44: ["Ad-Dukhan", "அத்-துகான்"],
    45: ["Al-Jathiyah", "அல்-ஜாதியா"],
    46: ["Al-Ahqaf", "அல்-அஹ்காஃப்"],
    47: ["Muhammad", "முஹம்மத்"],
    48: ["Al-Fath", "அல்-பத்"],
    49: ["Al-Hujurat", "அல்-ஹுஜுராத்"],
    50: ["Qaf", "காஃப்"],
    51: ["Adh-Dhariyat", "அத்-தாரியாத்"],
    52: ["At-Tur", "அத்-தூர்"],
    53: ["An-Najm", "அல்-நஜ்ம்"],
    54: ["Al-Qamar", "அல்-கமர்"],
    55: ["Ar-Rahman", "அர்-ரஹ்மான்"],
    56: ["Al-Waqi’a", "அல்-வாக்கியா"],
    57: ["Al-Hadid", "அல்-ஹதீத்"],
    58: ["Al-Mujadila", "அல்-முஜாதிலா"],
    59: ["Al-Hashr", "அல்-ஹஷ்ர்"],
    60: ["Al-Mumtahanah", "அல்-மும்தஹினா"],
    61: ["As-Saff", "அஸ்-ஸஃப்"],
    62: ["Al-Jumu’a", "அல்-ஜுமுஆ"],
    63: ["Al-Munafiqun", "அல்-முனாஃபிகூன்"],
    64: ["At-Taghabun", "அத்-தஃகாபுன்"],
    65: ["At-Talaq", "அத்-தலாக்"],
    66: ["At-Tahrim", "அத்-தஹ்ரீம்"],
    67: ["Al-Mulk", "அல்-முல்க்"],
    68: ["Al-Qalam", "அல்-கலாம்"],
    69: ["Al-Haqqah", "அல்-ஹாக்கா"],
    70: ["Al-Ma’arij", "அல்-மஅரிஜ்"],
    71: ["Nuh", "நூஹ்"],
    72: ["Al-Jinn", "அல்-ஜின்ன்"],
    73: ["Al-Muzzammil", "அல்-முஸம்மில்"],
    74: ["Al-Muddaththir", "அல்-முத்தஸ்ஸிர்"],
    75: ["Al-Qiyamah", "அல்-கியாமா"],
    76: ["Al-Insan", "அல்-இன்ஸான்"],
    77: ["Al-Mursalat", "அல்-முர்சலாத்"],
    78: ["An-Naba", "அன்-நபா"],
    79: ["An-Nazi’at", "அன்-நாஸிஅாத்"],
    80: ["Abasa", "அபசா"],
    81: ["At-Takwir", "அத்-தக்குவீர்"],
    82: ["Al-Infitar", "அல்-இன்பிதார்"],
    83: ["Al-Mutaffifin", "அல்-முதஃபிஃபீன்"],
    84: ["Al-Inshiqaq", "அல்-இன்ஷிக்காக்"],
    85: ["Al-Buruj", "அல்-புரூஜ்"],
    86: ["At-Tariq", "அத்-தாரிக்"],
    87: ["Al-Ala", "அல்-அஅ்லா"],
    88: ["Al-Ghashiyah", "அல்-காஷியா"],
    89: ["Al-Fajr", "அல்-ஃபஜ்ர்"],
    90: ["Al-Balad", "அல்-பலத்"],
    91: ["Ash-Shams", "அஷ்-ஷம்ஸ்"],
    92: ["Al-Layl", "அல்-லயில்"],
    93: ["Ad-Duhaa", "அத்-துஹா"],
    94: ["Ash-Sharh", "அஷ்-ஷர்ஹ்"],
    95: ["At-Tin", "அத்-தீன்"],
    96: ["Al-Alaq", "அல்-அலக்"],
    97: ["Al-Qadr", "அல்-கத்ர்"],
    98: ["Al-Bayyinah", "அல்-பய்யினா"],
    99: ["Az-Zalzalah", "அஸ்-ஸல்சலா"],
    100: ["Al-Adiyat", "அல்-அதியாத்"],
    101: ["Al-Qari’ah", "அல்-காரிஅ"],
    102: ["At-Takathur", "அத்-தகாஸுர்"],
    103: ["Al-Asr", "அல்-அஸ்ர்"],
    104: ["Al-Humazah", "அல்-ஹுமஸா"],
    105: ["Al-Fil", "அல்-ஃபீல்"],
    106: ["Quraish", "குரைஷ்"],
    107: ["Al-Ma’un", "அல்-மா’உன்"],
    108: ["Al-Kawthar", "அல்-கௌசர்"],
    109: ["Al-Kafirun", "அல்-காஃபிரூன்"],
    110: ["An-Nasr", "அல்-நஸ்ர்"],
    111: ["Al-Masad", "அல்-மசத்"],
    112: ["Al-Ikhlas", "அல்-இக்லாஸ்"],
    113: ["Al-Falaq", "அல்-பலக்"],
    114: ["An-Nas", "அல்-நாஸ்"]
}

# Reverse lookup for surah names
name_to_number = {v[0].lower(): k for k, v in surah_names.items()}
name_to_number.update({v[1].lower(): k for k, v in surah_names.items()})

def get_arabic_ayahs(surah_name, start_ayah, end_ayah):
    """Fetch multiple Arabic Ayahs."""
    surah_number = name_to_number.get(surah_name.lower())
    if surah_number is None:
        return None  # Surah not found

    verses = df[(df["SurahNumber"] == surah_number) & (df["AyahNumber"].between(start_ayah, end_ayah))]
    return verses["AyahText"].tolist() if not verses.empty else None


def get_tamil_ayahs(surah_name, start_ayah, end_ayah):
    """Fetch multiple Tamil Ayahs from a text file."""
    surah_file = os.path.join(TAMIL_QURAN_FOLDER, f"{surah_name}.txt")

    if not os.path.exists(surah_file):
        return None  # Surah not found

    try:
        with open(surah_file, "r", encoding="utf-8") as file:
            ayahs = file.readlines()  # Read all lines

        if start_ayah < 1 or end_ayah > len(ayahs):
            return None  # Ayah range out of bounds

        return ayahs[start_ayah - 1: end_ayah]  # Extract requested Ayahs

    except Exception as e:
        return None  # Error reading file


@app.route("/api/quran", methods=["GET"])
def get_quran_verses():
    surah_name = request.args.get("surah")
    start_ayah = int(request.args.get("startAyah"))
    end_ayah = int(request.args.get("endAyah"))

    arabic_ayahs = get_arabic_ayahs(surah_name, start_ayah, end_ayah)
    tamil_ayahs = get_tamil_ayahs(surah_name, start_ayah, end_ayah)

    if arabic_ayahs is None or tamil_ayahs is None:
        return jsonify({"error": "Surah or Ayah range not found."}), 404

    verses = [
        {"arabic": arabic_ayahs[i].strip(), "tamil": tamil_ayahs[i].strip()}
        for i in range(len(arabic_ayahs))
    ]

    return jsonify({"verses": verses})


if __name__ == "__main__":
    app.run(debug=True)
