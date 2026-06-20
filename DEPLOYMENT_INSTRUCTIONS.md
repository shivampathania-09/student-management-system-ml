# Deployment Instructions

This guide provides step-by-step instructions to deploy the **Student Management System** to various platforms.

## 1. Streamlit Community Cloud (Easiest)
Streamlit Community Cloud is the best platform for free, continuous deployment directly from your GitHub repository.

**Prerequisites:**
- Push this entire project folder to a public or private GitHub repository.
- Ensure `requirements.txt` is in the root directory.

**Steps:**
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
2. Click **New app**.
3. Select your repository, branch (usually `main`), and the main file path: `app.py`.
4. Click **Deploy!**
5. Streamlit will automatically read `requirements.txt`, install dependencies, and launch your app. The `.streamlit/config.toml` file will automatically configure the theme and port.

## 2. Docker Deployment (Local or VPS)
If you want to host the app on a Virtual Private Server (e.g., AWS EC2, DigitalOcean) or run it locally in an isolated environment.

**Prerequisites:**
- Docker and Docker Compose installed on the host machine.

**Steps:**
1. Navigate to the project directory on your server.
2. Build and start the container in detached mode:
   ```bash
   docker-compose up -d --build
   ```
3. The application will be exposed on port `8501`. Access it via `http://<server-ip>:8501`.
4. *Note:* The `docker-compose.yml` is configured to mount `students.db` to the host, ensuring your student records persist even if the container is restarted.

## 3. Heroku Deployment
**Prerequisites:**
- Heroku CLI installed.
- A `Procfile` and `setup.sh` (if you aren't using the container stack).

**Using Docker on Heroku:**
1. Log in to Heroku Container Registry:
   ```bash
   heroku container:login
   ```
2. Create a new Heroku app:
   ```bash
   heroku create student-management-sys
   ```
3. Push the Docker image:
   ```bash
   heroku container:push web -a student-management-sys
   ```
4. Release the image:
   ```bash
   heroku container:release web -a student-management-sys
   ```

## Verifying Dependencies
Before deploying to any platform, ensure your local environment runs cleanly:
```bash
pip install -r requirements.txt
pip check
pytest tests/
```
