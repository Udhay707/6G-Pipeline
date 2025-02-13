import requests
import time
from io import BytesIO
from requests.adapters import HTTPAdapter


class SourceAddressAdapter(HTTPAdapter):
    """
    Custom HTTPAdapter to bind requests to a specific source address (IP).
    """

    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_address, 0)
        return super().init_poolmanager(*args, **kwargs)


def fetch_webcam_frame(session, webcam_server_url):
    """
    Fetches the latest webcam frame from the webcam FastAPI server.

    Args:
        session (requests.Session): Requests session with custom adapter.
        webcam_server_url (str): URL of the webcam server.
    
    Returns:
        bytes: The JPEG image bytes of the frame.
    """
    response = session.get(webcam_server_url, stream=True)
    response.raise_for_status()
    return response.content


def send_image_to_server(session, image_bytes, fastapi_server_url):
    """
    Sends an image to the FastAPI image-processing server.

    Args:
        session (requests.Session): Requests session with custom adapter.
        image_bytes (bytes): The JPEG image bytes to send.
        fastapi_server_url (str): URL of the image-processing FastAPI server.
    
    Returns:
        dict: JSON response from the server.
    """
    files = {'image': ("frame.jpg", BytesIO(image_bytes), "image/jpeg")}
    # save the image to a file for debugging
    response = session.post(fastapi_server_url, files=files)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    FASTAPI_SERVER_URL = "http://192.168.76.160:8000/infer"  # Replace with actual server address

    # Source IP to bind the requests
    SOURCE_IP = "12.1.1.3"  # Replace with the desired source IP

    # Create a session with the custom adapter to bind requests to the specific IP
    session = requests.Session()
    session.mount('http://', SourceAddressAdapter(SOURCE_IP))
    session.mount('https://', SourceAddressAdapter(SOURCE_IP))

    try:
        while True:
            try:
                    # Load and send an image
                image_file_path = 'dog.jpg'  # Replace with the path to your image
                with open(image_file_path, 'rb') as image_file:
                    image_data = image_file.read()

                # Send the frame to the FastAPI server
                print("Sending frame to the FastAPI server...")
                result = send_image_to_server(session, image_data, FASTAPI_SERVER_URL)

                # Print the result
                print("Server Response:", result)

            except Exception as e:
                print(f"An error occurred: {e}")

            # Wait for 1 second before the next frame
            time.sleep(1)

    except KeyboardInterrupt:
        print("Streaming stopped.")