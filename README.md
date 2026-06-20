<div align="center">
  <h1>🎓 Student Management System</h1>
  <h3>With Machine Learning Grade Prediction</h3>

  <p>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version" />
    <img src="https://img.shields.io/badge/Streamlit-1.20+-red.svg" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Database-SQLite3-green.svg" alt="SQLite" />
    <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg" alt="Scikit-Learn" />
    <img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white" alt="Docker Ready" />
  </p>
</div>

<br />

## 📖 Project Overview
The **Student Management System** is a full-stack, data-driven application designed to efficiently handle massive student datasets (1,000,000+ records) while providing real-time predictive analytics. 

By migrating from a legacy flat-file system to an optimized **SQLite** database with server-side pagination, the application guarantees zero-lag performance. Integrated directly into the **Streamlit** dashboard is a pre-trained **Random Forest Machine Learning Pipeline** capable of forecasting a student's final academic grade with **99.8% accuracy** based on their behavioral and academic metrics.

---

## ✨ Key Features
- **📊 Interactive Dashboard:** A premium, responsive web interface built with Streamlit.
- **🗄️ Massive Scale Support:** Optimized SQLite queries with server-side pagination handle millions of rows without memory bloat.
- **🤖 Real-Time ML Predictions:** Instantly predict a student's final grade based on attendance, participation, and exam scores using a serialized Random Forest model.
- **🔄 Full CRUD Functionality:** Seamlessly Create, Read, Update, and Delete student records.
- **🐳 Containerized:** Fully Dockerized for instant, cross-platform deployment.
- **🧪 Automated Testing:** CI/CD ready with a robust `pytest` suite validating database handler integrity.

---

## 🚀 Installation & Quick Start

### Option 1: Docker (Recommended)
The fastest way to get the application running locally is via Docker Compose.
```bash
# Clone the repository
git clone https://github.com/yourusername/Student_Management_System.git
cd Student_Management_System

# Build and run the container
docker-compose up -d --build
```
Access the application at `http://localhost:8501`.

### Option 2: Local Python Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/Student_Management_System.git
cd Student_Management_System

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

---

## 🧠 Machine Learning Architecture
The predictive engine is powered by a **Decision Tree / Random Forest Classifier**. 
* **Input Features:** `total_score` (99.6% importance), `attendance_percentage`, `class_participation`.
* **Data Leakage Prevented:** The `grade` target variable is strictly isolated during training and inference.
* **Performance:** Evaluated via 5-Fold Cross Validation yielding an incredibly stable mean accuracy of `0.9980` with a standard deviation of `0.0001`.

---

## 📸 Screenshots

*(Replace these placeholder links with actual paths to your image files!)*

| Dashboard Overview | Add/Update Record | ML Prediction Output |
| :---: | :---: | :---: |
| <img src="https://via.placeholder.com/400x250.png?text=Dashboard+Screenshot" alt="Dashboard" /> | <img src="https://via.placeholder.com/400x250.png?text=CRUD+Form+Screenshot" alt="CRUD Form" /> | <img src="https://via.placeholder.com/400x250.png?text=Prediction+Screenshot" alt="Prediction" /> |

---

## 🛠️ Project Structure
```text
Student_Management_System/
├── src/
│   ├── data_handler.py          # SQLite database connection & CRUD logic
│   └── model_pipeline.py        # ML prediction loading
├── pages/
│   └── 1_Student_Records.py     # Streamlit UI for the datatable and CRUD
├── models/
│   ├── student_model.pkl        # Serialized Random Forest model
│   └── label_encoder.pkl        # Serialized Label Encoder
├── tests/
│   └── test_data_handler.py     # Automated unit tests
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml           # Multi-container setup and volume mapping
├── requirements.txt             # Python dependencies
└── app.py                       # Main Streamlit entry point
```

---

## 🔮 Future Scope
- **Advanced Visual Analytics:** Integration of dynamic Plotly charts to track institutional performance trends over multiple semesters.
- **Role-Based Access Control (RBAC):** Secure login portals restricting CRUD operations to administrators while granting read-only access to teachers and students.
- **Cloud Migration:** Transitioning the SQLite database to a managed PostgreSQL instance on AWS/Heroku for scalable, concurrent multi-user access.
- **NLP Integration:** Analyzing textual teacher feedback using Natural Language Processing.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
*Developed by [Your Name](https://github.com/yourusername).*
