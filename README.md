# Connectivity Monitor
This code creates an HTTP server using the FastAPI framework. It has two endpoints - one checks the connectivity of multiple servers concurrently, and the other checks the connectivity of a single server. It uses the check_server function to check the connectivity of each server by sending a GET request to the server's address. The code also includes configuration settings for the Cross-Origin Resource Sharing (CORS) middleware to allow cross-origin requests.

# Endpoint explanation
The server provides two endpoints:
1. The root endpoint ("/") performs a connectivity check on a list of servers specified in the servers variable. It uses the check_server function to check the connectivity of each server by sending a GET request to the server's address. The function uses the ThreadPoolExecutor class to send the requests concurrently, and returns a JSON object containing the status of each server.
2. The "/single-check/{server_index}" endpoint performs a connectivity check on a single server specified by the server_index parameter. It uses the check_server function to check the connectivity of the server by sending a GET request to the server's address. The function returns a JSON object containing the status of the server.
