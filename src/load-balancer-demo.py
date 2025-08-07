import socket
import platform
import os
import subprocess
import psutil # You'll need to install this: pip install psutil
from flask import Flask, render_template_string, request # Import request

app = Flask(__name__)

# HTML template for the server information page
# Using Tailwind CSS for a modern and responsive look
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" href="data:,">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Status - {{ hostname }}</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #fff 0%, #EEF2FF 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body class="p-4">
    <div class="bg-white shadow-xl rounded-xl p-8 md:p-12 max-w-3xl w-full text-center border-t-4 border-green-500">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-6 flex items-center justify-center">
            <img src="https://openscaler.net/logo.svg" alt="OpenScaler Logo" class="w-12 h-12 mr-3">
            Load Balancer Example
        </h1>
        <p class="text-gray-600 mb-8 text-lg">You've reached <span class="font-bold text-green-700">{{ hostname }}</span>!</p>

        $$$$$$$$$$$$$$$HEADER$$$$$$
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
            <div class="bg-gray-50 p-6 rounded-lg shadow-inner">
                <h2 class="text-xl font-semibold text-gray-800 mb-3 flex items-center">
                    <svg class="w-6 h-6 text-gray-600 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <rect x="2" y="2" width="16" height="16" rx="3" ry="3"/>
                    </svg>
                    Network Details
                </h2>
                <ul class="text-gray-700 space-y-2">
                    <li><strong>Hostname:</strong> <span class="font-medium text-gray-600">{{ hostname }}</span></li>
                    <li><strong>IP Address:</strong> <span class="font-medium text-gray-600">{{ ip_address }}</span></li>
                    <li><strong>ID:</strong> <span class="font-medium text-gray-600 break-all">{{ machine_id }}</span></li>
                </ul>
            </div>

            <div class="bg-lime-50 p-6 rounded-lg shadow-inner">
                <h2 class="text-xl font-semibold text-lime-800 mb-3 flex items-center">
                    <svg class="w-6 h-6 text-lime-600 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <rect x="2" y="2" width="16" height="16" rx="3" ry="3"/>
                    </svg>
                    System Information
                </h2>
                <ul class="text-gray-700 space-y-2">
                    <li><strong>Operating System:</strong> <span class="font-medium text-lime-600">{{ os_name }} {{ os_release }}</span></li>
                    <li><strong>Linux Distribution:</strong> <span class="font-medium text-lime-600">{{ linux_distro }}</span></li>
                    <li><strong>RAM Capacity:</strong> <span class="font-medium text-lime-600">{{ ram_capacity }}</span></li>
                    <li><strong>Disk Size:</strong> <span class="font-medium text-lime-600">{{ disk_size }}</span></li>
                    <li><strong>CPU Cores:</strong> <span class="font-medium text-lime-600">{{ cpu_cores }}</span></li>
                </ul>
            </div>
        </div>

        <div class="mt-6"> <!-- Added margin-top for spacing -->
            <div class="bg-orange-50 p-6 rounded-lg shadow-inner text-left">
                <h2 class="text-xl font-semibold text-orange-800 mb-3 flex items-center">
                    <svg class="w-6 h-6 text-orange-600 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <rect x="2" y="2" width="16" height="16" rx="3" ry="3"/>
                    </svg>
                    Client Information
                </h2>
                <ul class="text-gray-700 space-y-2">
                    <li><strong>Client IP (X-Forwarded-For):</strong> <span class="font-medium text-orange-600">{{ x_forwarded_for_ip }}</span></li>
                    <li><strong>Forwarded Header (for):</strong> <span class="font-medium text-orange-600">{{ forwarded_for_ip }}</span></li>
                    <li><strong>Forwarded Header (host):</strong> <span class="font-medium text-orange-600">{{ forwarded_host }}</span></li>
                </ul>
            </div>
        </div>

        <div class="mt-8 text-gray-500 text-sm">
            <p>This page is dynamically generated to help you test your load balancer configuration.</p>
            <p>OpenScaler Cloud Computing</p>
        </div>
    </div>
