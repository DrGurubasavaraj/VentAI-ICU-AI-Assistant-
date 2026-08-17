from pathlib import Path

path = Path("ui/dashboard.py")

if not path.exists():
    raise SystemExit(
        "Could not find ui/dashboard.py. Run this script from the VentAI project root."
    )

text = path.read_text(encoding="utf-8")

text = text.replace(
    "ABG / oxygenation risk",
    "ABG risk index"
)

text = text.replace(
    "Excludes HR, MAP, temperature and SpO2.",
    "Derived from pH, PaCO2 and PaO2; excludes FiO2/PF and context vitals."
)

path.write_text(text, encoding="utf-8")

print("Updated ui/dashboard.py terminology:")
print("  ABG / oxygenation risk -> ABG risk index")
print("  helper text now states what the index does and does not include")
