{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
\
# --- Konfiguration der Seite ---\
st.set_page_config(page_title="H\'e4rtefall-Rechner 2026", page_icon="\uc0\u55358 \u56759 ")\
\
st.title("\uc0\u55358 \u56759  H\'e4rtefall-Rechner Zahnersatz (2026)")\
st.write("Ermitteln Sie Ihren Anspruch auf den doppelten Festzuschuss oder den gleitenden H\'e4rtefall.")\
\
# --- Seitenleiste f\'fcr Eingaben ---\
st.sidebar.header("Ihre Daten")\
\
brutto_einkommen = st.sidebar.number_input(\
    "Monatliches Brutto-Einkommen (aller Personen)", \
    min_value=0.0, \
    value=1650.00, \
    step=10.00,\
    format="%.2f"\
)\
\
personen = st.sidebar.number_input(\
    "Anzahl Personen im Haushalt", \
    min_value=1, \
    value=1, \
    step=1\
)\
\
normaler_festzuschuss = st.sidebar.number_input(\
    "Regul\'e4rer Festzuschuss laut Heil- und Kostenplan (ohne Bonus)", \
    min_value=0.0, \
    value=400.00, \
    step=10.00,\
    format="%.2f",\
    help="Dies ist der Betrag, den die Kasse normalerweise zahlt (meist 60%)."\
)\
\
# --- Logik (Werte f\'fcr 2026) ---\
GRENZE_ALLEINSTEHEND = 1582.00\
GRENZE_MIT_1_ANGEHOERIGEN = 2175.25\
ZUSCHLAG_WEITERE_PERSON = 395.50\
\
# 1. Individuelle Grenze berechnen\
individuelle_grenze = GRENZE_ALLEINSTEHEND\
if personen == 2:\
    individuelle_grenze = GRENZE_MIT_1_ANGEHOERIGEN\
elif personen > 2:\
    individuelle_grenze = GRENZE_MIT_1_ANGEHOERIGEN + ((personen - 2) * ZUSCHLAG_WEITERE_PERSON)\
\
# --- Berechnung und Ausgabe ---\
\
st.divider() # Trennlinie\
\
col1, col2 = st.columns(2)\
with col1:\
    st.metric(label="Ihre Einkommensgrenze (2026)", value=f"\{individuelle_grenze:,.2f\} \'80")\
with col2:\
    diff = brutto_einkommen - individuelle_grenze\
    color = "inverse"\
    if diff <= 0:\
        delta_msg = "Unter der Grenze (Voller H\'e4rtefall)"\
        delta_color = "normal" # Gr\'fcn in Streamlit Standard\
    else:\
        delta_msg = f"\{diff:,.2f\} \'80 \'fcber der Grenze"\
        delta_color = "off" \
    st.metric(label="Ihr Einkommen", value=f"\{brutto_einkommen:,.2f\} \'80", delta=delta_msg, delta_color=delta_color)\
\
st.subheader("Ergebnis der Berechnung")\
\
# Fall A: Voller H\'e4rtefall\
if brutto_einkommen <= individuelle_grenze:\
    st.success("\uc0\u9989  **Voller H\'e4rtefall!** Sie m\'fcssen keine Eigenanteile f\'fcr die Regelversorgung zahlen.")\
    st.write(f"Die Kasse zahlt den doppelten Festzuschuss: **\{normaler_festzuschuss * 2:,.2f\} \'80**")\
\
# Fall B: Gleitender H\'e4rtefall\
else:\
    ueberschuss = brutto_einkommen - individuelle_grenze\
    zumutbare_belastung = ueberschuss * 3\
    doppelter_festzuschuss = normaler_festzuschuss * 2\
    \
    # H\'e4rtefall-Zuschuss berechnen\
    haertefall_zuschuss = doppelter_festzuschuss - zumutbare_belastung\
    \
    # Pr\'fcfen, ob der H\'e4rtefall h\'f6her ist als der normale Zuschuss\
    if haertefall_zuschuss > normaler_festzuschuss:\
        st.info("\uc0\u9888 \u65039  **Gleitender H\'e4rtefall greift!**")\
        \
        st.write("So setzt sich Ihr Zuschuss zusammen:")\
        \
        rechnung = \{\
            "Doppelter Festzuschuss (Maximal)": doppelter_festzuschuss,\
            "Abzug Zumutbare Belastung (3x \'dcberschuss)": -zumutbare_belastung,\
            "---------------------------------": 0,\
            "Ihr neuer Zuschuss": haertefall_zuschuss\
        \}\
        \
        # Sch\'f6ne Tabelle ausgeben\
        for k, v in rechnung.items():\
            if k.startswith("-"):\
                st.text(f"\{k\}")\
            else:\
                st.text(f"\{k:<45\} \{v:>10.2f\} \'80")\
        \
        ersparnis = haertefall_zuschuss - normaler_festzuschuss\
        st.markdown(f"### Sie erhalten: **\{haertefall_zuschuss:,.2f\} \'80**")\
        st.write(f"(Das sind **\{ersparnis:,.2f\} \'80 mehr** als ohne H\'e4rtefallantrag)")\
        \
    else:\
        st.error("\uc0\u10060  H\'e4rtefall lohnt sich rechnerisch nicht.")\
        st.write(f"Ihr Einkommen ist zu hoch bzw. der Festzuschuss zu niedrig. Der errechnete H\'e4rtefall-Zuschuss (\{haertefall_zuschuss:.2f\} \'80) w\'e4re niedriger als Ihr normaler Zuschuss (\{normaler_festzuschuss:.2f\} \'80).")\
        st.write("Sie erhalten den **regul\'e4ren Festzuschuss + Bonus**.")\
\
# Disclaimer\
st.caption("---")\
st.caption("Hinweis: Alle Angaben ohne Gew\'e4hr. Ma\'dfgeblich ist immer die Berechnung Ihrer Krankenkasse. Stand der Werte: 2026.")}