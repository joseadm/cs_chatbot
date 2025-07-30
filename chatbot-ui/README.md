# RAG Chatbot UI

A modern React-based chat interface for your RAG (Retrieval-Augmented Generation) chatbot API.

## Features

- 🎨 Clean, modern chat interface similar to professional chatbot systems
- 💬 Real-time messaging with typing indicators
- 📱 Responsive design (works on desktop and mobile)
- 🔗 Direct integration with your FastAPI backend
- ⚡ Click-to-send example questions
- 🕒 Message timestamps

## Setup Instructions

### 1. Start your API server first
In the parent directory (`../`), make sure your FastAPI server is running:

```bash
cd ../
./venv/bin/python api.py
```

The API should be running at `http://localhost:8000`

### 2. Install and start the React app

```bash
# Install dependencies
npm install

# Start the development server
npm start
```

The app will open at `http://localhost:3000`

## How to Use

1. **Example Questions**: Click any question in the left sidebar to auto-fill the input
2. **Type Your Question**: Enter your question in the input field at the bottom
3. **Send**: Press Enter or click the send button
4. **Get AI Response**: The chatbot will retrieve relevant information from your PDF and provide an AI-generated response

## Customization

### Update Example Questions
Edit the `exampleQuestions` array in `src/App.tsx` to match your PDF content:

```typescript
const exampleQuestions = [
  "Your custom question 1?",
  "Your custom question 2?",
  // Add more questions relevant to your PDF
];
```

### Change API URL
If your API is running on a different port or host, update the fetch URL in `src/App.tsx`:

```typescript
const response = await fetch('http://your-api-url:port/chat', {
  // ... rest of the code
});
```

### Styling
Modify `src/App.css` to customize colors, fonts, and layout to match your brand.

## Troubleshooting

1. **"Connection Error"**: Make sure your FastAPI server is running at `http://localhost:8000`
2. **CORS Issues**: The API is configured to allow all origins. In production, update the CORS settings in your API
3. **Example questions don't work**: Make sure your PDF contains information relevant to the example questions

## Production Deployment

For production:

1. **Build the React app**: `npm run build`
2. **Deploy the build folder** to your web server
3. **Update API URL** to your production API endpoint
4. **Configure CORS** in your API to only allow your domain
