Welcome to YouTube Viral Video Assistant!
This assistant checks if your video will go viral on Youtube based on the title, description, country, and tag you add. It will give some advice to optimize your content. Test this and become the next Youtube star!

To get started, clone the repo to your local machine：
```bash
# Clone the repository
git clone https://github.com/asdzjh/Youtube-data-analysis.git

# Navigate to the project directory
cd Youtube-data-analysis
```
Then you need to have a openai API key to replace the your_api_key and your_base_url in main.py:
```bash
client = OpenAI(
    api_key= your_api_key,
    base_url= your_base_url
)
```

To build the project from scratch:
```bash
# Build all in Docker
docker-compose up --build

# Open the web page in your browser
http://localhost:8501/
```
Start to have fun!
