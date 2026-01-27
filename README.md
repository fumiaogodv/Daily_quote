docker-compose.yml
```
version: "3.9"

services:
  quotes:
    image: 0424godv/quotes_prod:latest 
    container_name: quotes_app
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```
