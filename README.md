# Parking Management System - Backend

## Project Setup Instructions

Follow the steps below to set up and run the backend of the Parking Management System.

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.8 or higher
- Git

### Step 1: Clone the Repository

Start by cloning the backend GitHub repository to your local machine:

```bash
git clone https://github.com/akhilsai0099/Parking-Management-System-Backend.git
cd Parking-Management-System-Backend
```

### Step 2: Create and Activate a Virtual Environment

It's recommended to create a virtual environment to manage dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- **For Windows:**

  ```bash
  .\venv\Scripts\activate
  ```

- **For macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Required Packages

Install all required Python packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Backend (FastAPI)

1. **Navigate to the backend directory** (if not already there):

   ```bash
   cd Parking-Management-System-Backend
   ```

2. **Create a .env file:**

   - Open VSCode

   - Open a new file and save it with name a '.env' with no extension name.

   - Write the below inside the .env file

   ```bash
   SECRET_KEY=<your_secret_key>
   ```

3. **Start the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

   This will start the FastAPI server at `http://127.0.0.1:8000`.

4. **Verify the API is running:**

   Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the FastAPI documentation.

### Step 5: Testing the Backend

1. **API Testing with Pytest:**

   - Ensure that you are in the backend directory.
   - Run the following command to execute all tests:

   ```bash
   pytest
   ```

2. **API Testing with Postman:**

   - Open Postman and import the collection provided in the repository.
   - Run the test requests to verify API endpoints.

3. **Perform Load Testing (Optional):**

   Use tools like Apache JMeter or Postman Runner to simulate high-traffic scenarios and evaluate performance.

<br>

# API Documentation

### 1. **Register a User**

**Endpoint:** `POST /register/`  
**Description:** Register a new user.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

- **Success:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Failure (Email already registered):**
  ```json
  {
    "message": "Email already registered"
  }
  ```

### 2. **Login**

**Endpoint:** `POST /login/`  
**Description:** Authenticate a user and return a token.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

- **Success:**
  ```json
  {
    "token": "your_access_token",
    "role": false
  }
  ```
- **Failure (Invalid credentials):**
  ```json
  {
    "message": "Invalid email or password"
  }
  ```

### 3. **Create Parking Spot**

**Endpoint:** `POST /parking_spots/`  
**Description:** Create a new parking spot.

**Request Body:**

```json
{
  "level": 1,
  "section": "A",
  "spot_number": 101,
  "vehicle_type": "car",
  "exit_distance": 100,
  "short_term_only": false,
  "is_occupied": false
}
```

**Response:**

- **Success:**
  ```json
  {
    "id": 1,
    "level": 1,
    "section": "A",
    "spot_number": 101,
    "vehicle_type": "car",
    "exit_distance": 100,
    "short_term_only": false,
    "is_occupied": false,
    "created_at": "2024-09-08T00:00:00"
  }
  ```
- **Failure (Parking spot already exists):**
  ```json
  {
    "message": "Parking spot already exists"
  }
  ```

### 4. **Update Parking Spot**

**Endpoint:** `PUT /parking_spots/{spot_id}`  
**Description:** Update an existing parking spot.

**Request Body:**

```json
{
  "level": 2,
  "section": "B",
  "spot_number": 102,
  "vehicle_type": "motorcycle",
  "exit_distance": 200,
  "short_term_only": true,
  "is_occupied": true
}
```

**Response:**

- **Success:**
  ```json
  {
    "id": 1,
    "level": 2,
    "section": "B",
    "spot_number": 102,
    "vehicle_type": "motorcycle",
    "exit_distance": 200,
    "short_term_only": true,
    "is_occupied": true
  }
  ```

### 5. **Delete Parking Spot**

**Endpoint:** `DELETE /parking_spots/{spot_id}`  
**Description:** Delete a parking spot.

**Response:**

- **Success:**
  ```json
  {
    "message": "Parking spot deleted"
  }
  ```
- **Failure (Parking spot not found):**
  ```json
  {
    "message": "Parking spot not found"
  }
  ```

### 6. **Get All Parking Spots**

**Endpoint:** `GET /parking_spots/`  
**Description:** Retrieve all parking spots.

**Response:**

```json
[
  {
    "id": 1,
    "level": 1,
    "section": "A",
    "spot_number": 101,
    "vehicle_type": "car",
    "exit_distance": 100,
    "short_term_only": false,
    "is_occupied": false,
    "created_at": "2024-09-08T00:00:00"
  }
]
```

### 7. **Get Parking Spots by Level**

**Endpoint:** `GET /parking_spots/availability/level/{level}`  
**Description:** Retrieve parking spots by level.

**Response:**

```json
[
  {
    "id": 1,
    "level": 1,
    "section": "A",
    "spot_number": 101,
    "vehicle_type": "car",
    "exit_distance": 100,
    "short_term_only": false,
    "is_occupied": false,
    "created_at": "2024-09-08T00:00:00"
  }
]
```

