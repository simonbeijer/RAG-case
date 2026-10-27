# RAG-chatt för compileit.com

En chatt som svarar på svenska på frågor om compileit.com. Svaret strömmas, källorna visas och följdfrågor fungerar inom samma session.

Python, LangChain, LangGraph, FastAPI och Next.js. Agentens graf: [`docs/agent-graph.md`](docs/agent-graph.md).

## Kom igång
Kräver [uv](https://docs.astral.sh/uv/), Node.js och en API-nyckel från [OpenRouter](https://openrouter.ai) eller OpenAI.

```
make setup
cp backend/.env.example backend/.env   # lägg in LLM_API_KEY
make ingest                            # hämtar sajten och bygger index
make api
```

Kör i en annan terminal:

```
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm install
npm run dev
```

Öppna http://localhost:3000. Terminalchatt med loggar: `make chat`. Tester: `make test`.

### OpenAI i stället för OpenRouter
Ändra tre rader i `backend/config.yaml`:

```
base_url: https://api.openai.com/v1
chat_model: gpt-4.1-mini
embedding_model: text-embedding-3-small
```

## Why this design
- **Litet.** Ca 350 chunks ryms i en matris i minnet. Därför finns ingen vektordatabas.
- **Testbart.** Terminalchatten loggar sökfråga, träffar, tokens, kostnad och tid för varje svar.
- **Styrbart.** Allt som påverkar svaret ligger i `backend/config.yaml` och `backend/prompts/`.
- **Billig modell.** Hämtningen och prompten ska göra svaren bra, inte en dyr modell.
- **Agent med verktyg.** En LangGraph-graf med verktyget `search_knowledge_base`. Sökningen är tvingad (`tool_choice="required"`), så modellen söker alltid innan den svarar.

## Testfrågor
- Vad erbjuder ni för typer av AI-tjänster?
- Vilka branscher jobbar ni med?
- Hur kontaktar man er, och var sitter ni?
- Har ni beskrivit hur ni jobbar med säkerhet/sekretess?
- Sammanfatta sidan "Om oss" i tre punkter och länka källan.

## Antaganden
- Körs lokalt.
- Minnet försvinner vid omstart.

## Känt fel
Frågor om enskilda medarbetare kan ge fel stad. På medarbetarsidorna ligger kollegornas kort i samma chunk som personens egna uppgifter, och modellen kopplar fel stad till personen. Lösning: ta bort kollegornas kort i rensningen (`backend/app/scrape.py`), så att varje chunk bara innehåller personens egen text.

## Säkerhet i en riktig produkt
Chatten körs lokalt, så de här hålen är inte fyllda:
- `thread_id` kontrolleras inte. Den som gissar ett id kan läsa någon annans samtal. Kräv ett UUID eller koppla tråden till en inloggning.
- Ingen gräns för antal frågor per IP. CORS stoppar bara webbläsare, så ett skript kan bränna API-krediterna.
- Samtalet växer utan gräns. Begränsa antal frågor eller hur mycket historik som skickas med.
- Länkar i svaret som inte finns bland källorna kontrolleras inte. En påhittad eller injicerad länk blir klickbar.
- Minnet ligger i RAM. En riktig produkt behöver en databas för samtalen.

## Förbättringar
- Dyrare modell som berikar chunks vid indexeringen
- Ordsökning (BM25) tillsammans med vektorsökningen
- En modell som kontrollerar svaret innan det skickas
- En klassificeringsmodell som stoppar prompt injection
- LangSmith för att spåra varje steg agenten tar och felsöka dåliga svar
- Tumme upp/ner som sparas, så att dåliga svar blir nya testfrågor
