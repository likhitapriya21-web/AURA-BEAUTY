// Aura Boutique - Firebase Backend Configuration & Cloud Firestore Integration

// REPLACE THE CONFIG VALUES BELOW WITH YOUR FIREBASE PROJECT SETTINGS:
// You can get these in Firebase Console: https://console.firebase.google.com/
// Project Settings -> General -> Your apps -> Web app -> SDK setup and configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "aura-cosmetics-boutique.firebaseapp.com",
    projectId: "aura-cosmetics-boutique",
    storageBucket: "aura-cosmetics-boutique.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abcdef1234567890"
};

let db = null;
let auth = null;
let isFirebaseConnected = false;

// Initialize Firebase if valid configuration exists
(function initFirebase() {
    try {
        if (typeof firebase !== 'undefined' && firebaseConfig.apiKey && firebaseConfig.apiKey !== "YOUR_API_KEY") {
            firebase.initializeApp(firebaseConfig);
            db = firebase.firestore();
            auth = firebase.auth();
            isFirebaseConnected = true;
            console.log("🔥 Aura Firebase Cloud Backend: Connected successfully!");
            
            // Sign in anonymously if no auth present
            auth.onAuthStateChanged(user => {
                if (!user) {
                    auth.signInAnonymously().catch(err => console.warn("Firebase Auth Note:", err.message));
                }
            });
        } else {
            console.info("ℹ️ Aura Boutique: Using local storage backend (Firebase placeholder active). Enter your Firebase credentials in firebase-config.js to activate live Cloud Firestore.");
        }
    } catch (err) {
        console.warn("Firebase initialization warning (falling back to local cache):", err);
        isFirebaseConnected = false;
    }
})();

// Helper Functions for Firestore Backend
const FirebaseBackend = {
    isConnected: () => isFirebaseConnected && db !== null,

    // Save newly placed order to Firestore 'orders' collection
    async saveOrder(order) {
        if (!this.isConnected()) return null;
        try {
            const docRef = await db.collection("orders").doc(order.id).set({
                ...order,
                createdAt: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log("🔥 Order synced to Firebase Firestore:", order.id);
            return docRef;
        } catch (err) {
            console.error("Error saving order to Firestore:", err);
            return null;
        }
    },

    // Fetch order history from Firestore
    async getOrders() {
        if (!this.isConnected()) return null;
        try {
            const snapshot = await db.collection("orders").orderBy("createdAt", "desc").get();
            const cloudOrders = [];
            snapshot.forEach(doc => cloudOrders.push(doc.data()));
            return cloudOrders;
        } catch (err) {
            console.error("Error retrieving orders from Firestore:", err);
            return null;
        }
    },

    // Sync product inventory to Firestore 'products' collection
    async syncProduct(product) {
        if (!this.isConnected()) return null;
        try {
            await db.collection("products").doc(String(product.id)).set(product, { merge: true });
            console.log("🔥 Product updated in Firebase Firestore:", product.name);
        } catch (err) {
            console.error("Error syncing product to Firestore:", err);
        }
    },

    // Fetch all products from Firestore
    async getProducts() {
        if (!this.isConnected()) return null;
        try {
            const snapshot = await db.collection("products").get();
            if (snapshot.empty) return null;
            const cloudProducts = [];
            snapshot.forEach(doc => cloudProducts.push(doc.data()));
            return cloudProducts;
        } catch (err) {
            console.error("Error fetching products from Firestore:", err);
            return null;
        }
    },

    // Record stock receipt / inventory log
    async logInventoryReceipt(log) {
        if (!this.isConnected()) return null;
        try {
            await db.collection("inventory_logs").doc(log.id).set({
                ...log,
                serverTimestamp: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log("🔥 Inventory receipt logged to Firebase Firestore:", log.id);
        } catch (err) {
            console.error("Error logging inventory receipt to Firestore:", err);
        }
    }
};

window.FirebaseBackend = FirebaseBackend;
