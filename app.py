import streamlit as st

# --- Konfiguration der Seite ---
st.set_page_config(page_title="Härtefall-Rechner 2026", page_icon="🦷")

st.title("🦷 Härtefall-Rechner Zahnersatz (2026)")
st.write("Ermitteln Sie Ihren Anspruch auf den doppelten Festzuschuss oder den gleitenden Härtefall.")

# --- Seitenleiste für Eingaben ---
st.sidebar.header("Ihre Daten")

brutto_einkommen = st.sidebar.number_input(
    "Monatliches Brutto-Einkommen (aller Personen)", 
    min_value=0.0, 
    value=1650.00, 
    step=10.00,
    format="%.2f"
)

personen = st.sidebar.number_input(
    "Anzahl Personen im Haushalt", 
    min_value=1, 
    value=1, 
    step=1
)

normaler_festzuschuss = st.sidebar.number_input(
    "Regulärer Festzuschuss laut Heil- und Kostenplan (ohne Bonus)", 
    min_value=0.0, 
    value=400.00, 
    step=10.00,
    format="%.2f",
    help="Dies ist der Betrag, den die Kasse normalerweise zahlt (meist 60%)."
)

# --- Logik (Werte für 2026) ---
GRENZE_ALLEINSTEHEND = 1582.00
GRENZE_MIT_1_ANGEHOERIGEN = 2175.25
ZUSCHLAG_WEITERE_PERSON = 395.50

# 1. Individuelle Grenze berechnen
individuelle_grenze = GRENZE_ALLEINSTEHEND
if personen == 2:
    individuelle_grenze = GRENZE_MIT_1_ANGEHOERIGEN
elif personen > 2:
    individuelle_grenze = GRENZE_MIT_1_ANGEHOERIGEN + ((personen - 2) * ZUSCHLAG_WEITERE_PERSON)

# --- Berechnung und Ausgabe ---

st.divider() # Trennlinie

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Ihre Einkommensgrenze (2026)", value=f"{individuelle_grenze:,.2f} €")
with col2:
    diff = brutto_einkommen - individuelle_grenze
    color = "inverse"
    if diff <= 0:
        delta_msg = "Unter der Grenze (Voller Härtefall)"
        delta_color = "normal" # Grün in Streamlit Standard
    else:
        delta_msg = f"{diff:,.2f} € über der Grenze"
        delta_color = "off" 
    st.metric(label="Ihr Einkommen", value=f"{brutto_einkommen:,.2f} €", delta=delta_msg, delta_color=delta_color)

st.subheader("Ergebnis der Berechnung")

# Fall A: Voller Härtefall
if brutto_einkommen <= individuelle_grenze:
    st.success("✅ **Voller Härtefall!** Sie müssen keine Eigenanteile für die Regelversorgung zahlen.")
    st.write(f"Die Kasse zahlt den doppelten Festzuschuss: **{normaler_festzuschuss * 2:,.2f} €**")

# Fall B: Gleitender Härtefall
else:
    ueberschuss = brutto_einkommen - individuelle_grenze
    zumutbare_belastung = ueberschuss * 3
    doppelter_festzuschuss = normaler_festzuschuss * 2
    
    # Härtefall-Zuschuss berechnen
    haertefall_zuschuss = doppelter_festzuschuss - zumutbare_belastung
    
    # Prüfen, ob der Härtefall höher ist als der normale Zuschuss
    if haertefall_zuschuss > normaler_festzuschuss:
        st.info("⚠️ **Gleitender Härtefall greift!**")
        
        st.write("So setzt sich Ihr Zuschuss zusammen:")
        
        rechnung = {
            "Doppelter Festzuschuss (Maximal)": doppelter_festzuschuss,
            "Abzug Zumutbare Belastung (3x Überschuss)": -zumutbare_belastung,
            "---------------------------------": 0,
            "Ihr neuer Zuschuss": haertefall_zuschuss
        }
        
        # Schöne Tabelle ausgeben
        for k, v in rechnung.items():
            if k.startswith("-"):
                st.text(f"{k}")
            else:
                st.text(f"{k:<45} {v:>10.2f} €")
        
        ersparnis = haertefall_zuschuss - normaler_festzuschuss
        st.markdown(f"### Sie erhalten: **{haertefall_zuschuss:,.2f} €**")
        st.write(f"(Das sind **{ersparnis:,.2f} € mehr** als ohne Härtefallantrag)")
        
    else:
        st.error("❌ Härtefall lohnt sich rechnerisch nicht.")
        st.write(f"Ihr Einkommen ist zu hoch bzw. der Festzuschuss zu niedrig. Der errechnete Härtefall-Zuschuss ({haertefall_zuschuss:.2f} €) wäre niedriger als Ihr normaler Zuschuss ({normaler_festzuschuss:.2f} €).")
        st.write("Sie erhalten den **regulären Festzuschuss + Bonus**.")

# Disclaimer
st.caption("---")
st.caption("Hinweis: Alle Angaben ohne Gewähr. Maßgeblich ist immer die Berechnung Ihrer Krankenkasse. Stand der Werte: 2026.")