# main.py
import modal
import torch
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from diffusers import StableDiffusionPipeline
import io
from PIL import Image
import logging

app = modal.App("sd15-text2img-api")

image = modal.Image.debian_slim().pip_install(
    "torch==2.0.1",
    "torchvision==0.15.2",
    "diffusers[torch]==0.21.4",
    "transformers==4.34.0",
    "accelerate==0.23.0",
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "pillow==10.0.1",
    "numpy==1.24.3"
)

@app.cls(
    image=image,
    gpu="A10G",
    timeout=600,
    scaledown_window=300
)
@modal.concurrent(max_inputs=10)
class StableDiffusionModel:
        
    @modal.enter()
    def load_model(self):
        print("Loading Stable Diffusion 1.5 model...")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            revision="fp16",
            use_auth_token="your_huggingface_token_here",  
            safety_checker=None,
            requires_safety_checker=False
        ).to("cuda")
        
        self.pipe.enable_attention_slicing()
        self.pipe.enable_model_cpu_offload()
        print("Model loaded successfully!")
    
    @modal.method()
    def generate_image(self, prompt: str, negative_prompt: str = "", 
                      num_inference_steps: int = 20, guidance_scale: float = 7.5,
                      width: int = 512, height: int = 512, seed: int = None):
        try:
            if seed is not None:
                torch.manual_seed(seed)
            
            with torch.autocast("cuda"):
                result = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height
                )
            
            image = result.images[0]
            
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise e

model = StableDiffusionModel()

@app.function(image=image, timeout=600)
@modal.asgi_app()
def fastapi_app():
    app = FastAPI(
        title="Stable Diffusion 1.5 API",
        description="API để generate images với Stable Diffusion 1.5",
        version="1.0.0"
    )
    
    @app.get("/")
    def root():
        return {
            "message": "SD1.5 API is running",
            "status": "healthy",
            "model": "runwayml/stable-diffusion-v1-5"
        }
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    @app.post("/generate")
    async def generate_image(request: Request):
        try:
            data = await request.json()
            
            prompt = data.get("prompt")
            if not prompt:
                raise HTTPException(status_code=400, detail="Prompt is required")
            
            negative_prompt = data.get("negative_prompt", "")
            num_inference_steps = data.get("num_inference_steps", 20)
            guidance_scale = data.get("guidance_scale", 7.5)
            width = data.get("width", 512)
            height = data.get("height", 512)
            seed = data.get("seed", None)
            
            if not (10 <= num_inference_steps <= 50):
                raise HTTPException(status_code=400, detail="num_inference_steps must be between 10 and 50")
            
            if not (1.0 <= guidance_scale <= 20.0):
                raise HTTPException(status_code=400, detail="guidance_scale must be between 1.0 and 20.0")
            
            if width not in [512, 768, 1024] or height not in [512, 768, 1024]:
                raise HTTPException(status_code=400, detail="width and height must be 512, 768, or 1024")
            
            print(f"Generating image with prompt: {prompt}")
            image_bytes = model.generate_image.remote(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                seed=seed
            )
            
            return StreamingResponse(
                io.BytesIO(image_bytes),
                media_type="image/png",
                headers={
                    "Content-Disposition": "inline; filename=generated_image.png"
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error in generate endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    return app

