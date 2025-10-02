# Karavali Mitra

Karavali Mitra is a Flutter-based chatbot application that provides travel guide suggestions, itineraries, and tourist spot recommendations for regions like Udupi, Mangalore, and South Canara. It integrates Google Sign-In for authentication, Google Maps for location visualization, Geolocator for real-time location access, and a Python FastAPI backend for AI-powered responses using FAISS for semantic search, Hugging Face's Mistral model for generation, Tavily for web search fallback, and Redis for caching.

The app sends user queries and locations to the backend, which retrieves relevant information from a pre-built knowledge base or falls back to web searches.

## Features
- Google OAuth login for secure authentication.
- Real-time location detection and interactive mapping with Google Maps.
- Search-based chatbot for personalized travel recommendations (e.g., famous places, cuisine, festivals, accommodations, and transportation).
- Backend AI processing with semantic search (FAISS), natural language generation (Mistral via Hugging Face), web search fallback (Tavily), and caching (Redis).
- Cross-platform support: Android, iOS, macOS, Windows, and Web.
- Markdown-formatted responses for clear, structured itineraries and suggestions.

## Prerequisites

### Flutter (Frontend)
- **Flutter SDK**: Version 3.24.0 or later (as specified in `.metadata` and `pubspec.lock`).
- **Dart SDK**: Version 3.6.0 or later (as per `pubspec.yaml` environment).
- **Development Tools**:
  - Android Studio (with Android SDK) for Android development and emulation.
  - Xcode (version 15 or later) for iOS and macOS development and simulation.
  - Visual Studio (with Desktop development with C++ workload) for Windows builds.
  - Chrome or Edge for Web development.
- **API Keys and Configurations**:
  - Google Maps API Key: Required for maps integration. Enable Maps SDK for Android/iOS/JavaScript in Google Cloud Console.
  - Google Sign-In Client ID: Already hardcoded in `lib/main.dart` (e.g., '807837243380-ku6eat428jbumbo5dkovndj7lp3h9t8f.apps.googleusercontent.com'). Verify/setup in Google Cloud Console under OAuth 2.0 Client IDs.
  - Firebase Project: For authentication (firebase_auth package); configure in Google Cloud and add `google-services.json` (Android) and `GoogleService-Info.plist` (iOS).
- **Hardware/Emulator Requirements**: For location features (Geolocator), use a physical device or emulator with GPS simulation enabled. Permissions must be granted at runtime.

### Backend (Python)
- **Python**: Version 3.10 or later (recommended for compatibility with libraries like PyTorch in Hugging Face).
- **Dependencies**: Install via `pip` (listed in detail for reproducibility):
  - `fastapi`: Core framework for the API.
  - `uvicorn`: ASGI server to run FastAPI.
  - `sentence-transformers`: For generating embeddings (model: 'all-MiniLM-L6-v2').
  - `faiss-cpu`: For vector similarity search (switch to `faiss-gpu` if you have CUDA-enabled GPU).
  - `redis`: Python client for Redis caching.
  - `huggingface-hub`: For accessing Hugging Face Inference API (Mistral model).
  - `requests`: For making HTTP calls to Tavily API.
  - `pydantic`: For data validation in FastAPI models.
  - `pickle`: Built-in, for serializing text mappings.
  - `traceback`: Built-in, for error handling.
  - Additional for dataset generation: `pandas`, `faker`, `random`, `json`.
- **External Services**:
  - Redis Server: Version 7.x or later. Install via package manager (e.g., `brew install redis` on macOS, or download from redis.io for Windows).
  - Hugging Face API Key: Free tier available; sign up at huggingface.co and generate a token.
  - Tavily API Key: Sign up at tavily.com for a free/paid API key (used for web search fallback).
- **FAISS Index Files**: `knowledge_base_semantic.index` and `text_mapping.pkl` must be generated (see setup below).

### Other Tools
- **Git**: For version control and cloning the repository.
- **Node.js**: Optional for web builds (Flutter handles it internally).
- **Docker**: Optional for containerizing the backend (e.g., for production deployment).

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/RandomForestPanda/Karavali-Mitra.git
cd karavali-mitra
```

### 2. Frontend (Flutter) Setup
1. Ensure Flutter is installed and configured:
   ```bash:disable-run
   flutter doctor  # Verify setup; fix any issues (e.g., Android licenses, Xcode agreements)
   ```
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Generate mocks for testing (using build_runner):
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```
4. Platform-Specific Configurations:
   - **Android**:
     - Add Google Maps API key to `android/app/src/main/AndroidManifest.xml`:
       ```xml
       <meta-data android:name="com.google.android.geo.API_KEY" android:value="YOUR_GOOGLE_MAPS_API_KEY"/>
       ```
     - Update package name in `AndroidManifest.xml` and `build.gradle` to `com.solmelu.karavalimitra` (or your custom name) for consistency.
     - Enable location permissions in `AndroidManifest.xml` (already partially set; add if missing).
   - **iOS**:
     - Add Google Maps API key and Sign-In client ID to `ios/Runner/Info.plist`:
       ```xml
       <key>GMSServicesProvideAPIKey</key>
       <string>YOUR_GOOGLE_MAPS_API_KEY</string>
       <key>CFBundleURLTypes</key>
       <array>
         <dict>
           <key>CFBundleTypeRole</key>
           <string>Editor</string>
           <key>CFBundleURLSchemes</key>
           <array>
             <string>com.googleusercontent.apps.YOUR_CLIENT_ID</string>
           </array>
         </dict>
       </array>
       ```
     - Update bundle ID in Xcode to match (e.g., `com.solmelu.karavalimitra`).
     - Add location permissions to `Info.plist` (e.g., `NSLocationWhenInUseUsageDescription`).
   - **Web**:
     - Add Google Maps JS API key to `web/index.html` (already set; replace placeholder).
     - Ensure CORS is allowed in backend for web origin (already `*` in app.py; restrict in prod).
   - **Desktop (Windows/macOS)**: No extra config; Flutter handles it.
