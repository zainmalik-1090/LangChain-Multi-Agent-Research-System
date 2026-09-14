import streamlit as st
from src.pipelines.pipeline import run_research_pipeline

# Page setup
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            color: #6c757d;
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar settings & details
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown(
        """
    **Architecture Overview:**
    * **Search Agent**: Queries real-time sources.
    * **Reader Agent**: Scrapes and extracts in-depth article content.
    * **Writer Chain**: Synthesizes structured markdown reports.
    * **Critic Chain**: Evaluates structure, facts, and assigns a rating.
    """
    )
    st.divider()
    st.caption("Powered by LangChain, LangGraph & Google Gemini")

# Header Section
st.markdown(
    '<div class="main-title">🔎 Multi-Agent Deep Research System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Automate topic investigation, web extraction, report drafting, and critique through collaborative LLM agents.</div>',
    unsafe_allow_html=True,
)

# Input Area
topic = st.text_input(
    "Enter a research topic:",
    placeholder="e.g., Quantum Computing breakthroughs in drug discovery",
)

start_button = st.button("🚀 Start Deep Research", type="primary")

# Run Pipeline and Display Steps
if start_button:
    if not topic.strip():
        st.warning("Please enter a valid research topic to begin.")
    else:
        with st.status(
            "Running Research Pipeline...", expanded=True
        ) as status_box:
            st.write("🛰️ **Step 1:** Search Agent collecting initial web data...")

            try:
                # Execute pipeline
                final_state = run_research_pipeline(topic)

                st.write(
                    "📄 **Step 2:** Reader Agent selecting and scraping deep sources..."
                )
                st.write("✍️ **Step 3:** Writer drafting the finalized report...")
                st.write("⚖️ **Step 4:** Critic reviewing and scoring the output...")

                status_box.update(
                    label="Research Completed Successfully!",
                    state="complete",
                    expanded=False,
                )

                # Output presentation in clean tabs
                tab_report, tab_critic, tab_raw = st.tabs(
                    ["📑 Final Report", "🎯 Critique & Score", "🔍 Raw Data"]
                )

                with tab_report:
                    st.subheader("Research Report")
                    st.markdown(final_state.get("report", "No report generated."))
                    st.download_button(
                        label="📥 Download Report (Markdown)",
                        data=final_state.get("report", ""),
                        file_name=f"{topic.replace(' ', '_')}_report.md",
                        mime="text/markdown",
                    )

                with tab_critic:
                    st.subheader("Agent Feedback & Quality Assessment")
                    st.markdown(
                        final_state.get(
                            "feedback", "No critique feedback generated."
                        )
                    )

                with tab_raw:
                    st.subheader("Extracted Source Content")
                    with st.expander("Search Results Summary", expanded=False):
                        st.write(
                            final_state.get(
                                "search_results", "No search data found."
                            )
                        )

                    with st.expander("Deep Scraped Content", expanded=False):
                        st.write(
                            final_state.get(
                                "scraped_content", "No scraped data found."
                            )
                        )

            except Exception as e:
                status_box.update(
                    label="Pipeline execution failed.",
                    state="error",
                    expanded=True,
                )
                st.error(f"Execution Error: {e}")