</body>
</html>
"""

def get_linux_distro():
    """
    Attempts to get Linux distribution information.
    Prioritizes platform.freedesktop_os_release() for modern systems,
    falls back to lsb_release or a generic "Linux".
    """
    try:
        # For modern Linux systems using systemd
        os_release = platform.freedesktop_os_release()
        if os_release:
            name = os_release.get('PRETTY_NAME') or os_release.get('NAME')
            version = os_release.get('VERSION')
            if name and version:
                return f"{name} {version}"
            elif name:
                return name
    except AttributeError:
        pass # freedesktop_os_release not available

    # Fallback for older systems or if freedesktop_os_release fails
    try:
        # Try lsb_release command
        result = subprocess.run(['lsb_release', '-d', '-s'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return "Linux (Unknown Distribution)"

def get_machine_id():
    """
    Reads the machine ID (UUID) from /etc/machine-id.
    """
    try:
        with open('/etc/machine-id', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "N/A (File /etc/machine-id not found)"
    except Exception as e:
        return f"Error reading machine ID: {e}"

def render_details(path = ""):
    """
    Gathers server information and renders it in an HTML template,
    including various client IP addresses and potentially port information
    from request headers.
    """
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        os_name = platform.system()
        os_release = platform.release()
        cpu_cores = os.cpu_count()

        # Get Linux distribution info
        linux_distro = get_linux_distro()

        # Get RAM capacity using psutil
        ram = psutil.virtual_memory()
        ram_capacity = f"{ram.total / (1024**3):.2f} GB" # Convert bytes to GB

        # Get disk size (total for root partition) using psutil
        # Assuming '/' is the root partition
        disk = psutil.disk_usage('/')
        disk_size = f"{disk.total / (1024**3):.2f} GB" # Convert bytes to GB

        # Get machine ID (UUID)
        machine_id = get_machine_id()

        # Get sender's IP address (direct connection to this server)
        direct_ip = request.remote_addr if request.remote_addr else "N/A"

        # Get X-Forwarded-For header
        x_forwarded_for_ip = "N/A"
        x_forwarded_for_header = request.headers.get('X-Forwarded-For')
        if x_forwarded_for_header:
            # X-Forwarded-For can contain multiple IPs if there are multiple proxies
            # The first IP is usually the original client IP
            x_forwarded_for_ip = x_forwarded_for_header.split(',')[0].strip()

        # Get Forwarded header
        forwarded_for_ip = "N/A"
        forwarded_host = "N/A"
        forwarded_header = request.headers.get('Forwarded')
        if forwarded_header:
            # Parse the Forwarded header (e.g., "for=192.0.2.60;proto=http;by=203.0.113.43;host=example.com:8080")
            parts = forwarded_header.split(';')
            for part in parts:
                part = part.strip()
                if part.startswith('for='):
                    forwarded_for_ip = part.split('=', 1)[1].strip()
                elif part.startswith('host='):
                    forwarded_host = part.split('=', 1)[1].strip()
        if path:
            template = HTML_TEMPLATE.replace('$$$$$$$$$$$$$$$HEADER$$$$$$', f"""
            <div class="bg-green-50 p-6 rounded-lg shadow-inner text-left mb-4">
                <h2 class="text-xl font-semibold text-green-800 mb-3 flex items-center">
                    <svg class="w-6 h-6 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <rect x="2" y="2" width="16" height="16" rx="3" ry="3"/>
                    </svg>
                    Path and parameters
                </h2>
                <ul class="text-gray-700 space-y-2">
                    <li><strong>Path:</strong> <span class="font-medium text-green-600">{ path }</span></li>
                    <li><strong>Arguments:</strong> <span class="font-medium text-green-600">{ dict(request.args) }</span></li>
                </ul>
            </div>""")
        else:
            template = HTML_TEMPLATE.replace('$$$$$$$$$$$$$$$HEADER$$$$$$', "")
        return render_template_string(
            template,
            hostname=hostname,
            ip_address=ip_address,
            os_name=os_name,
            os_release=os_release,
            linux_distro=linux_distro,
            ram_capacity=ram_capacity,
            disk_size=disk_size,
            cpu_cores=cpu_cores if cpu_cores else "N/A",
            machine_id=machine_id,
            direct_ip=direct_ip,
            x_forwarded_for_ip=x_forwarded_for_ip,
            forwarded_for_ip=forwarded_for_ip,
            forwarded_host=forwarded_host,
        )
    except Exception as e:
        # Basic error handling
        return f"<h1 style='color: orange;'>Error: Could not retrieve server information.</h1><p>{e}</p>"

# -------------------------------------------------------------------------------------------------
#   Use this to check server health in your load balancer
# -------------------------------------------------------------------------------------------------
@app.route('/health')
def health():
    return "OK"

@app.route('/health_slow')
def health_slow():
    from time import sleep
    sleep(2)
    return "OK"

@app.route('/')
def root():
    return render_details()

@app.route('/<path:path>')
def other(path):
    return render_details(path)

if __name__ == '__main__':
    # Run the Flask app on all available interfaces (0.0.0.0) and port 8080
    # In a production environment, you would typically use a WSGI server like Gunicorn
    print("Starting Flask app...")
    print("Access the server info at http://0.0.0.0:8080/")
    app.run(host='0.0.0.0', port=8080)
