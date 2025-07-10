\# Stable Diffusion 1.5 API on Modal



Deploy Stable Diffusion 1.5 như một FastAPI service trên Modal để tạo ảnh từ text.



\## 🚀 Quick Start



\### 1. Cài đặt \& Đăng nhập

```bash

pip install modal

modal auth new

```



\### 2. Deploy

```bash

modal deploy main.py

```



\### 3. Test

```bash

\# Health check

curl https://your-username--sd15-text2img-api-fastapi-app.modal.run/



\# Generate image

curl -X POST "https://your-username--sd15-text2img-api-fastapi-app.modal.run/generate" \\

&nbsp; -H "Content-Type: application/json" \\

&nbsp; -d '{"prompt": "a beautiful sunset"}' \\

&nbsp; --output image.png

```



\## 📖 API Usage



\*\*Endpoint:\*\* `POST /generate`



\*\*Basic:\*\*

```json

{"prompt": "a cute cat"}

```



\*\*Advanced:\*\*

```json

{

&nbsp; "prompt": "cyberpunk city at night",

&nbsp; "negative\_prompt": "blurry, low quality",

&nbsp; "num\_inference\_steps": 25,

&nbsp; "guidance\_scale": 7.5,

&nbsp; "width": 512,

&nbsp; "height": 512,

&nbsp; "seed": 42

}

```



\## 🐍 Python Example

```python

import requests



response = requests.post("https://your-api-url/generate", json={

&nbsp;   "prompt": "a beautiful landscape",

&nbsp;   "seed": 42

})



with open("image.png", "wb") as f:

&nbsp;   f.write(response.content)

```





\## 🔧 Troubleshooting

```bash

\# Re-auth

modal auth login



\# Check logs

modal logs sd15-text2img-api



\# Update Modal

pip install --upgrade modal

```

