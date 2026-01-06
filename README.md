
# 🏥 FastAPI Patient Management System

A complete **FastAPI-based Patient Management System** demonstrating real-world REST API development using **FastAPI + Pydantic**.  
This project covers **CRUD operations, path & query parameters, data validation, computed fields (BMI), and JSON-based persistence**.

---

## 🚀 Features

- FastAPI REST API
- Pydantic models with validation
- Computed fields (`bmi`, `verdict`)
- CRUD operations (Create, Read, Update, Delete)
- Path & Query parameters
- Sorting using query params
- JSON file–based storage
- Automatic Swagger UI documentation

---

## 🛠 Tech Stack

- **Python 3.9+**
- **FastAPI**
- **Pydantic**
- **Uvicorn**

---

## 📂 Project Structure

.
├── main.py  
├── patients_200.json  
├── requirements.txt  
└── README.md  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/fastapi-patient-management-system.git
cd fastapi-patient-management-system
```

### 2️⃣ Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

Server will start at:
http://127.0.0.1:8000

---

## 📘 API Documentation

- Swagger UI → http://127.0.0.1:8000/docs  
- ReDoc → http://127.0.0.1:8000/redoc  

---

## 🔗 API Endpoints

### 🏠 Home
GET /

### ℹ️ About
GET /about

### 👀 View All Patients
GET /view

### 🔍 View Single Patient
GET /patient/{patient_id}

### 🔃 Sort Patients
GET /sort?sort_by=bmi&order=asc

Valid sort fields:
- height
- weight
- bmi
- age

### ➕ Create Patient
POST /crate

### ✏️ Update Patient
PUT /update/{patient_id}

### ❌ Delete Patient
DELETE /delete/{patient_id}

---

## 🧠 BMI & Verdict Logic

BMI = weight / (height²)

Verdict:
- Underweight
- Normal
- Overweight
- Obese

---

## 📌 Purpose

This project is ideal for:
- Learning FastAPI from basics to advanced
- Understanding Pydantic deeply
- Building resume-ready backend projects

---

## 👨‍💻 Author

**Saikat Santra**  
M.Tech, IIT Kharagpur  

---

⭐ If you like this project, give it a star on GitHub!
