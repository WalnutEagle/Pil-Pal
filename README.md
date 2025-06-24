## Overview

The workflow is a two-step process:
1.  **Identification (Multi-Modal):** The user uploads an image of a pill. The `Google Gemini Pro Vision` model analyzes the image to identify the pill's characteristics (color, shape, markings) and determine its likely name.
2.  **Information Retrieval (Agentic):** The textual description from the vision model is passed to a Langchain agent. This agent is equipped with a `Tavily` search tool, allowing it to autonomously search the web for detailed information about the identified medication, such as its usage, side effects, and dosage.

## Features

**Multi-Modal Input:** Accepts image uploads for pill identification.
**Intelligent Agent:** Uses a Langchain agent to perform dynamic, tool-based actions (web search).
**Interactive UI:** Built with Streamlit for a user-friendly, real-time chat experience.
**Stateful Conversation:** Remembers the context of the identified pill for follow-up questions.

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/Pill-Pal-Agent.git
    cd Pill-Pal-Agent
    ```

2.  **Create a `.env` file** and add your API keys:
    ```
    GOOGLE_API_KEY="YourGoogleApiKeyGoesHere"
    TAVILY_API_KEY="YourTavilyApiKeyGoesHere"
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    Your browser will open with the app. Upload an image of a pill to begin.
