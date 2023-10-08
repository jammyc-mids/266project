import re,json
import requests
from bs4 import BeautifulSoup
import pdb


headers = {'Content-Type' : 'application/json'}

bug_status_list = ['ASSIGNED', 'REOPENED', 'RESOLVED', 'REOPENED', 'VERIFIED', 'DEFERRED', 'CLOSED']
product_list = ["ACPI", "Backports project", "Documentation", "Drivers", "EFI", "File System", "IO/Storage", "Memory Management",
"Networking", "Platform Specific/Hardware", "Power Management", "Process Management", "Product", "SCSI Drivers", "Timers",
"Tools", "Tracing/Profiling", "Virtualization"]

def extractValue(token_str):
    mat = re.search(r'\>([^<]+)\s*\<', token_str.decode())
    if mat:
        value = mat.group(1).replace('\n', '')
        value = value.rstrip('( ')
        return value
    return ""

def generateData(blist):
    words = []
    for bl in blist:
        url = "https://bugzilla.kernel.org/show_bug.cgi?id=" + bl
        print(f"Extracting bugs data for {bl}...")
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            wdata = BeautifulSoup(resp.content, "html.parser")
            topic = extractValue(wdata.find(class_="subheader", id="subtitle"))
            product = extractValue(wdata.find(id="field_container_product"))
            component = extractValue(wdata.find(id="field_container_component"))
            comment = ""
            for c in wdata.find_all(class_="bz_comment_text"):
                comment += extractValue(c)
            words.append({'topic' : topic, 'product' : product, 'component' : component, 'comments' : comment})
    return words

with open("../data/bugs_list.txt") as f:
    bids = f.read().splitlines()
    f.close()
    words = generateData(bids)
    
with open("bugs_data.json", "w+") as f:
    f.write(json.dumps(words, indent=4))
    f.close()
