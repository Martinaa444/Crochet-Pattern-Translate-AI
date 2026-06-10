import streamlit as st
from google import genai
from google.genai import types

# 1. Ustawienia wyglądu strony
st.set_page_config(page_title="Crochet Pattern Translate_AI", page_icon="🧶", layout="wide")

# --- DODAWANIE TŁA STRONY ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://plus.unsplash.com/premium_photo-1675799559532-b51954034628?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* Wymuszenie, żeby główne tytuły były ciemne i bardzo czytelne na wybranym tle */
    h1, h2, h3, h4, .stSubheader, span[data-testid="stHeaderMarkdown"] {
        color: #3d2a1c !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }
    
    /* Ten kawałek sprawia, że białe boksy z tekstem są lekko przezroczyste, żeby tło nie utrudniało czytania */
    .stTextArea textarea, .stMarkdown, div[data-testid="stColumn"] {
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("🧶 Crochet Pattern Translate_AI")
st.subheader("System kontekstowego tłumaczenia wzorów rękodzielniczych")
st.write("---")

# 2. Definicja promptu systemowego (Mózg AI z obsługą ES, EN, DE)
SYSTEM_PROMPT = """
Jesteś ekspertem w dziedzinie międzynarodowego rękodzieła i amigurumi. Działasz jako kompilator semantyczny wzorów szydełkowych. 
Twoim zadaniem jest przetłumaczenie podanego tekstu wzoru na język polski, zachowując jego strukturę logiczną.

SŁOWNIK NADRZĘDNY DO MAPOWANIA POJĘĆ BRANŻOWYCH:

--- JĘZYK HISZPAŃSKI ---
- am / anillo mágico -> MR / magiczne kółko
- pb / punto bajo -> ps / półsłupek
- aum / aumento -> dod / dodać oczko (zwiększenie)
- dis / dism / dec -> red / redukcja oczka (zmniejszenie)
- pa / punto alto -> s / słupek
- mpa / medio punto alto -> psn / półsłupek nawijany
- cad / cadeneta -> op / oczko łańcuszka

--- JĘZYK ANGIELSKI (US/UK) ---
- mr / magic ring -> MR / magiczne kółko
- sc / single crochet -> ps / półsłupek
- inc / increase -> dod / dodać oczko
- dec / decrease -> red / redukcja oczka
- dc / double crochet -> s / słupek
- hdc / half double crochet -> psn / półsłupek nawijany
- ch / chain -> op / oczko łańcuszka

--- JĘZYK NIEMIECKI ---
- MR / Magischer Ring -> MR / magiczne kółko
- fM / feste Masche -> ps / półsłupek
- zun / Zunahme / verdoppeln -> dod / dodać oczko (zwiększenie)
- abn / Abnahme / zusammenhäkeln -> red / redukcja oczka (zmniejszenie)
- Lm / Luftmasche -> op / oczko łańcuszka
- hStb / halbes Stäbchen -> psn / półsłupek nawijany
- Stb / Stäbchen -> s / słupek
- km / Kettmasche -> oz / oczko łańcuszka

FORMAT WYJŚCIOWY (Zwróć wynik w czystym Markdown):
### 📋 Informacje o wzorze
* **Wykryty język źródłowy:** [Wpisz język]
* **Wymagane materiały:** [Wypisz włóczki/szydełka, jeśli są w tekście]

### 🔤 Użyte skróty (Legenda)
- *skrót oryginalny* -> **polskie znaczenie (skrót polski)**

### 🧶 Tłumaczenie wzoru krok po kroku
Każdy rząd MUSI zaczynać się od nowej linii i być bezwzględnie odseparowany od poprzedniego. 
Używaj zapisu z nawiasami okrągłymi dla rund/rzędów. Po każdym rzędzie wstaw podwójny enter (nową linię).

Formatuj dokładnie tak (przykład):
(Runda 1) **6 ps** w magiczne kółko [6]

(Runda 2) **6 dod** [12]

(Runda 3) (**1 ps, 1 dod**) x 6 [18]

NIGDY nie łącz rzędów w jeden blok tekstu. Jeśli wzór zawiera zakres rzędów, np. 6-10, napisz:
(Runda 6 - 10) **30 ps** [30]
"""

# 3. Inicjalizacja klienta Gemini API
GEMINI_KEY = "tu_wklej_swój_klucz"
client = genai.Client(api_key=GEMINI_KEY)

# 4. Tworzenie interfejsu użytkownika (2 kolumny)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Wklej oryginalny wzór")
    user_input = st.text_area(
        "Wklej tekst wzoru (obsługiwane języki: hiszpański, angielski, niemiecki):", 
        height=400,
        placeholder="Przykłady wejściowe:\n- ES: Vta 1: am de 6 pb (6)\n- EN: Rnd 1: 6 sc in MR (6)\n- DE: Rd 1: 6 fM in MR (6)"
    )
    
    run_button = st.button("🚀 Przetłumacz wzór przez Gemini AI", use_container_width=True)

with col2:
    st.markdown("### 📤 Przetłumaczony wzór")
    
    if run_button:
        if not user_input.strip():
            st.error("Błąd: Najpierw wklej jakiś wzór do okienka po lewej stronie!")
        else:
            with st.spinner("Gemini analizuje strukturę wzoru..."):
                import time
                
                max_retries = 3
                response = None
                
                # Próba wysłania zapytania (max 3 podejścia)
                for attempt in range(max_retries):
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=user_input,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                temperature=0.2
                            )
                        )
                        break  # Sukces! Przerwanie pętli
                    except Exception as e:
                        if "503" in str(e) and attempt < max_retries - 1:
                            time.sleep(1.5)  # Serwer zajęty, czekamy i próbujemy znowu
                            continue
                        else:
                            break
                
                # Renderowanie wyniku w zależności od odpowiedzi serwera
                if response:
                    st.success("Gotowe!")
                    formatted_text = response.text.replace("\n", "\n\n")
                    st.markdown(formatted_text)
                else:
                    st.warning("⚠️ Usługa tłumaczenia jest w tej chwili przeciążona (Błąd sieciowy 503). Serwery Google nie odpowiadają. Spróbuj kliknąć przycisk ponownie za moment.")
