# Welcome to your Expo app 👋

This is an [Expo](https://expo.dev) project created with [`create-expo-app`](https://www.npmjs.com/package/create-expo-app).

## Get started

1. Install dependencies

   ```bash
   npm install
   ```

2. Start the app

   ```bash
   npx expo start
   ```

In the output, you'll find options to open the app in a

- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), a limited sandbox for trying out app development with Expo

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

# AI Text Detector App

A beautiful React Native (Expo) application with FastAPI backend for detecting AI-generated text vs human-written content.

## 🚀 Features

- **Modern UI**: Clean and aesthetically pleasing interface with gradient headers and themed components
- **Real-time Analysis**: Send text to FastAPI backend for AI detection
- **Confidence Scoring**: Get percentage-based confidence scores with visual indicators
- **Cross-platform**: Works on iOS, Android, and Web
- **Dark/Light Mode**: Supports system theme preferences
- **Educational Content**: Learn about AI detection in the Explore tab

## 📱 Frontend (React Native/Expo)

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Expo CLI

### Installation & Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run web      # For web
npm run ios      # For iOS simulator  
npm run android  # For Android emulator
npm start        # For Expo DevTools
```

## 🔧 Backend (FastAPI)

### Prerequisites
- Python 3.8 or higher
- pip

### Installation & Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:
```bash
python fastapi_server.py
```

The API will be available at:
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### API Endpoints

#### POST `/detect`
Analyze text for AI detection.

**Request Body:**
```json
{
  "text": "Your text to analyze here"
}
```

**Response:**
```json
{
  "prediction": "Human" | "AI",
  "confidence": 85.7
}
```

#### GET `/health`
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Text Detector API is running"
}
```

## 🎨 App Screenshots

### Main Screen
- Clean text input area with placeholder text
- Analyze and Clear buttons
- Results display with prediction badge and confidence score
- Visual progress bar for confidence level

### Explore Screen
- Information about AI detection
- Confidence score explanations
- API integration details
- Limitations and best practices

## 🔧 Configuration

### Updating API URL
To change the FastAPI server URL, edit the `analyzeText` function in `app/(tabs)/index.tsx`:

```typescript
const response = await axios.post('YOUR_API_URL/detect', {
  text: inputText
});
```

### Customizing Themes
Colors and themes can be modified in:
- `constants/Colors.ts` - App color scheme
- Individual component styles in the screen files

## 🧠 AI Detection Logic

The current implementation uses a simple heuristic-based approach for demonstration:

- **Text Patterns**: Analyzes repetition, complexity, coherence, and formality
- **Scoring Algorithm**: Combines multiple indicators to make predictions
- **Confidence Calculation**: Provides percentage-based confidence scores

### Replacing with Real ML Model

To integrate a real AI detection model:

1. Replace the `make_prediction` function in `fastapi_server.py`
2. Add your model loading and inference code
3. Update the feature extraction logic
4. Adjust the response format if needed

## 📦 Project Structure

```
ai-text-detector/
├── app/
│   ├── (tabs)/
│   │   ├── index.tsx          # Main AI detection screen
│   │   ├── explore.tsx        # Information and help screen
│   │   └── _layout.tsx        # Tab navigation layout
│   └── _layout.tsx            # Root layout
├── components/                # Reusable UI components
├── constants/                 # App constants and colors
├── hooks/                     # Custom React hooks
├── assets/                    # Images and fonts
├── fastapi_server.py          # FastAPI backend server
├── requirements.txt           # Python dependencies
└── package.json              # Node.js dependencies
```

## 🚀 Deployment

### Frontend Deployment
For production deployment of the React Native app:
- **Web**: Use `npm run build` and deploy to Vercel, Netlify, etc.
- **Mobile**: Use Expo Application Services (EAS) for app store deployment

### Backend Deployment
For production deployment of the FastAPI server:
- Use services like Railway, Heroku, or AWS
- Configure CORS for your production domain
- Set up proper environment variables
- Use a production WSGI server like Gunicorn

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the FastAPI server is running and CORS is properly configured
2. **Module Not Found**: Run `npm install` to install missing dependencies
3. **Server Connection**: Verify the API URL in the frontend matches your FastAPI server
4. **PowerShell Execution Policy**: Use `npm install` instead of `npx` commands if you encounter PowerShell restrictions

### Getting Help

- Check the console/logs for detailed error messages
- Verify both frontend and backend are running
- Test the API endpoints using the FastAPI docs at `/docs`

## Learn more

To learn more about developing your project with Expo, look at the following resources:

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.
