# flake8: noqa
import streamlit as st


def faq():
    st.markdown(
        """
# Thanks to
This tool is a customized fork from a [GitHub repository](https://github.com/mmz-001/knowledge_gpt) of [mmz_001](https://twitter.com/mm_sasmitha)"  noqa: E501

## How does Vink-GPT work?
The Vink article as been stored as a .txt Vink article. This is then divided into smaller chunks 
and stored in a special type of database called a vector index 
that allows for semantic search and retrieval.

When you ask a question, Vink GPT, it will search through the
article chunks and find the most relevant ones using the vector index.
Then, it will use GPT3 to generate a final answer.


## What do the numbers mean under each source?
For a PDF Vink article, you will see a citation number like this: 3-12. 
The first number is the page number and the second number is 
the chunk number on that page. For DOCS and TXT Vink articles, 
the first number is set to 1 and the second number is the chunk number.

## Are the answers 100% accurate?
No, the answers are not 100% accurate. Vink GPT uses GPT-3 to generate
answers. GPT-3 is a powerful language model, but it sometimes makes mistakes 
and is prone to hallucinations. Also, Vink GPT uses semantic search
to find the most relevant chunks and does not see the entire Vink article,
which means that it may not be able to find all the relevant information and
may not be able to answer all questions (especially summary-type questions
or questions that require a lot of context from the Vink article).

But for most use cases, Vink GPT is very accurate and can answer
most questions. Always check with the sources to make sure that the answers
are correct.
"""
    )
