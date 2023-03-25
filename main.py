from fastapi import FastAPI
from datetime import datetime
from servers import servers
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

app = FastAPI()

# Konfigurasi pengaturan CORS
origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def check():
    # Menggunakan ThreadPoolExecutor untuk mengirim request ke banyak server secara bersamaan
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_server, server) for server in servers]
        results = [future.result() for future in as_completed(futures)]

    # Format waktu saat ini sesuai dengan format "YYYY-MM-DD HH:MM:SS"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Return JSON object dengan informasi hasil cek server
    return {"timestamp": timestamp, "server": servers, "connectivity": results}

def check_server(server):
    # Cek apakah alamat server valid
    if not server.startswith("http"):
        return {"status": False,"server": server,"message": "Bukan alamat http yang valid"}

    try:
        # Kirim request GET ke server dengan timeout 3 detik
        response = requests.get(server, timeout=3)
        # Jika response status code dalam range 200-299, server dianggap berhasil dihubungi
        if 200 <= response.status_code < 300:
            message = f"Terkoneksi dengan kode status {response.status_code}"
            status = True
        # Jika response status code tidak dalam range tersebut, server dianggap tidak berhasil dihubungi
        else:
            message = f"Tidak terkoneksi, kode error {response.status_code}"
            status = False
    except requests.exceptions.Timeout:
        message = "Tidak terkoneksi, waktu request habis"
        status = False
    except requests.exceptions.RequestException:
        message = "Tidak terkoneksi, request gagal"
        status = False

    # Return JSON object dengan informasi hasil cek server
    return {"status": status,"server": server.replace("https://", ""),"message": message}

@app.get("/single-check/{server_index}")
def check(server_index: int):
    # Cek apakah server_index berada dalam rentang indeks servers
    if server_index < 0 or server_index >= len(servers):
        return {"message": "Indeks server tidak valid"}

    server = servers[server_index]

    # Kirim request GET ke server yang ditentukan menggunakan fungsi check_server
    result = check_server(server)

    # Format waktu saat ini sesuai dengan format "YYYY-MM-DD HH:MM:SS"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Return JSON object dengan informasi hasil cek server
    return {"timestamp": timestamp, "server": server, "connectivity": result}
