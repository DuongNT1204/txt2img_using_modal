# Stable Diffusion 1.5 API on Modal

Deploy Stable Diffusion 1.5 như một FastAPI service trên Modal để tạo ảnh từ text.

## Quick Start

### 1. Cài đặt & Đăng nhập
```bash
pip install modal
modal auth new
```

### 2. Deploy
```bash
modal deploy main.py
```

### 3. Test
```bash
# Health check
curl https://your-username--sd15-text2img-api-fastapi-app.modal.run/

# Generate image
curl -X POST "https://your-username--sd15-text2img-api-fastapi-app.modal.run/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset"}' \
  --output image.png
```

## API Usage

**Endpoint:** `POST /generate`

**Basic:**
```json
{"prompt": "a cute cat"}
```

**Advanced:**
```json
{
  "prompt": "cyberpunk city at night",
  "negative_prompt": "blurry, low quality",
  "num_inference_steps": 25,
  "guidance_scale": 7.5,
  "width": 512,
  "height": 512,
  "seed": 42
}
```

## Python Example
```python
import requests

response = requests.post("https://your-api-url/generate", json={
    "prompt": "a beautiful landscape",
    "seed": 42
})

with open("image.png", "wb") as f:
    f.write(response.content)
```

## Troubleshooting
```bash
# Re-auth
modal auth login

# Check logs
modal logs sd15-text2img-api

# Update Modal
pip install --upgrade modal
```
