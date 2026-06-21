# 🏦 Credit Card Approval Prediction System

A full-stack web application that predicts credit card approval using a **custom Decision Tree algorithm implemented from scratch** — no sklearn black boxes. Built with Flask, SQLite, and a clean banking-style UI.

---

## ✨ Features

- **Custom ML Model** — Decision Tree built from scratch using Gini Index for splitting
- **Real-time Prediction** — Instant approval/rejection prediction on form submission
- **Role-based Auth** — Separate login portals for users and admins
- **Admin Dashboard** — Review, approve, or reject applications with status tracking
- **Email Notifications** — Automated emails on application submission and status updates
- **Balanced Dataset** — Trained on a pre-processed, class-balanced dataset

---

## 🗂️ Project Structure

```
├── model.py                          # Custom Decision Tree (Node, Gini, split logic)
├── train.py                          # Model training script → saves .pkl
├── predict.py                        # Standalone prediction utility
├── app.py                            # Flask web app (routes, auth, DB, predictions)
├── test.py                           # Model testing script
├── test_email.py                     # Email notification test script
├── templates/                        # HTML templates (Jinja2)
│   ├── base.html                     # Landing page
│   ├── login.html / register.html
│   ├── dashboard.html                # User application history
│   ├── apply.html                    # Credit card application form
│   ├── admin.html / admin_login.html
│   ├── about.html / contact.html
├── static/                           # CSS, JS, assets
├── credit.ipynb                      # EDA & preprocessing notebook
├── new_credit.ipynb                  # Revised notebook with balanced dataset
├── application_record.csv            # Raw applicant data
├── credit_record.csv                 # Raw credit history data
├── Merged_Dataset.csv                # Merged raw dataset
├── Balanced_Credit_Card_Dataset.csv  # Final balanced training dataset
├── custom_decision_tree.pkl          # Trained custom model (primary)
├── decision_tree.pkl                 # Sklearn baseline model
└── decision_tree_balanced.pkl        # Sklearn model on balanced data
```

---

## ⚙️ How It Works

### ML Pipeline

1. **Data Prep** (`credit.ipynb` / `new_credit.ipynb`) — Merges `application_record.csv` and `credit_record.csv`, handles missing values, encodes categoricals, and balances classes.
2. **Model** (`model.py`) — Implements `DecisionTreeClassifierCustom` with:
   - Gini Index impurity calculation
   - Best-split search across all features and thresholds
   - Recursive tree building with configurable `max_depth` and `min_samples_split`
3. **Training** (`train.py`) — Loads the balanced dataset, trains the custom tree (default: depth=5, 5,000 samples), evaluates accuracy, and serializes to `custom_decision_tree.pkl`.
4. **Inference** (`app.py → predict_approval()`) — Encodes 14 form fields and calls `model.predict()` to return Approved/Rejected.

### Application Workflow

```
User registers → Fills application form → ML predicts outcome →
Admin reviews → Admin approves/rejects → Email sent to user
```

### Input Features (14)

Gender, Car ownership, Realty ownership, Number of children, Annual income, Income type, Education level, Family status, Housing type, Age, Work experience, Work phone, Occupation type, Family members

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install flask numpy pandas scikit-learn joblib
```

### Run

```bash
# 1. Train the model
python train.py

# 2. Start the web app
python app.py
```

App runs at `http://127.0.0.1:5000`

### Default Admin Credentials

| Field    | Value                   |
|----------|-------------------------|
| Email    | admin@smartcredit.com   |
| Password | admin123                |

---

## 📧 Email Notifications (Optional)

The app supports email alerts for application received, approved, and rejected events. Place a configured `email_utils.py` in the root directory to enable. The app runs normally without it.

---

## 🛠️ Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python, Flask                       |
| ML         | Custom Decision Tree (NumPy)        |
| Database   | SQLite                              |
| Frontend   | HTML/CSS/Jinja2                     |
| Auth       | SHA-256 password hashing, sessions  |
| Model I/O  | joblib                              |

---

## 📊 Dataset

Sourced from the [UCI Credit Card Approval dataset](https://www.kaggle.com/rikdifos/credit-card-approval-prediction). The two raw CSVs are merged and resampled to produce a class-balanced training set (`Balanced_Credit_Card_Dataset.csv`).

---

## 👤 Author

**ushaaaa33** — [GitHub](https://github.com/ushaaaa33)
