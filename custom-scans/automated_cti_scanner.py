import os
import subprocess
from datetime import datetime
import sys

# Use absolute path to SpiderFoot
SPIDERFOOT_PATH = os.path.expanduser("~/spiderfoot/sf.py")

# Verify SpiderFoot installation
if not os.path.exists(SPIDERFOOT_PATH):
    print("❌ Error: SpiderFoot not found at", SPIDERFOOT_PATH)
    print("Please install SpiderFoot: git clone https://github.com/smicallef/spiderfoot.git")
    sys.exit(1)

# Verify modules directory
MODULES_DIR = os.path.join(os.path.dirname(SPIDERFOOT_PATH), "modules")
if not os.path.exists(MODULES_DIR):
    print("❌ Error: SpiderFoot modules directory not found at", MODULES_DIR)
    sys.exit(1)

targets = [
    "contagiodump.blogspot.com",
    "sellstuff.su",
    "darkjob.org",
    "mozi.malware.org.cn",
    "ayylmao.ninja",
    "btc-address.org",
    "ns1.nasa-gov.org",
    "apt28updates.com",
    "attackerserver.dynalias.com"
]

# Create absolute path for output directory
output_dir = os.path.abspath("reports")
os.makedirs(output_dir, exist_ok=True)

# Start with basic modules for testing
modules = "sfp__stor_db,sfp__stor_stdout,sfp_dns"  # Include required storage modules

print("\n🚀 Starting CTI scans...\n")
for target in targets:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = os.path.join(output_dir, f"{target}_{timestamp}.json")
        
        # Modified command structure with proper module dependencies
        command = [
            "python3",
            SPIDERFOOT_PATH,
            "-s", target,
            "-m", modules,
            "-o", "json",
            "-D", "spiderfoot.db"  # Add database file
        ]

        print(f"🔍 Scanning {target}...")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(SPIDERFOOT_PATH)  # Run from SpiderFoot directory
        )
        
        if result.returncode == 0:
            # Parse and save the JSON output
            with open(report_filename, 'w') as f:
                f.write(result.stdout)
            print(f"📝 Report generated for {target}: {report_filename}")
        else:
            print(f"❌ Error scanning {target}:")
            print(f"stderr: {result.stderr}")
            print(f"stdout: {result.stdout}")

    except Exception as e:
        print(f"❌ Error processing {target}: {str(e)}")

print("\n✅ All scans completed! Check your 'reports/' directory for the results.")