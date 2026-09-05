# FlyRank Backend Track - Task Manager API

A FastAPI REST API for task management and user authentication, built for the FlyRank Internship Backend Track.

The application uses PostgreSQL to store tasks, Supabase Auth to manage users and verify access tokens, and Docker Compose to run the API and database.

---

## Features

* Create, read, update, and delete tasks
* PostgreSQL database persistence
* User signup with Supabase Auth
* User login with access and refresh tokens
* Protected routes using bearer tokens
* Reusable authentication dependency
* User logout
* Public and protected API endpoints
* Interactive Swagger UI documentation
* Docker and Docker Compose support

---

## Technologies Used

* Python
* FastAPI
* PostgreSQL
* Psycopg
* Supabase Auth
* Docker
* Docker Compose
* Swagger UI

---

## Project Structure

* `main.py` - FastAPI application, routes, authentication, and database logic
* `compose.yaml` - Runs the FastAPI and PostgreSQL containers
* `Dockerfile` - Builds the FastAPI Docker image
* `.env.example` - Example environment variables without real secrets
* `.gitignore` - Prevents `.env` and other unwanted files from being committed
* `.dockerignore` - Prevents secrets and unnecessary files from entering the Docker image
* `requirements.txt` - Python dependencies
* `screenshots/` - Project screenshots

---

## Environment Configuration

Create a file named `.env` in the project root.

Add the following environment variables:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

Replace `your_supabase_project_url` and `your_supabase_anon_key` with the values from your Supabase project.

The real `.env` file is ignored by Git and must never be committed.

The repository includes `.env.example` to show which environment variables are required without exposing real values.

---

## Supabase Setup

1. Create a project at [Supabase](https://supabase.com/).
2. Open the project dashboard.
3. Open **Project Settings → API**.
4. Copy the project URL into `SUPABASE_URL`.
5. Copy the anon/public key into `SUPABASE_KEY`.
6. Do not use the `service_role` key.
7. Open **Authentication → Sign In / Providers → Email**.
8. Disable email confirmation for testing this assignment.

Supabase manages user accounts, hashes passwords, and creates signed access tokens. This application does not store or hash user passwords.

---

## Running with Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/RasemMaraqa/FlyRankAI.git
cd FlyRankAI
```

### 2. Create the `.env` file

Copy `.env.example` to `.env` and add your real Supabase project values.

On PowerShell:

```powershell
Copy-Item .env.example .env
```

### 3. Build and start the containers

```bash
docker compose up --build
```

### 4. Open the application

* Root endpoint: http://localhost:8000/
* Health check: http://localhost:8000/health
* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

Use `localhost:8000` in the browser. Do not use `0.0.0.0:8000`.

To stop the application, press `Ctrl+C`.

---

## API Endpoints

### General and Task Endpoints

| Method | Endpoint           | Description                      | Authentication |
| :----- | :----------------- | :------------------------------- | :------------- |
| GET    | `/`                | Display API information          | No             |
| GET    | `/health`          | Check whether the API is running | No             |
| GET    | `/tasks`           | Retrieve all tasks               | No             |
| GET    | `/tasks/{task_id}` | Retrieve one task                | No             |
| POST   | `/tasks`           | Create a task                    | No             |
| PUT    | `/tasks/{task_id}` | Update a task                    | No             |
| DELETE | `/tasks/{task_id}` | Delete a task                    | No             |

### Authentication Endpoints

| Method | Endpoint               | Description                                  | Authentication |
| :----- | :--------------------- | :------------------------------------------- | :------------- |
| POST   | `/auth/signup`         | Create a new user account                    | No             |
| POST   | `/auth/login`          | Log in and receive access and refresh tokens | No             |
| POST   | `/auth/logout`         | Log out the authenticated user               | Bearer token   |
| GET    | `/public/info`         | Retrieve public information                  | No             |
| GET    | `/protected/profile`   | Retrieve the authenticated user's profile    | Bearer token   |
| GET    | `/protected/dashboard` | Retrieve protected dashboard information     | Bearer token   |

---

## Authentication Flow

1. The user creates an account using `POST /auth/signup`.
2. The user logs in using `POST /auth/login`.
3. Supabase returns an access token and a refresh token.
4. The access token is sent to protected routes in the `Authorization` header.
5. The API asks Supabase to verify the access token.
6. The protected route runs only when the token is valid.

The authorization header uses this format:

```text
Authorization: Bearer ACCESS_TOKEN
```

A missing, invalid, changed, or expired access token returns status code `401 Unauthorized`.

---

## Testing Authentication in Swagger UI

1. Start the application:

```bash
docker compose up --build
```

2. Open http://localhost:8000/docs.

3. Open `POST /auth/signup` and create a user:

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

4. Open `POST /auth/login` and log in with the same information.

5. Copy the returned `access_token`.

6. Click the **Authorize** button at the top of Swagger UI.

7. Paste the access token and click **Authorize**.

8. Test `GET /protected/profile` or `GET /protected/dashboard`.

A valid token returns status code `200`. An invalid token returns status code `401`.

---

## Testing Authentication with PowerShell

### Create a user

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/auth/signup" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"test@example.com","password":"password123"}'
```

### Log in

```powershell
$login = Invoke-RestMethod `
  -Uri "http://localhost:8000/auth/login" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"test@example.com","password":"password123"}'
