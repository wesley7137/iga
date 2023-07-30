import os
import requests
from urllib.parse import urlparse

def download_arxiv_pdf(url):
    try:
        # Extract the arXiv identifier from the URL
        arxiv_id = url.split('/')[-1]

        # Construct the PDF download URL
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        # Send a GET request to download the PDF
        response = requests.get(pdf_url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the filename from the response headers
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
            else:
                # If filename cannot be obtained from the response headers, use the arXiv identifier as the filename
                filename = f"{arxiv_id}.pdf"

            # Save the PDF in the current working directory
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Downloaded '{filename}' successfully.")
        else:
            print(f"Failed to download. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace the example URL with the arXiv article link you want to download
    arxiv_article_url = "https://arxiv.org/abs/2101.00123"
    download_arxiv_pdf(arxiv_article_url)



