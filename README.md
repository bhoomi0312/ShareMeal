# 🍲 ShareMeal: Zero-Waste Campus Logistics Platform

**ShareMeal** is a real-time, full-stack logistics platform designed to eliminate food wastage in college messes and institutional cafeterias. It connects mess administrators directly with local NGOs, campus support staff, and volunteer networks to distribute surplus food before it spoils.

---

## 🚀 The Problem & The Solution
Every day, perfectly good food is thrown away simply due to a lack of immediate communication. ShareMeal solves this by creating an ultra-fast, decentralized marketplace for surplus food.

* **For the Mess Admin:** A secure dashboard to list leftover food, set an expiry time, and track exactly who claimed it with private contact logs.
* **For the NGO/Recipient:** A real-time, public board to see what food is available, where it is, and claim the exact number of servings they need.

---

## ✨ Key Features
* **Real-Time State Management:** When a recipient claims food, available servings update instantly across the network.
* **Smart Expiry Tracking:** Food listings require a "Fresh For" time limit to ensure hygiene and food safety.
* **Privacy & Accountability:** Recipient contact details are securely logged for the Admin to verify pickups, but are completely hidden from the public recipient dashboard.
* **Zero-Friction UI:** Built with Tailwind CSS for a modern, responsive, mobile-friendly experience.

---

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Pydantic (Data Validation)
* **Frontend:** HTML5, Asynchronous JavaScript (Fetch API), Tailwind CSS
* **Architecture:** RESTful API with an in-memory data store for hyper-fast localized testing.

---

## 📁 Project Structure

```text
sharemeal_project/
├── main.py              # FastAPI backend engine and routing
├── README.md            # Project documentation
└── static/
    └── index.html       # Frontend UI and JavaScript logic
```

HOW TO RUN LOCALLY?

1. Clone the repository
   git clone [https://github.com/bhoomi0312/ShareMeal.git](https://github.com/bhoomi0312/ShareMeal.git)
cd ShareMeal
2.Set up a virtual environment
  (a)python3 -m venv venv
  (b)source venv/bin/activate
3.Install the required dependencies
  pip install fastapi uvicorn pydantic
4. Start the live server
   uvicorn main:app --reload --port 8001
5. Open the App
  Open your web browser and navigate to: http://127.0.0.1:8001

