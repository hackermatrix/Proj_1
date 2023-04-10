from xsstrike.core import xsser

# Define the target URL
target_url = "http://example.com/search"

# Create an instance of the xsser class
scanner = xsser(target_url)

# Enable auto mode
scanner.auto()

# Start the scan
scanner.start()

# Print the results
if scanner.vulns:
    print("XSS vulnerabilities found:")
    for vuln in scanner.vulns:
        print("  - URL: {}".format(vuln.url))
        print("    Parameter: {}".format(vuln.param))
        print("    Vector: {}".format(vuln.vector))
else:
    print("No XSS vulnerabilities found.")
