import requests
import time

# Replace with your actual API URL
API_URL = "https://duongnt1204--sd15-text2img-api-fastapi-app.modal.run"

def test_health():
    """Test if API is running"""
    print("Testing API health...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def generate_image(prompt, filename="test_image.png"):
    """Generate a single image"""
    print(f"Generating: '{prompt}'")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/generate",
            json={"prompt": prompt},
            timeout=120
        )
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Saved as {filename} ({duration:.1f}s)")
            return True
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"Failed: {e}")
        return False

def main():
    print("Starting SD1.5 API Test\n")
    
    # Test 1: Health check
    if not test_health():
        print("API is not responding. Exiting.")
        return
    
    print("\n" + "="*40)
    
    # Test 2: Simple generation
    generate_image("a beautiful sunset", "sunset.png")
    
    # Test 3: More complex prompt
    generate_image("a cute cat wearing sunglasses", "cool_cat.png")
    
    # Test 4: Landscape
    generate_image("mountains and lake reflection", "landscape.png")
    
    print("\nTest completed!")

if __name__ == "__main__":
    main()