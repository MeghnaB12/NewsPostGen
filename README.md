
# NewsPostGen 🤖

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-blueviolet?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered API that uses LangChain and the Google Gemini API to find recent news on any topic and automatically generate a professional LinkedIn post.

This project was built as an personal work.

---

## 🚀 Live Demo

You can test the live API and see the Swagger documentation here:

**[https://newspostgen.onrender.com/docs](https://newspostgen.onrender.com/docs)**

### Demo Screenshot
Here is the live Swagger UI in action:

![NewsPostGen Swagger UI](demo-swagger.png)

---

## ✨ Core Features

* **Recent News:** Uses the Tavily search tool to find *recent* articles from the web.
* **AI-Powered Content:** Leverages the Google Gemini API (`gemini-2.0-flash`) to write a professional and engaging summary.
* **Ready-to-Use Output:** Returns a clean JSON response with:
    * `topic`: The original topic.
    * `news_sources`: A list of source URLs.
    * `linkedin_post`: The generated post text.
    * `image_suggestion`: A text-based idea for a post image.

## 🛠️ Tech Stack

* **Backend:** FastAPI, Uvicorn
* **AI Orchestration:** LangChain
* **LLM:** Google Gemini (`gemini-2.0-flash`)
* **Web Search:** Tavily Search API
* **Deployment:** Render

---

## ⚙️ How to Run This Project Locally

### 1. Prerequisites
* Python 3.10+
* Git

### 2. Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MeghnaB12/NewsPostGen.git](https://github.com/MeghnaB12/NewsPostGen.git)
    cd NewsPostGen
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows, use `venv\Scripts\activate`)*

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    * Copy the example file:
        ```bash
        cp .env.example .env
        ```
    * Edit the `.env` file and add your secret API keys from Google AI Studio and Tavily.

### 3. Run the Server
```bash
uvicorn main:app --reload
