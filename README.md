
# AI-Powered Root Cause Analysis Assistance

An AI-driven web application that automatically generates **three independent 5-Why Root Cause Analyses (RCA)** from a construction quality issue or task description.

The application helps quality engineers, project managers, and site teams quickly identify potential root causes and corrective actions using Large Language Models (LLMs).

---

## Features

* Generate **3 independent 5-Why analyses**
* Produces:

  * Why 1 to Why 5
  * Corresponding responses
  * Root Cause
  * Corrective Action
* Construction quality and project management focused
* JSON report download support
* Multiple AI model fallback system
* Web-based interface using Streamlit
* Cloud deployment support

---

## Problem Statement

Construction quality teams often spend significant time preparing Root Cause Analysis (RCA) reports for site observations, non-conformances, and quality deviations.

This application automates the process by generating structured RCA reports from a simple task description provided by the user.

### Example Input

```text
Balance whitewash paint work is pending on the ceiling in some portions of the OPD building first slab around installed HVAC ducts, fire-fighting pipelines, and electrical conduits.
```

### Example Output

```text
Analysis 1                               Analysis 2                 Analysis 3
Execution / Workmanship Perspective      :                          :

Why 1                                    :                          :      
Response 1

Why 2                                    :                          :
Response 2

...

Root Cause

Corrective Action                        :                           :
```

The application generates three different perspectives:

1. Execution / Workmanship Perspective
2. Supervision / Coordination Perspective
3. Planning / Process Control Perspective

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Models

#### Primary Models

* Gemini 2.5 Flash Lite
* Gemini 2.5 Flash

#### Fallback Models

* Groq Llama 3.3 70B Versatile
* Groq Llama 3.1 8B Instant

### Libraries

* google-genai
* groq
* streamlit
* python-dotenv
* json

---

## Project Structure

```text
rca-quality-assistance/
│
├── app.py
├── examples.txt
├── prompt_template.txt
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### File Description

#### app.py

Main Streamlit application.

#### examples.txt

Reference RCA examples used for prompt engineering.

#### prompt_template.txt

Prompt template used to instruct the LLM.

#### requirements.txt

Python dependencies.

#### .env

Stores API keys locally.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/<your-username>/rca-quality-assistance.git

cd rca-quality-assistance
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key

GROQ_API_KEY=your_groq_api_key
```

---

## Run Application

```bash
streamlit run app.py
```


---

## Deployment

The application can be deployed using:

* Streamlit Community Cloud
* Azure App Service
* AWS
* Google Cloud Run
* Docker Containers

Current deployment uses:

```text
Streamlit Community Cloud
```

---

## AI Model Fallback Strategy

The application automatically switches models if a provider quota is exhausted.

```text
Gemini 2.5 Flash Lite
        ↓
Gemini 2.5 Flash
        ↓
Groq Llama 3.3 70B
        ↓
Groq Llama 3.1 8B
```

This improves application availability and reliability.

---

## Use Cases

* Construction Quality Management
* Site Observation Reports
* NCR Investigation
* Quality Audits
* Project Coordination Reviews
* Corrective Action Planning
* Engineering Documentation

---

## Future Enhancements

* PDF report export
* Excel report export
* RCA history management
* User authentication
* Multi-project support
* Image-based defect analysis
* Construction document integration
* AI Agent workflow support

---

## Author

**Roshni Debnath**

---

## License

This project is developed for educational and industrial quality management purposes.

---