### 8. **Get Parking Spots by Section**

**Endpoint:** `GET /parking_spots/availability/section/{section}`  
**Description:** Retrieve parking spots by section.

**Response:**

```json
[
  {
    "id": 1,
    "level": 1,
    "section": "A",
    "spot_number": 101,
    "vehicle_type": "car",
    "exit_distance": 100,
    "short_term_only": false,
    "is_occupied": false,
    "created_at": "2024-09-08T00:00:00"
  }
]
```

### 9. **Create Vehicle**

**Endpoint:** `POST /vehicles/`  
**Description:** Register a new vehicle.

**Request Body:**

```json
{
  "license_plate": "XYZ123",
  "vehicle_type": "car",
  "owner_id": 1,
  "owner_name": "John Doe",
  "contact_number": "123-456-7890"
}
```

**Response:**

- **Success:**
  ```json
  {
    "id": 1,
    "license_plate": "XYZ123",
    "vehicle_type": "car",
    "owner_id": 1,
    "owner_name": "John Doe",
    "contact_number": "123-456-7890"
  }
  ```

### 10. **Get All Vehicles**

**Endpoint:** `GET /vehicles/`  
**Description:** Retrieve all vehicles.

**Response:**

```json
[
  {
    "id": 1,
    "license_plate": "XYZ123",
    "vehicle_type": "car",
    "owner_id": 1,
    "owner_name": "John Doe",
    "contact_number": "123-456-7890"
  }
]
```

### 11. **Update Vehicle**

**Endpoint:** `PUT /vehicles/{id}`  
**Description:** Update vehicle information.

**Request Body:**

```json
{
  "license_plate": "XYZ123",
  "vehicle_type": "truck",
  "owner_id": 1,
  "owner_name": "John Doe",
  "contact_number": "123-456-7890"
}
```

**Response:**

- **Success:**
  ```json
  {
    "message": "Vehicle updated"
  }
  ```
- **Failure (Error details):**
  ```json
  {
    "message": "Error details"
  }
  ```

### 12. **Delete Vehicle**

**Endpoint:** `DELETE /vehicles/{id}`  
**Description:** Delete a vehicle.

**Response:**

- **Success:**
  ```json
  {
    "message": "Vehicle deleted"
  }
  ```
- **Failure (Error details):**
  ```json
  {
    "message": "Error details"
  }
  ```

### 13. **Create Parking Session**

**Endpoint:** `POST /parking_sessions/`  
**Description:** Start a new parking session.

**Request Body:**

```json
{
  "vehicle_id": 1,
  "entry_time": "2024-09-08T10:00:00",
  "expected_exit_time": "2024-09-08T12:00:00"
}
```

**Response:**

- **Success:**
  ```json
  {
    "message": "Parking session created"
  }
  ```
- **Failure (Error details):**
  ```json
  {
    "message": "Error details"
  }
  ```

### 14. **Delete Parking Session**

**Endpoint:** `DELETE /parking_sessions/{session_id}`  
**Description:** End a parking session.

**Response:**

- **Success:**
  ```json
  {
    "message": "Parking session deleted"
  }
  ```
- **Failure (Error details):**
  ```json
  {
    "message": "Error details"
  }
  ```

### 15. **Get All Parking Sessions**

**Endpoint:** `GET /parking_sessions/`  
**Description:** Retrieve all parking sessions.

**Response:**

```json
[
  {
    "id": 1,
    "vehicle_id": 1,
    "spot_id": 1,
    "entry_time": "2024-09-08T10:00:00",
    "actual_exit_time": null,
    "fee": null,
    "payment_status": "pending",
    "created_at": "2024-09-08T10:00:00"
  }
]
```

### 16. **Calculate Price and Exit**

**Endpoint:** `PUT /parking_sessions/{session_id}/price`  
**Description:** Calculate the parking fee and end the session.

**Response:**

- **Success:**
  ```json
  {
    "price": 10.5
  }
  ```
- \*\*Failure (Error

details):\*\*

```json
{
  "message": "Error details"
}
```

### 17. **Get Logs**

**Endpoint:** `GET /logs/`  
**Description:** Retrieve application logs.

**Response:**

```
2024-09-08 18:54:15,547 - main - INFO - Fetching all parking spots
2024-09-08 18:54:11,025 - main - INFO - User test@gmail.com logged in
2024-09-08 18:15:46,170 - main - INFO - Fetching all parking sessions
2024-09-08 - main - INFO - Fetching all vehicles
2024-09-08 18:15:44,731 - main - INFO - Fetching all parking spots
2024-09-08 18:15:44,720 - main - INFO - Fetching all parking spots
2024-09-08 18:15:37,183 - main - INFO - Fetching all parking spots
2024-09-08 18:15:32,510 - main - INFO - User test@gmail.com logged in
```

---
