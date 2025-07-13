# 🧠 OpenAI FastAPI Microservice Deployment Guide (Local + EC2 with Docker)

This guide walks you through:
1. Creating a FastAPI microservice using OpenAI API
2. Running it locally (including Docker)
3. Deploying it to an EC2 instance
4. Cloning from GitHub
5. Building Docker image and running container
6. Testing with curl

---

## 1️⃣ Create & Run the FastAPI Project Locally

### A. Setup Project Structure
```bash
mkdir openai-ec2-fastapi-microservice
cd openai-ec2-fastapi-microservice
```

### B. `app.py`
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/query")
async def get_response(request: Request):
    try:
        data = await request.json()
        user_query = data.get("query")
        if not user_query:
            return JSONResponse(content={"error": "Query not provided"}, status_code=400)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_query}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
```

### C. `requirements.txt`
```
fastapi
uvicorn
openai
```

### D. `Dockerfile`
```dockerfile
# Use the official lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install dependencies using pip without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container's working directory
COPY . . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### E. Run Locally without Docker
```bash
export OPENAI_API_KEY="your_openai_key"
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### F. Run with Docker
```bash
docker build -t openai-fastapi-microservice .
docker run -d -p 8000:8000 \
-e OPENAI_API_KEY="your_real_openai_key" \
--name openai-service \
openai-fastapi-microservice
```

### G. Test with curl
```bash
curl -X POST http://localhost:8000/query \
-H "Content-Type: application/json" \
-d '{"query": "Tell me a joke about clouds"}'
```

---

## 2️⃣ Create an EC2 Instance

1. Go to AWS Console ➝ EC2 ➝ Launch Instance
2. AMI: **Amazon Linux 2023**
3. Instance type: `t2.micro` (Free Tier)
4. Key pair: Create or select existing (e.g., `my-ec2-key.pem`)
5. Configure security group:
   - Allow inbound: TCP 22 (SSH), TCP 8000 (App)

---

## 3️⃣ Connect to EC2 Instance from Local System

```bash
chmod 400 my-ec2-key.pem
ssh -i my-ec2-key.pem ec2-user@<your-ec2-public-ip>
```

---

## 4️⃣ Clone GitHub Repo & Install Docker

### A. Install Docker on EC2 (Amazon Linux 2023)
```bash
sudo dnf update -y
sudo dnf install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
exit
```
Then reconnect via SSH.

### B. Clone Repo
```bash
git clone https://github.com/mrsujeet/openai-ec2-fastapi-microservice.git
cd openai-ec2-fastapi-microservice
```

---

## 5️⃣ Build Docker Image & Run Container on EC2

### A. Build image:
```bash
docker build -t openai-fastapi-microservice .
```

### B. Run container:
```bash
docker run -d -p 8000:8000 \
-e OPENAI_API_KEY="your_real_openai_key" \
--name openai-service \
openai-fastapi-microservice
```

---

## 6️⃣ Test with curl from Local Machine

```bash
curl -X POST http://<ec2-public-ip>:8000/query \
-H "Content-Type: application/json" \
-d '{"query": "Tell me a joke about clouds"}'
```

✅ You should receive a JSON response with GPT-generated content.

---

## ✅ Next Steps (Optional)
- Add Nginx + SSL
- Set up Docker Compose or ECS
- Use GitHub Actions for CI/CD

Let me know if you’d like help automating or securing any part of this!
# openai-ec2-fastapi-microservice
openai-ec2-fastapi-microservice
