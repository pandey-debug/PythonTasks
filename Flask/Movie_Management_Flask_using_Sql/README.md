# CineBook 🍿 — Premium Full-Stack Movie Booking System

This is a complete, production-grade movie reservation web application featuring a modern **Flask Frontend** and a robust **FastAPI Backend Service**. The application leverages SQLite, SQLAlchemy database models, Pydantic data schemas, and is styled with a gorgeous, responsive, cinematic dark-mode UI employing Tailwind CSS and Lucide Icons.

---

## 🏗️ System Architecture & Data Flow

```text
+-------------------+             +-----------------------+              +-----------------------+
|   Flask Client    |   HTTP      |    FastAPI Service    |  SQLAlchemy  |    SQLite Database    |
|   (Port 5000)     | ----------> |      (Port 8000)      | -----------> |  (movie_booking.db)   |
| (HTML + Tailwind) |             | (JSON REST/Valuation) |              | (Users/Movies/Book)   |
+-------------------+             +-----------------------+              +-----------------------+
```

1. **Flask Client (Port `5000`)**: Renders high-quality templates using Tailwind CSS for browse views, seat allocation calculations, ticket printing, and bookings management.
2. **FastAPI Backend (Port `8000`)**: Governs database access, handles model schema constraints, and automates booking codes (reference keys) generation.
3. **SQLite Database (`movie_booking.db`)**: Offers reliable local record persistence for members, screens, and reservation receipts.

---

## ⚡ Quick Start Instructions

Follow these commands to configure the libraries, initialize data, and run the service.

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Install Dependencies
Navigate into your project folder and run the installation script:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required Python packages
pip install -r requirements.txt
```

### 3. Run FastAPI Backend Service
Boot up the FastAPI database gate. This process will automatically instantiate the SQLite schema and seed mock movies so the app is instantly ready for use.

```bash
python uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
# Or directly run: python backend.py
```

### 4. Run Flask Web Client
Open another terminal/session, activate the virtual environment, and boot up the Flask customer controller:

```bash
python app.py
```

The web interface is now ready! Navigate to **`http://localhost:5000`** in any web browser.

---

## 🎟️ Core Features Included

- **🎬 Showcase Gallery**: Dynamic index displaying showtimes. Includes real-time movie searches without page reloads.
- **🛋️ Luxury Seating Grid**: Visual cinema floor diagram indicating occupied/available seats and automatic price/fee calculations.
- **👤 Identity Management**: Built-in user sign up and quick login authentication backed by Flask session cookies.
- **📋 Ticket Vault**: Access your past reservation stubs. Includes a fully operational button to cancel bookings and free up seating inventory.
- **🔧 System Management (Admin Panel)**: High-altitude KPI metrics dashboard. Allows system admins to mark showcases as completed or register new movies dynamically.

---

