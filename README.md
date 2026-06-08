# 🤖 Chatbot version 2.2

A modern, fast, and responsive personal AI chatbot application featuring a glassmorphic React frontend and a FastAPI backend with local AI integration (Ollama).

---

## 🌟 Features

- 🎨 **Premium Glassmorphic UI:** Smooth micro-animations, copy-to-clipboard functionality, and responsive layouts.
- ⚡ **FastAPI Backend:** Lightweight and high-performance API services.
- 🧠 **Hybrid Query Processing:**
  - Automated setup/greeting memory.
  - Integration with Wikipedia API for factual queries.
  - Fallback to local AI via **Ollama** (`llama3.2`).
- 🕒 **Live Tools:** Built-in current time query.
- 🐳 **Docker Support:** Fully containerized setup for easy deployments.
- 🚀 **One-Click Startup:** A unified startup script (`start.sh`) to launch both servers simultaneously.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React, Vite | Modern UI framework and lightning-fast bundler. |
| **Styling** | Vanilla CSS | Custom responsive glassmorphic styles. |
| **Icons** | Lucide React | Clean, scalable vector icons. |
| **Backend** | FastAPI, Uvicorn | High-performance Python web framework and ASGI server. |
| **AI Engine** | Ollama (`llama3.2`) | Local LLM integration for private AI responses. |

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.10+**
2. **Node.js 18+**
3. **Ollama** (optional, for local AI processing)
   - Install from [Ollama's official website](https://ollama.com).
   - Pull the model:
     ```bash
     ollama pull llama3.2
     ```

### ⚡ Easy Start (Linux / macOS)

You can launch both the backend and frontend simultaneously using the included startup script:

```bash
chmod +x start.sh
./start.sh
```

---

## 🔧 Manual Setup

If you prefer to run each service individually:

### 1. Backend Setup

1. Navigate to the root directory and create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn api.index:app --port 8000 --reload
   ```
   *The backend will be available at `http://localhost:8000`.*

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install package dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev -- --port 5173
   ```
   *The frontend will be available at `http://localhost:5173`.*

---

## 🐳 Docker Deployment

To run the application inside a container:

1. Build the Docker image:
   ```bash
   docker build -t chatbot-v2.2 .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 chatbot-v2.2
   ```

---

## 📁 Repository Structure

```
├── api/
│   └── index.py        # FastAPI Backend logic and endpoints
├── frontend/
│   ├── src/
│   │   ├── App.jsx     # Main React interface
│   │   ├── index.css   # Main CSS styles
│   │   └── main.jsx    # Vite application entrypoint
│   ├── package.json    # Frontend dependency configuration
│   └── vite.config.js  # Vite dev server configuration
├── Dockerfile          # Container configuration
├── requirements.txt    # Python backend dependencies
├── start.sh            # One-click launch shell script
└── README.md           # Project documentation
```
