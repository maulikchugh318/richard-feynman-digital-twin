import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st

from rag.retriever import Retriever
from services.gemini_service import GeminiService
from memory.memory_manager import MemoryManager
from utils.voice import text_to_speech


st.set_page_config(
    page_title="Feynman Chat Mode",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Feynman Chat Mode")
st.caption("Ask questions and receive answers in Richard Feynman's teaching style.")

if "retriever" not in st.session_state:
    st.session_state.retriever = Retriever()

if "gemini" not in st.session_state:
    st.session_state.gemini = GeminiService()

if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.header("⚙️ Settings")

    answer_mode = st.selectbox(
        "Answer Style",
        ["Short", "Normal", "Detailed"]
    )

    if answer_mode == "Short":
        max_words = 80
    elif answer_mode == "Normal":
        max_words = 150
    else:
        max_words = 300

    voice_enabled = st.checkbox(
        "🔊 Enable Voice Output",
        value=False
    )

    st.divider()

    st.header("🧠 Memory Dashboard")

    try:
        memories = (
            st.session_state.memory
            .long_term
            .get_memories_with_time()
        )

        st.metric(
            "Total Memories",
            len(memories)
        )

        if not memories:
            st.info("No memories stored yet.")

        else:
            st.caption("Recent Memories")

            for memory_id, memory_text, created_at in memories[:5]:

                with st.expander(
                    f"Memory {memory_id}"
                ):
                    st.write(memory_text)
                    st.caption(
                        f"Created at: {created_at}"
                    )

    except Exception:
        memories = []
        st.warning(
            "Memory dashboard will appear after the first saved memory."
        )

    st.divider()

    st.header("⏳ Timeline Awareness")

    if memories:
        latest_memory = memories[0]

        st.write(
            f"Latest Memory Time: {latest_memory[2]}"
        )

        st.caption(
            latest_memory[1]
        )

    else:
        st.info("No timeline data yet.")

    st.divider()

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])


user_question = st.chat_input(
    "Ask Feynman anything..."
)

if user_question:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    st.session_state.memory.add_user_message(
        user_question
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):

        with st.spinner("Feynman is thinking..."):

            rag_results = st.session_state.retriever.retrieve(
                user_question
            )

            context = "\n\n".join(
                rag_results["documents"][0]
            )

            relevant_memories = (
                st.session_state.memory
                .get_relevant_memories(
                    user_question,
                    top_k=3
                )
            )

            answer = st.session_state.gemini.generate_response(
                question=user_question,
                context=context,
                memories=relevant_memories,
                max_words=max_words
            )

            st.markdown(answer)

            try:
                audio_path = text_to_speech(
                    answer
                )

                with open(
                    audio_path,
                    "rb"
                ) as audio_file:

                    audio_bytes = audio_file.read()

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

            except Exception as e:
                st.warning(
                    f"Voice output failed: {e}"
                )

            st.session_state.memory.add_assistant_message(
                answer
            )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.expander("🧠 Retrieved Memories"):
                for memory in relevant_memories:
                    st.write(memory)

            with st.expander("📚 Retrieved Sources"):
                for source in rag_results["metadatas"][0]:
                    st.write(source)