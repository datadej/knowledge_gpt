import streamlit as st

from knowledge_gpt.components.faq import faq
from dotenv import load_dotenv
import os

load_dotenv()


def sidebar():
    with st.sidebar:
        st.markdown(
            "# Guide 🗺️"
        )
        st.markdown(
            "# Step 1\n"
            "Enter the provided [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        st.markdown("# Step 2")
        st.markdown(
            "\nBefore trying out the Vink GPT, I recommend reading the [article](https://vink.aftenposten.no/artikkel/onOkVa/her-er-oslos-hotteste-restauranter-akkurat-na) to familiarize yourself with the knowledge base of this tool. Once ready, simply select the model (GPT-4 is recommended for optimal results), and start exploring."
)
        st.markdown("# Hints 🤔💭")
        st.markdown(


            "\nFeel free to ask anything related to the article **in English**. Here are some example queries:"
            "\n- What is the main focus of the article?"
            "\n- Which Oslo restaurant is redefining traditional cuisine?"
            "\n- What are the top vegetarian dining spots in Oslo for Autumn 2023?"
            "\n- Can you name an Oslo eatery that offers an exciting fusion of global flavors?"
            )
       # st.markdown(
       #     "🍕Vink GPT allows you to ask questions about this [Vink article](https://vink.aftenposten.no/artikkel/onOkVa/her-er-oslos-hotteste-restauranter-akkurat-na) on the hottest restaurants in Oslo right now."
       #     "The article has been last updated on 2023-10-28, and is written in Norwegian but for the purpose of this Proof of Concept it has been translated in English and questions to Vink GPT should be made in English."
       # )
       # st.markdown("---")

        faq()
