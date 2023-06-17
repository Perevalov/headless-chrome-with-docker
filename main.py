from fastapi import FastAPI, HTTPException
import undetected_chromedriver.v2 as uc
import os
import uvicorn
import logging
import gc


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'

app = FastAPI()


@app.get("/route")
async def route():
    try:
        options = uc.ChromeOptions()
        
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--user-agent={user_agent}')
        options.user_data_dir = "./chrome"
        options.add_argument('--user-data-dir=./chrome')

        driver = uc.Chrome(options=options, version_main=os.getenv('CHROME_VERSION') or 100)
        driver.get("https://your-url.com")

        # find element and click
        #driver.find_element("class name", "button_type_submit").click()
        
        
        # navigate between tabs:
        # driver.switch_to.window(driver.window_handles[1])

        # get current url:
        # url = driver.current_url

        driver.close()
        driver.quit()
        gc.collect()
        
        return {"status": True}

    except Exception as e:
        logger.error("Exception: " + str(e))

    return HTTPException(status_code=500, detail="Error")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

