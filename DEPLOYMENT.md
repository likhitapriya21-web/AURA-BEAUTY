# Aura Beauty Boutique - Hosting & Deployment Architecture

This project is configured with a modern, decoupled production architecture:
- **Frontend Hosting**: **Firebase Hosting** (`https://aura-beauty-82fd4.web.app`) or **Vercel** (`https://aura-beauty.vercel.app`)
- **Cloud Backend**: **Firebase Cloud Firestore & Authentication** on project **`aura-beauty-82fd4`** (Real-time orders, dynamic inventory sync, product catalog, and supply logs)
- **AI Diagnostic Engine**: **Streamlit Cloud** (Python ML recommender system)

---

## 1. Firebase Backend & Project Setup (`aura-beauty-82fd4`)

- **Firebase Console:** [https://console.firebase.google.com/u/0/project/aura-beauty-82fd4/overview](https://console.firebase.google.com/u/0/project/aura-beauty-82fd4/overview)

### Step 1: In Your Firebase Console
1. Under **Build**:
   - **Firestore Database**: Click *Create Database* in **Production mode** (or test mode).
   - **Authentication**: Enable *Anonymous* and/or *Email/Password* provider.
2. In **Project Settings** (gear icon) -> **General**:
   - Under **Your apps**, if not already registered, click the **Web** (`</>`) icon.
   - Register your app as `Aura Boutique`.
   - Copy your `firebaseConfig` keys and paste them into [`Aura.com/firebase-config.js`](file:///c:/Users/LENOVO/OneDrive/Desktop/cosmetic_recommendation_system%20(2)/cosmetic_recommendation_system/Aura.com/firebase-config.js):
```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_FROM_CONSOLE",
    authDomain: "aura-beauty-82fd4.firebaseapp.com",
    projectId: "aura-beauty-82fd4",
    storageBucket: "aura-beauty-82fd4.firebasestorage.app",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```
*(Note: When hosted on Firebase Hosting, the app will also auto-connect via Firebase Hosting's built-in SDK loader)*

### Step 2: Deploy to Firebase Hosting & Firestore
In your terminal:
```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\cosmetic_recommendation_system (2)\cosmetic_recommendation_system"

# Log in to Google account associated with aura-beauty-82fd4
firebase login

# Deploy both Hosting (Aura.com) and Firestore Security Rules
firebase deploy
```
*To deploy only hosting:*
```powershell
firebase deploy --only hosting
```

Your boutique will immediately go live at:
- **`https://aura-beauty-82fd4.web.app`**
- **`https://aura-beauty-82fd4.firebaseapp.com`**

---

## 2. Frontend Hosting on Vercel (Alternative / Multi-Cloud)

The repository also includes pre-configured [`vercel.json`](file:///c:/Users/LENOVO/OneDrive/Desktop/cosmetic_recommendation_system%20(2)/cosmetic_recommendation_system/vercel.json) files for multi-cloud deployment.

### Option A: 1-Click via GitHub
1. Push your code to GitHub (see Section 3).
2. Go to [vercel.com/new](https://vercel.com/new).
3. Import the repository **`likhitapriya21-web/AURA-BEAUTY`**.
4. Click **Deploy**.
   - Your frontend will be live on `https://aura-beauty.vercel.app` with instant SSL and worldwide CDN!

---

## 3. Git Commands to Commit & Push

To commit all configurations and push them to your GitHub repository:

```powershell
cd "c:\Users\LENOVO\OneDrive\Desktop\cosmetic_recommendation_system (2)\cosmetic_recommendation_system"

# 1. Check status
git status

# 2. Stage all files
git add .

# 3. Commit changes
git commit -m "feat(firebase): connect aura-beauty-82fd4 live Firebase project and hosting"

# 4. Push to GitHub main branch
git push -u origin main
```
