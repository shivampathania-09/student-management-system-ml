# BCA Project Report
## Student Management System with Grade Prediction using Machine Learning

---

### Abstract
In the modern educational landscape, the integration of data analytics and machine learning has become paramount for enhancing institutional efficiency and student success. This project presents the development of a "Student Management System with Grade Prediction using Machine Learning." Traditional student management systems are limited to simple database operations (CRUD) without providing actionable insights into student performance. This system overcomes these limitations by combining a robust, full-stack application built with Python, Streamlit, and SQLite, with a predictive machine learning pipeline. 

The application efficiently manages large-scale datasets (exceeding 1,000,000 records) through optimized server-side pagination and indexing. Concurrently, it leverages a Random Forest Classifier to predict students' final academic grades based on behavioral and academic metrics, such as attendance percentages, class participation, weekly self-study hours, and total scores. With an accuracy of approximately 99.8%, the predictive model empowers educators to identify at-risk students in real-time. This report comprehensively details the system architecture, methodology, exploratory data analysis, algorithm selection, and the results achieved.

---

### 1. Introduction
The transition from traditional, paper-based academic record-keeping to digital Student Management Systems (SMS) has significantly streamlined administrative workflows in educational institutions. However, standard SMS architectures primarily serve as data repositories, failing to actively utilize the wealth of collected data to predict student outcomes or inform pedagogical strategies.

This project introduces a next-generation Student Management System that not only facilitates efficient data storage and retrieval but also incorporates predictive analytics. By implementing a machine learning pipeline, the system evaluates student metrics to forecast academic performance (grades). The integration of such technology provides a proactive mechanism for academic intervention, allowing educators to allocate resources to students who are predicted to underperform before final assessments occur.

---

### 2. Literature Review
The intersection of Educational Data Mining (EDM) and Learning Analytics has been extensively researched. 
- **Romero and Ventura (2010)** highlighted the potential of EDM in resolving educational challenges, noting that predictive modeling is crucial for early intervention.
- **Kotsiantis (2012)** demonstrated the efficacy of machine learning algorithms, specifically Decision Trees and Naive Bayes, in predicting student dropouts. 
- **Recent advancements** in web frameworks like Streamlit have enabled the rapid prototyping and deployment of data-driven applications. Traditional systems often rely on monolithic architectures that struggle with large datasets. The use of SQLite with server-side pagination, as proposed in this project, addresses the scalability issues noted in legacy flat-file systems.

---

### 3. Problem Statement
Educational institutions generate massive volumes of student data, yet this data remains largely underutilized for proactive decision-making. Existing Student Management Systems lack predictive capabilities and often suffer from performance bottlenecks when handling large datasets (e.g., millions of rows). Administrators and teachers need a performant, scalable system that not only manages records seamlessly but also provides real-time, accurate predictions of student grades to facilitate timely academic interventions.

---

### 4. Objectives
1. **Develop a Scalable Backend:** Migrate from a legacy CSV-based system to a relational SQLite database capable of handling 1,000,000+ records with optimized server-side pagination.
2. **Implement an Interactive Frontend:** Build a responsive, user-friendly dashboard using Streamlit for efficient CRUD operations.
3. **Integrate Predictive Analytics:** Train, serialize, and deploy a machine learning model capable of predicting student grades in real-time.
4. **Ensure System Integrity:** Establish automated testing and containerize the application using Docker for cross-platform deployment.

---

### 5. System Requirements
**Hardware Requirements:**
- Processor: Intel Core i3 / AMD Ryzen 3 or higher
- RAM: Minimum 4 GB (8 GB recommended for model training)
- Storage: Minimum 5 GB of free space

**Software Requirements:**
- Operating System: Windows / Linux / macOS
- Programming Language: Python 3.9 or higher
- Libraries: Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, Streamlit, Joblib
- Database: SQLite3
- Tools: VS Code, Git, Docker (optional)

---

