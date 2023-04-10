import subprocess

# Set the target URL
target_url = 'http://10.10.114.63/vulnerabilities/fi/?page=file1.php'

# Set the path to the Nikto executable
# nikto_path = '/path/to/nikto'

# Set the Nikto options
nikto_options = [
    '-host', target_url,
    '-Plugin', 'lfi',
    '-Tuning', '123456',
    '-Format', 'txt',
]

# Run the Nikto command and capture its output
result = subprocess.Popen(['nikto'] + nikto_options, stdout=subprocess.PIPE, bufsize=1)

# Print the output
for line in iter(result.stdout.readline, b''):
    print(line.decode('utf-8'), end='')
