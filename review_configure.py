import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize WebDriver
driver_path = config["driver_path"]
driver = webdriver.Chrome(service=Service(driver_path))

def get_amazon_reviews(product_url, item_name, review_count):
    reviews_data = []
    driver.get(product_url)

    # Wait and click "See All Reviews"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]'))).click()
    time.sleep(2)
    
    # Loop to collect reviews
    while len(reviews_data) < review_count:
        review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-hook="review"]')
        
        # Extract review details
        for review_element in review_elements:
            review_text = review_element.find_element(By.CSS_SELECTOR, 'span[data-hook="review-body"]').text if review_element else None
            review_date = review_element.find_element(By.CSS_SELECTOR, 'span[data-hook="review-date"]').text if review_element else None
            username = review_element.find_element(By.CSS_SELECTOR, 'span.a-profile-name').text if review_element else None
            rating = review_element.find_element(By.CSS_SELECTOR, 'i[data-hook="review-star-rating"]').get_attribute("textContent").split(" ")[0] if review_element else None
            
            # Add to list
            reviews_data.append({
                "Review": review_text,
                "Date": review_date,
                "Username": username,
                "Rating": rating
            })
            
            if len(reviews_data) >= review_count:
                break

        # Click "Next" if more reviews are needed
        try:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.a-last a')))
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)
        except:
            print("No more pages left or could not find the next button.")
            break

    # Save reviews to a CSV with the item name
    output_file = f"Iphone_amazon_reviews.csv"
    df = pd.DataFrame(reviews_data[:review_count])
    df.to_csv(output_file, index=False)
    print(f"Saved reviews to Iphone_amazon_reviews")

    return reviews_data[:review_count]

# Usage with config.json values
product_url = config["product_url"]
item_name = config["item_name"]
review_count = config["review_count"]

reviews_data = get_amazon_reviews(product_url, item_name=item_name, review_count=review_count)

# Close the browser
driver.quit()