5. Clean and rebuild if needed:
   ```bash
   flutter clean
   flutter pub get
   ```

### 3. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd Backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sentence-transformers faiss-cpu redis huggingface-hub requests pydantic pandas faker
   # If using GPU: pip install faiss-gpu instead of faiss-cpu
   ```
4. Start Redis Server:
   - Run in a separate terminal: `redis-server` (ensure it's running on localhost:6379; check with `redis-cli ping`).
5. Generate the Tourism Dataset:
   ```bash
   python dataset_gen.py
   ```
   - Outputs: `south_canara_tourism_dataset.json`, `.csv`, and `.jsonl`.
6. Build the FAISS Index:
   - Create and run `build_faiss_index.py` (as provided in previous instructions):
     ```bash
     python build_faiss_index.py
     ```
   - This generates `knowledge_base_semantic.index` and `text_mapping.pkl`.
7. Configure API Keys in `app.py`:
   - Replace `HF_API_KEY = 'Your Hf key Here'` with your Hugging Face token.
   - Replace `TAVILY_API_KEY = 'Your Tavily Key Here'` with your Tavily key (corrected typo from "Tvaily").
8. Test Backend Connections:
   - Ensure Redis responds: Add a test in `app.py` (e.g., `redis_client.set('test', 'value')`).
   - Verify FAISS loads: Run the server and query `/search`.

### 4. Running the Application

#### Backend
1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
   - Access API docs/Swagger at `http://localhost:8000/docs`.
   - Test endpoints: POST `/search` with JSON body `{ "user_id": "123", "query": "Top places in Udupi" }`.

#### Frontend (Flutter)
1. Ensure backend is running (Flutter connects to `http://127.0.0.1:8000` or your IP).
2. Run the app:
   - Android/iOS: `flutter run` (select device/emulator).
   - Web: `flutter run -d chrome` (or other browser).
   - Windows: `flutter run -d windows`.
   - macOS: `flutter run -d macos`.
3. Usage Flow:
   - Login with Google.
   - Grant location permissions (for maps and sending lat/long to backend).
   - Enter queries in the search field (e.g., "Best beaches in Mangalore").
   - View AI responses in Markdown format below the search bar.

## Troubleshooting
- **Flutter Build Errors**: Run `flutter doctor` and `flutter analyze`. Fix package name inconsistencies.
- **Location Issues**: Check `permission_handler` logs; ensure `geolocator` is configured (e.g., Android min SDK 21+).
- **Auth Errors**: Verify Google Client ID in code and console. For web, enable third-party cookies.
- **Backend Failures**: 
  - Redis: Check connection errors; restart server.
  - FAISS/HF: Ensure files exist; check API rate limits (Hugging Face free tier has limits).
  - Tavily: Verify key; handle 500 errors by checking query limits.
- **Maps Not Displaying**: Confirm API key and billing enabled in Google Cloud.
- **CORS Problems**: If frontend can't reach backend, verify CORS middleware in `app.py`.
- **Performance**: For large datasets, optimize FAISS (e.g., use IndexIVFFlat for speed).

## Known Issues
- Limited to South Canara regions; expand `tourism_data` in `dataset_gen.py` for broader coverage.
- No advanced error handling (e.g., for missing index files); add try-except in `app.py`
- Web Builds: Google Sign-In may require additional setup for CORS and OAuth redirects

## Deployment
- **Flutter**:
  - Web: `flutter build web --release`; host on Firebase Hosting or Vercel.
  - Android: `flutter build apk --release`; sign and upload to Google Play.
  - iOS: `flutter build ipa --release`; archive in Xcode and submit to App Store.
- **Backend**:
  - Deploy to Heroku, Vercel, or AWS EC2/Lambda.
  - Use Docker: Create a `Dockerfile` for FastAPI/Redis.
  - Environment: Use `python-dotenv` for keys; scale Redis with cloud services (e.g., Redis Labs).
- **Limitations**: rate-limit API endpoints; FAISS as vector store - operational overhead of FAISS at a deployment level is a potential concern, Works well for a prototype/POC but not ideal for deployments.


```
