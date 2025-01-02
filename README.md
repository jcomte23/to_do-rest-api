# ToDo REST API

This is a REST API built with Flask for managing a ToDo list. The application allows users to perform CRUD operations (Create, Read, Update, Delete) on their tasks. It uses MongoDB for data persistence.

## Features

- **GET /to-do**: Retrieve all tasks.
- **POST /to-do**: Add a new task.
- **PUT /to-do/{id}**: Update an existing task by ID.
- **DELETE /to-do/{id}**: Delete a task by ID.

## Installation

Follow these steps to set up the project locally:

### 1. Clone the repository:
```bash
git clone https://github.com/jcomte23/todo-api.git
cd todo-api
```

### 2. Set up a virtual environment (optional but recommended):
```bash
python -m venv venv
```

### 3. Activate the virtual environment:
- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install dependencies:
```bash
pip install -r requirements.txt
```

### 5. Set up the `.env` file:
Create a `.env` file in the root directory of your project with the following content:
```
CONNECTION_STRING=your_mongodb_connection_string
```
Replace `your_mongodb_connection_string` with your actual MongoDB connection URI.

### 6. Run the application:
- Start the Flask application:
  ```bash
  python main.py
  ```
- The API will be available at `http://127.0.0.1:5000/`.

## Project Structure

```
todo-api/
│
├── src/
│   ├── app.py            # Main Flask application
│   ├── config/
│   │   └── mongodb.py    # MongoDB connection setup
│   ├── routes/
│       └── todo.py       # ToDo routes and logic
│
├── main.py               # Entry point to start the application
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables
```

## Technologies Used

- **Python**: Core programming language.
- **Flask**: Web framework for building the REST API.
- **MongoDB**: Database for data persistence.
- **dotenv**: To manage environment variables securely.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.