```

### Save the access token

```powershell
$token = $login.access_token
```

### Access the protected profile

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/protected/profile" `
  -Headers @{Authorization = "Bearer $token"}
```

### Access the protected dashboard

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/protected/dashboard" `
  -Headers @{Authorization = "Bearer $token"}
```

### Test an invalid token

```powershell
Invoke-WebRequest `
  -Uri "http://localhost:8000/protected/profile" `
  -Headers @{Authorization = "Bearer invalid-token"}
```

This request should return status code `401 Unauthorized`.

### Log out

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/auth/logout" `
  -Method Post `
  -Headers @{Authorization = "Bearer $token"}
```

A successful logout returns status code `204 No Content`.

---

## Testing Task Endpoints with PowerShell

### Get all tasks

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/tasks" `
  -Method Get
```

### Create a task

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/tasks" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"title":"Complete authentication assignment","done":false}'
```

### Update a task

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/tasks/1" `
  -Method Put `
  -ContentType "application/json" `
  -Body '{"title":"Learn FastAPI and Supabase","done":true}'
```

### Delete a task

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/tasks/1" `
  -Method Delete
```

---

## HTTP Status Codes

| Status             | Meaning                                     | Used For                             |
| :----------------- | :------------------------------------------ | :----------------------------------- |
| `200 OK`           | The request succeeded                       | Login and reading information        |
| `201 Created`      | A resource was created                      | Signup and task creation             |
| `204 No Content`   | The request succeeded with no response body | Logout and task deletion             |
| `400 Bad Request`  | Required input is missing or invalid        | Empty email, password, or task title |
| `401 Unauthorized` | The user is not authenticated               | Missing, invalid, or expired token   |
| `404 Not Found`    | The requested resource does not exist       | Missing task                         |

`401 Unauthorized` means that the API cannot verify the user's identity.

`403 Forbidden` would mean that the API knows the user's identity, but the user does not have permission to perform an action.

---

## Security

* Passwords are managed and hashed by Supabase.
* The API never stores user passwords.
* Access tokens are verified through Supabase before protected routes run.
* Authentication logic is reused through a FastAPI dependency.
* The Supabase `service_role` key is not used.
* The real `.env` file is ignored by Git.
* `.env.example` contains placeholders instead of secrets.
* `.dockerignore` prevents `.env` from being copied into the Docker image.

---

## Screenshots and Visuals

### Manual Database Verification

<img width="584" height="373" alt="Manual SQL Exploration" src="https://github.com/user-attachments/assets/c62cfb2b-5933-4411-add3-92837a942649" />

### Interactive Swagger UI Documentation

<img width="1574" height="617" alt="Swagger UI" src="https://github.com/user-attachments/assets/25cd5ce3-912b-450f-a47c-1b9b3011ed83" />

### Docker Startup

<img width="1307" height="314" alt="Docker Startup" src="https://github.com/user-attachments/assets/84a669b2-a573-40c6-896d-efe6a8c1e35a" />

### Swagger Bearer Authentication




<img width="1277" height="865" alt="Screenshot 2026-09-05 044855" src="https://github.com/user-attachments/assets/5bf6c28f-d979-4f5e-9c68-04763d4b2caa" />



---

## Author

Created by Rasem Maraqa for the FlyRank Backend Internship Track.
