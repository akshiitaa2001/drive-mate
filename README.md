# Drive-Mate

## Project Overview
**Drive-Mate** is an end-to-end project that demonstrates the development of a data-driven application for managing vehicle rentals. This project integrates user management, vehicle booking, data storage, automated ETL pipelines, and interactive visualizations to showcase skills in Python, Flask, PostgreSQL, AWS, and Streamlit.

---

## Features
### 1. User Details Collection
- Frontend: HTML form with Flask backend.
- Features: 
  - Data validation.
  - Storage of user details in a PostgreSQL database.

### 2. Vehicle Rental Process
- Booking page where users select vehicles and rental dates.
- Backend features:
  - Validation of rental data.
  - Logging of rental transactions.
  - Confirmation display.

### 3. ETL Process
- Automated ETL pipeline for data processing.
- Features:
  - Frontend status page to monitor and manually trigger the ETL process.
  - Display of the last data load timestamp.
- Technology: Python-based ETL pipeline, integrated with PostgreSQL.

### 4. Data Visualization
- Interactive dashboards using Streamlit.
- Features:
  - Visualization of rental trends, vehicle usage, and other analytics.
  - Integrated into a dashboard page for user-friendly insights.

 ### 5. Recommendation System
- Uses MapReduce to generate personalized recommendations.
- Features:
  - Item-based collaborative filtering approach.
  - Identifies similarities between items based on rental history.
  - Provides tailored recommendations to users for vehicles they are likely to rent.
- Technology: Python-based MapReduce implementation.

---

## Project Workflow
1. **User Registration**
    - Users fill out their details using an HTML form.
2. **Vehicle Rental**
    - Users book vehicles through the rental interface.
3. **ETL Process**
    - Data is processed, cleaned, and loaded into the data warehouse.
4. **Visualization**
    - Dashboards display actionable insights from the data.
5. **Recommendation System**
    - Personalized vehicle recommendations generated for users.

---

## Technologies Used
- **Frontend:** Flask, HTML, CSS (Deployed on Railway)
- **Backend:** Python
- **Database:** PostgreSQL (Hosted on AWS RDS)
- **Visualization:** Streamlit
- **ETL Pipeline:** Custom Python scripts
- **Recommendation System:** MapReduce for collaborative filtering
- **Cloud Platforms:**
  - Railway: Frontend deployment
  - AWS RDS: Database hosting
  - AWS EC2: Execution of Python scripts
  - Streamlit: Visualizations to drive business insights
- **Version Control:** GitHub

---

## Setup Instructions
### Prerequisites
1. Python 3.7+
2. PostgreSQL
3. Flask
4. Streamlit
5. AWS EC2 (optional for deployment)

### Steps to Run Locally
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/drive-mate.git
    cd drive-mate
    ```
2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up the PostgreSQL database:
    - Create a database named `vehicle_rental`.
    - Run the `database.py` script to create tables and insert initial data.
4. Start the Flask application:
    ```bash
    python app.py
    ```
5. Access the application at `http://localhost:5000`.
6. Run the ETL pipeline:
    ```bash
    python etl_process.py
    ```
7. Generate recommendations:
    ```bash
    python recommendation_system.py
    ```
8. View visualizations:
    ```bash
    streamlit run dashboard.py
    ```

---

## AWS Deployment
- All scripts (e.g., `database.py`, `etl_process.py`, `recommendation_system.py`) are stored on GitHub and pulled to AWS EC2 for execution.
- The database is hosted on AWS RDS for reliable and scalable storage.
- The frontend is deployed on Railway for easy and efficient access.
- Streamlit dashboards provide business insights through interactive visualizations.

---

## Project Insights
This project demonstrates the following skills:
- Backend development with Flask and Python.
- Database design and management with PostgreSQL.
- Building ETL pipelines for data processing.
- Interactive data visualization using Streamlit.
- MapReduce implementation for collaborative filtering recommendations.
- Cloud deployment across multiple platforms (Railway, AWS RDS, AWS EC2).

---

## Future Improvements
- Add advanced analytics features such as predictive vehicle demand.
- Enhance the frontend design for better user experience.
- Implement authentication and user role management.

---

## Contributors
- **Akshita Agrawal**
  - [LinkedIn](https://linkedin.com/in/akshita-agrawal)
  - [GitHub](https://github.com/akshita-agrawal)

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
