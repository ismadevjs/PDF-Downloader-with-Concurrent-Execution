import os
import requests
from concurrent.futures import ThreadPoolExecutor

def download_pdf(number, save_path):
    pdf_url = f"https://localhost/public/{number}/mob"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/pdf',
    }

    try:
        response = requests.get(pdf_url, headers=headers)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"PDF for number {number} downloaded successfully and saved at: {save_path}")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

def download_pdfs_concurrently(start_number, end_number, save_directory, batch_size, max_threads):
    with ThreadPoolExecutor(max_threads) as executor:
        for batch_start in range(start_number, end_number + 1, batch_size):
            batch_end = min(batch_start + batch_size - 1, end_number)
            folder_name = f"{batch_start:02d}-{batch_end:02d}"
            folder_path = os.path.join(save_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            futures = []
            for number in range(batch_start, batch_end + 1):
                save_path = os.path.join(folder_path, f"pdf_{number}.pdf")
                future = executor.submit(download_pdf, str(number), save_path)
                futures.append(future)

            # nessnaw futures bach ykamlo
            for future in futures:
                future.result()

# Example usage:
           
start_number = 30002020230000001
end_number = 30002020230030001
save_directory = "output1"
batch_size = 3000
max_threads = 5

download_pdfs_concurrently(start_number, end_number, save_directory, batch_size, max_threads)
