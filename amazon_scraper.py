import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Initialize WebDriver
driver_path =  r'C:\Users\Admin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

def get_amazon_reviews(product_url, max_reviews=500):
    reviews_data = []
    driver.get(product_url)

    # Scroll down to load the reviews section and click "See All Reviews"
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]').click()
    time.sleep(2)
    
    # Loop through pages to collect reviews
    while len(reviews_data) < max_reviews:
        # Find all review elements on the page
        review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-hook="review"]')
        
        # Extract details for each review
        for review_element in review_elements:
            # Review text
            try:
                review_text = review_element.find_element(By.CSS_SELECTOR, 'span[data-hook="review-body"]').text
            except:
                review_text = None
            
            # Review date
            try:
                review_date = review_element.find_element(By.CSS_SELECTOR, 'span[data-hook="review-date"]').text
            except:
                review_date = None
            
            # Username
            try:
                username = review_element.find_element(By.CSS_SELECTOR, 'span.a-profile-name').text
            except:
                username = None
            
            # Rating
            try:
                rating_element = review_element.find_element(By.CSS_SELECTOR, 'i[data-hook="review-star-rating"]')
                rating = rating_element.get_attribute("textContent").split(" ")[0]  # Extract the numeric rating
            except:
                rating = None
            
            # Add review data to the list
            reviews_data.append({
                "Review": review_text,
                "Date": review_date,
                "Username": username,
                "Rating": rating
            })
            
            # Stop if we've reached the target number of reviews
            if len(reviews_data) >= max_reviews:
                break

        # Try to click the "Next" button to go to the next page
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.a-last a')
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  # Wait for the next page to load
        except:
            print("No more pages left or could not find the next button.")
            break

    return reviews_data[:max_reviews]

# Example Usage
product_url = 'https://www.amazon.in/Apple-iPhone-13-128GB-Midnight/product-reviews/B09G9HD6PD/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1'  # Replace with the product's Amazon URL
reviews_data = get_amazon_reviews(product_url, max_reviews=500)

# Save to CSV
df = pd.DataFrame(reviews_data)
df.to_csv("amazon_reviews.csv", index=False)
print("Saved reviews to amazon_reviews.csv")

# Close the browser
driver.quit()