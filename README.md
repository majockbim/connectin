# Connectin

## About

If you ever wanted though about having a 'coffee chat' with a cracked LinkedIn user but wouldn't know what to say, ConnectIn is for you!

## Features

- AI-powered coffee chat question generation
- LinkedIn profile analysis
- Personalized networking conversation starters
- RESTful API backend
- Modern web interface

## Technology Stack

### Backend
- FastAPI
- Mistral 7B AI Model (via llama-cpp-python)
- Playwright for web scraping
- BeautifulSoup for HTML parsing

### Frontend
- [frontend technologies here]


### Developers

**Backend Developer**: [Majock Bim](https://github.com/majockbim)
- API development
- AI model integration
- LinkedIn scraping implementation

**Frontend Developer**: [Carson Carrasco](https://github.com/CarsonCarrasco)
- [info here]

## Getting Started

### Prerequisites

- LinkedIn account credentials

### Installation

1. Clone the repository:
```bash
git clone https://github.com/majockbim/connectin.git
cd connectin
```

2. Backend setup:
```bash
cd backend
pip install -r requirements.txt
python -m playwright install chromium
```

3. Environment configuration:
```bash
# Create .env file in backend directory
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
```

4. Download the AI model:
   - Follow instructions in mistral_README.txt to install `mistral-7b-instruct-v0.1.Q4_K_M.gguf` in `backend/app/models/`

5. Start the backend server:
```bash
cd connectin
python -m backend.main
```

6. Frontend setup:
```bash
cd frontend
npm run dev

# frontend installation steps here
```

## API Documentation

Once the backend is running, visit:
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000`

### Main Endpoint

```http
POST /generate
Content-Type: application/json

{
  "learner_url": "https://linkedin.com/in/student-profile",
  "mentor_url": "https://linkedin.com/in/mentor-profile"
}
```

## Project Structure

```
connectin/
├── backend/
│   ├── app/
│   ├── prompt_engine.py
│   │   ├── models/
│   │   │   └── mistral-7b-instruct-v0.1.Q4_K_M.gguf
│   │   └── utils/
│   │       └── scraper.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── [Frontend files]
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request


## Acknowledgments

- Mistral AI for the language model
- LinkedIn for profile data
- FastAPI and Playwright communities

Honourable Mention: [Junior Assani](https://github.com/juniorassani) for creating the first and only pull request.
