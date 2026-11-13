import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama(prompt, model="mistral"):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        st.error("❌ Ollama service not running. Start it with: `ollama serve`")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Ollama request timed out")
        return None
    except Exception as e:
        st.error(f"❌ LLM Error: {str(e)}")
        return None