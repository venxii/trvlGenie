// src/firebase.js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";
import { getStorage } from "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyB9cOc6vUgAQdByX7Hq4YKzngsFBnvYacU",
  authDomain: "trvlgenie-65d83.firebaseapp.com",
  projectId: "trvlgenie-65d83",
  storageBucket: "trvlgenie-65d83.firebasestorage.appspot.com",
  messagingSenderId: "798345781966",
  appId: "1:798345781966:web:2d1c2efb53a9127cc6a69f",
  measurementId: "G-39JDWDRJPF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Export Firebase services
export const db = getFirestore(app);
export const auth = getAuth(app);
export const storage = getStorage(app);
