# 🌿 LeafGuard: Mango Leaf Disease Classification

LeafGuard is an AI-powered web application designed to assist mango farmers by providing instant diagnosis of common mango leaf diseases using a Convolutional Neural Network (CNN) model.

The system uses a Flask backend, a responsive frontend, and a trained deep learning model to classify leaf diseases accurately and efficiently.

---

## 🚀 Features

* 📸 Upload mango leaf images
* 🤖 AI-based disease prediction
* 📊 Multi-class classification
* 💬 Chatbot support for disease information
* 🌐 User-friendly web interface

---

## 🧠 Model Details

* Model: CNN (MobileNetV2-based)
* Framework: TensorFlow / Keras
* Accuracy: ~98%
* Format: `.h5`

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS3, JavaScript, Jinja2
* **Backend:** Python (Flask)
* **Database:** MySQL
* **Machine Learning:** TensorFlow / Keras

---

## ⚙️ Setup and Installation

### 📌 Prerequisites

* Python (3.9 – 3.11 recommended)
* MySQL Server
* Git

---

### 🧩 Steps

#### 1. Clone Repository

```bash
git clone https://github.com/deekshithprasad8050/AI-Driven-Visual-Detection-of-Multiple-Disease-in-Mango-Leaves-Using-Convolutional-Neural-Networks.git
cd AI-Driven-Visual-Detection-of-Multiple-Disease-in-Mango-Leaves-Using-Convolutional-Neural-Networks
```

---

#### 2. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

---

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

#### 4. Database Setup

Create database:

```sql
CREATE DATABASE leafguard_db;
```

Import schema:

```bash
mysql -u root -p leafguard_db < database.sql
```

---

#### 5. Run Application

```bash
python app.py
```

👉 Open in browser:
http://127.0.0.1:5000/

---

## 📂 Project Structure

```
backend/
ml_model_files/
src/
app.py
config.py
database.sql
requirements.txt
```

---

## 📸 Screenshots (Add Images Here)

* Upload Page
* Prediction Result
* Dashboard

(You can add images like below)

```md
![App Screenshot](screenshots/home.png)
```

---

## ⚠️ Note

The trained model file is included using Git LFS due to its large size.

---

## 🎯 Use Cases

* Farmers for early disease detection
* Smart agriculture systems
* Research applications

---

## 🔮 Future Scope

* Mobile app integration
* Real-time camera detection
* Multi-crop disease classification
* Cloud deployment

---

## 👨‍💻 Author

**Deekshith Prasad R**
