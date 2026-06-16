import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from groq import Groq


# -----------------------------
# Helper functions
# -----------------------------

def load_text_file(file_path):
    """Read text content from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def build_prompt(task_description):
    """Create final prompt using reference examples and user task description."""
    examples = load_text_file("examples.txt")
    prompt_template = load_text_file("prompt_template.txt")

    final_prompt = prompt_template.replace("{examples}", examples)
    final_prompt = final_prompt.replace("{task_description}", task_description)

    return final_prompt


def clean_json_response(response_text):
    """Clean response if model returns markdown JSON block."""
    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()
    elif response_text.startswith("```"):
        response_text = response_text.replace("```", "").strip()

    return response_text

def generate_with_groq(prompt):
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        groq_api_key = st.secrets.get("GROQ_API_KEY", None)

    if not groq_api_key:
        raise Exception("Groq API key not found")

    client = Groq(api_key=groq_api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def generate_with_groq(prompt):
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        groq_api_key = st.secrets.get("GROQ_API_KEY", None)

    if not groq_api_key:
        raise Exception("Groq API key not found")

    client = Groq(api_key=groq_api_key)

    groq_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]

    last_error = ""

    for model_name in groq_models:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )

            st.caption(f"Generated using model: Groq {model_name}")
            return response.choices[0].message.content

        except Exception as e:
            last_error = str(e)
            continue

    raise Exception(f"All Groq models failed: {last_error}")

def generate_rca(task_description):
    """Generate RCA using Gemini first, then Groq as fallback."""

    load_dotenv()

    prompt = build_prompt(task_description)

    # -------------------------
    # GEMINI FALLBACK MODELS
    # -------------------------

    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        gemini_api_key = st.secrets.get("GEMINI_API_KEY", None)

    gemini_models = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash"
    ]

    if gemini_api_key:
        gemini_client = genai.Client(api_key=gemini_api_key)

        for model_name in gemini_models:
            try:
                response = gemini_client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                cleaned_response = clean_json_response(response.text)
                rca_data = json.loads(cleaned_response)

                st.caption(f"Generated using model: {model_name}")
                return rca_data

            except Exception:
                continue

    # -------------------------
    # GROQ FALLBACK MODELS
    # -------------------------

    try:
        groq_response = generate_with_groq(prompt)

        cleaned_response = clean_json_response(groq_response)
        rca_data = json.loads(cleaned_response)

        return rca_data

    except Exception as e:
        st.error("Daily quota for all the models exhausted. Please try again later.")
        st.text(str(e))
        return None

def display_analysis(title, analysis):
    """Display one RCA analysis in a clean format."""
    st.subheader(title)

    for i in range(1, 6):
        st.markdown(f"**Why {i}:** {analysis.get(f'why_{i}', '')}")
        st.markdown(f"**Response {i}:** {analysis.get(f'response_{i}', '')}")
        st.write("")

    st.markdown("**Root Cause:**")
    st.info(analysis.get("root_cause", ""))

    st.markdown("**Corrective Action:**")
    st.success(analysis.get("corrective_action", ""))


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="AI RCA Quality Assistant",
    layout="wide"
)

st.title("AI-Powered Root Cause Analysis Generator")

st.write(
    "Generate three independent 5-Why analyses with responses, root causes, "
    "and corrective actions from a construction quality task description."
)

st.divider()

task_description = st.text_area(
    "Provide the task description",
    placeholder="Example: Balance whitewash paint work is pending on the ceiling in some portions of the OPD building first slab...",
    height=150
)

generate_button = st.button("Generate 5 Why Analysis")

if generate_button:
    if not task_description.strip():
        st.warning("Please enter a task description.")
    else:
        with st.spinner("Generating RCA analysis..."):
            result = generate_rca(task_description)

        if result:
            st.success("RCA generated successfully.")

            tab1, tab2, tab3 = st.tabs(["Analysis 1", "Analysis 2", "Analysis 3"])

            with tab1:
                display_analysis("Analysis 1 - Execution / Workmanship Perspective", result.get("analysis_1", {}))

            with tab2:
                display_analysis("Analysis 2 - Supervision / Coordination Perspective", result.get("analysis_2", {}))

            with tab3:
                display_analysis("Analysis 3 - Planning / Process Control Perspective", result.get("analysis_3", {}))

            st.divider()

            st.download_button(
                label="Download JSON Report",
                data=json.dumps(result, indent=4, ensure_ascii=False),
                file_name="rca_report.json",
                mime="application/json"
            )