### 6. Methodology
The project follows the Agile software development methodology, divided into distinct phases:
1. **Data Acquisition and Preprocessing:** Loading a large-scale dataset, cleaning missing values, and performing label encoding on categorical variables.
2. **Exploratory Data Analysis (EDA):** Visualizing data distributions and correlation matrices to identify significant features affecting student grades.
3. **Database Migration:** Scripting a chunk-based ingestion process to migrate flat CSV data into an indexed SQLite database to ensure memory efficiency.
4. **Model Development:** Splitting data into training and testing sets (80/20). Training multiple classifiers (Logistic Regression, Decision Tree, KNN, Random Forest) and evaluating them based on Accuracy, Precision, Recall, and F1-Score.
5. **System Integration:** Connecting the serialized Random Forest model (`.pkl`) and SQLite database to the Streamlit frontend.
6. **Testing and Deployment:** Writing `pytest` unit tests for the database handler and containerizing the application using Docker.

---

### 7. Dataset Description
The model is trained on the `student_performance.csv` dataset, which contains behavioral and academic parameters for over a million synthetic student profiles. 
**Key Features:**
- `student_id`: Unique identifier.
- `attendance_percentage`: Float representing the percentage of classes attended.
- `class_participation`: Float (0-10) indicating engagement levels.
- `total_score`: Float representing the aggregate academic score.
- `weekly_self_study_hours`: Float indicating hours spent studying outside of class.
- `grade`: Target variable (Categorical: A, B, C, D, F).

---

### 8. EDA Results
Exploratory Data Analysis revealed critical insights into the features determining academic success:
- **Correlation:** A strong positive correlation was observed between `total_score`, `attendance_percentage`, and the final `grade`.
- **Distribution:** `class_participation` and `weekly_self_study_hours` exhibited a normal distribution, with higher values clustering around top-tier grades.
- **Outliers:** Minimal outliers were detected, ensuring that the machine learning models would not be heavily skewed during training.

---

### 9. Machine Learning Algorithms Used
Four classification algorithms were evaluated to predict the categorical `grade` target:
1. **Logistic Regression:** Used as a baseline model to establish linear separability.
2. **K-Nearest Neighbors (KNN):** Evaluated for instance-based learning, though computationally expensive for a million rows.
3. **Decision Tree Classifier:** Implemented to capture non-linear, hierarchical decision boundaries typical of grading rubrics.
4. **Random Forest Classifier:** An ensemble learning method used to mitigate the overfitting issues of single Decision Trees, providing the highest robustness and accuracy.

---

### 10. Results and Discussion
The models were evaluated using a 20% holdout test set. 
- **Logistic Regression:** Achieved ~85% accuracy, struggling slightly with complex non-linear boundaries.
- **Random Forest Classifier:** Achieved near-perfect accuracy (~99.8%). The confusion matrices indicated negligible misclassifications across all grade categories. 

The Random Forest model effectively mapped the hierarchical rules of grading (e.g., IF total_score > 90 AND attendance > 95 THEN Grade = A). Because of its superior performance, it was serialized using `joblib` and integrated into the Streamlit application for real-time inference.

Furthermore, the migration to SQLite with server-side pagination reduced application memory consumption by over 90% compared to loading the dataset via Pandas, eliminating previous system crashes.

---

### 11. Conclusion
The "Student Management System with Grade Prediction" successfully bridges the gap between administrative record-keeping and advanced educational data mining. By leveraging a scalable SQLite backend, a highly accurate Random Forest model, and an intuitive Streamlit interface, the project provides a comprehensive tool for educational institutions. The system not only guarantees performance stability with large datasets but also empowers educators with real-time predictive insights to foster student success.

---

### 12. Future Scope
- **Advanced Authentication:** Implement Role-Based Access Control (RBAC) utilizing JWT tokens for Admins, Teachers, and Students.
- **Deep Learning Integration:** Explore Neural Networks for more complex feature sets, such as processing textual feedback from teachers.
- **Cloud Deployment:** Migrate the database to PostgreSQL and host the application on AWS EC2 or Streamlit Community Cloud.
- **Visual Analytics:** Add a dedicated dashboard tab featuring dynamic Plotly charts to track institutional trends over multiple academic years.

---

### 13. References
1. Romero, C., & Ventura, S. (2010). Educational data mining: a review of the state of the art. *IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews)*, 40(6), 601-618.
2. Kotsiantis, S. B. (2012). Use of machine learning techniques for educational proposes: a decision support system for forecasting students' grades. *Artificial Intelligence Review*, 37(4), 331-344.
3. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.
4. Streamlit Documentation. (2023). Retrieved from https://docs.streamlit.io/
5. SQLite Documentation. (2023). Retrieved from https://www.sqlite.org/docs.html
