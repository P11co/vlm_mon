# VLM Monitor

This repo provides a small prototype for capturing screenshots of the active window and summarising them with the OpenAI API. It also includes a minimal Streamlit frontend for quick testing.

## Requirements
- Python 3.10+
- [OpenAI Python library](https://pypi.org/project/openai/)
- `mss`, `pyautogui`, `python-dotenv`, `streamlit`

## Setup
1. Install dependencies:
   ```bash
   pip install openai mss pyautogui python-dotenv streamlit
   ```
2. Create a `.env.local` file with your `OPENAI_API_KEY`.

## Usage

Run the capture session directly:
```bash
python monitor.py
```

Or start the Streamlit prototype:
```bash
streamlit run frontend.py
```
