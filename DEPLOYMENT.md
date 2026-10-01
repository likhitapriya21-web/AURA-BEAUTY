# Aura Beauty Boutique - Hosting & Deployment Architecture

This project is configured with a modern, decoupled production architecture:
- **Frontend Hosting**: **Vercel** (Global Edge CDN with sub-second asset delivery) or **Firebase Hosting**
- **Cloud Backend**: **Firebase Cloud Firestore & Authentication** (Real-time orders, dynamic inventory sync, product catalog, and supply logs)
- **AI Diagnostic Engine**: **Streamlit Cloud** (Python ML recommender system)

---

## 1. Firebase Backend Setup (Cloud Firestore & Auth)

The application includes real-time Firebase Firestore synchronization with offline local fallback.

### Step 1: Create a Firebase Project
1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Click **Create a project** and name it (e.g. `aura-cosmetics-boutique`).
3. Under **Build**:
   - **Firestore Database**: Click *Create Database* in **Production mode** (or test mode).
   - **Authentication**: Enable *Anonymous* and/or *Email/Password* provider.

### Step 2: Configure Your Credentials
1. In Firebase Console, go to **Project Settings** (gear icon) -> **General**.
2. Scroll to **Your apps**, click the **Web** (`</>`) icon, and register the app.
3. Copy the `firebaseConfig` object and paste it into [`Aura.com/firebase-config.js`](file:///c:/Users/LENOVO/OneDrive/Desktop/cosmetic_recommendation_system%20(2)/cosmetic_recommendation_system/Aura.com/firebase-config.js):
```javascript
const firebaseConfig = {
    apiKey: "AIzaSy...",
    authDomain: "aura-cosmetics-boutique.firebaseapp.com",
    projectId: "aura-cosmetics-boutique",
    storageBucket: "aura-cosmetics-boutique.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abcdef"
};
```

### Step 3: Deploy Firestore Security Rules via Firebase CLI
Run the following in PowerShell:
```powershell
npm install -g firebase-tools
firebase login
firebase deploy --only firestore
```
> The included [`firestore.rules`](file:///c:/Users/LENOVO/OneDrive/Desktop/cosmetic_recommendation_system%20(2)/cosmetic_recommendation_system/firestore.rules) will automatically be deployed to secure your `products`, `orders`, and `inventory_logs` collections!

---

## 2. Frontend Hosting on Vercel

The repository includes pre-configured [`vercel.json`](file:///c:/Users/LENOVO/OneDrive/Desktop/cosmetic_recommendation_system%20%282%29/cosmetic_recommendation_system/vercel.json) files at both root and subfolder levels for zero-configuration deployment.

### Option A: 1-Click via GitHub (Recommended)
1. Push your code to GitHub (see Section 4).
2. Go to [vercel.com/new](https://vercel.com/new).
3. Import the repository **`likhitapriya21-web/AURA-BEAUTY`**.
4. Leave all settings default (Vercel automatically detects [`vercel.json`](file:///c:/Users/LENOVO/OneDrive/Desktop/cosmetic_recommendation_system%20(2)/cosmetic_recommendation_system/vercel.json)).
5. Click **Deploy**.
   - Your frontend will be live on `https://aura-beauty.vercel.app` with instant SSL and worldwide CDN!

### Option B: Deploy via Vercel CLI
In your terminal:
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\cosmetic_recommendation_system (2)\cosmetic_recommendation_system"
npx vercel
```
For production:
```powershell
npx vercel --prod
```

---

## 3. Hosting on Firebase (Target: https://aura-cosmetics-boutique.web.app)

To deploy the frontend directly to Firebase Hosting:
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\cosmetic_recommendation_system (2)\cosmetic_recommendation_system"
firebase deploy --only hosting
```
Your boutique will immediately go live at:
**`https://aura-cosmetics-boutique.web.app`** (and `https://aura-cosmetics-boutique.firebaseapp.com`)

---

## 4. Git Commands to Commit & Push Deployment Configurations

To commit the new Firebase backend and Vercel hosting configurations and push them to GitHub:

```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\cosmetic_recommendation_system (2)\cosmetic_recommendation_system"

# 1. Check newly added files
git status

# 2. Stage all hosting and backend files
git add vercel.json Aura.com/vercel.json firebase.json .firebaserc firestore.rules firestore.indexes.json Aura.com/firebase-config.js Aura.com/index.html Aura.com/script.js Aura.com/styles.css DEPLOYMENT.md

# 3. Commit changes
git commit -m "feat: configure Vercel frontend hosting and Firebase Firestore backend"

# 4. Push to GitHub main branch
git push -u origin main
```
