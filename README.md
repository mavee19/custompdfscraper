# **custompdfscraper**
Customized PDF scraper for www.artesyn.com/documents. This code needs further refactoring.

# >**Using Selenium**
Download Chromedriver.exe based on your Chrome Browser version. https://chromedriver.chromium.org/

# >**Scraping the PDF**
```python
 # Find all the <a> tags with 'onclick' attribute containing 'download'
    links = driver.find_elements(By.XPATH, '//a[contains(@onclick, "download")]')
    links_url = [link.get_attribute('href') for link in links]
    # print(links_url)
    for link in links_url:
        pdf_link = link
        # print(pdf_link)
        # Navigate to the PDF link and find the embedded PDF object
        driver.get(pdf_link)
        driver.implicitly_wait(10)
        embedded_pdf = driver.find_element(By.XPATH, '//object[contains(@data, ".pdf")]')
        # Extract the source URL of the embedded PDF
        embedded_pdf_url = embedded_pdf.get_attribute('data')
        # Extract the filename from the URL and sanitize it
        parsed_url = urllib.parse.urlparse(embedded_pdf_url)
        filename = os.path.basename(parsed_url.path)
        print(filename)
```
With Basic HTML knowledge,you can inspect the website you are scraping and identify the XPATH or CSS Selector where the PDF resides.
Since the target website in this code contains more links, the above code snippet is responsible for finding all the element(links) of the PDF. 
Once all the links are collected, another find element is called to determine the download link of the individual PDF.
