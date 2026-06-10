# Crochet-Pattern-Translate-AI
System kontekstowego tłumaczenia wzorów szydełkowych przy użyciu Gemini API
## 🚀 Jak uruchomić projekt lokalnie
1. Zainstaluj wymagane biblioteki:
pip install streamlit google-genai
   
   Umieść swój klucz API w pliku app.py w zmiennej GEMINI_KEY.

Uruchom aplikację komendą:
python -m streamlit run app.py

W repozytorium znajdują się gotowe pliki tekstowe z surowymi wzorami w trzech językach, przygotowane do przetestowania aplikacji:

Wzór_1_hiszpański.txt – zawiera terminologię taką jak anillo mágico (am) oraz punto bajo (pb).
Wzór_2_angielski.txt – zawiera standardowe oznaczenia US, m.in. single crochet (sc) i increase (inc).
Wzór_3_niemiecki.txt – zawiera skróty niemieckie, np. feste Masche (fM) oraz Luftmasche (Lm).

Możesz otworzyć te pliki, skopiować ich zawartość i wkleić bezpośrednio do lewego okna aplikacji, aby zweryfikować poprawność działania kompilatora semantycznego AI.
