# Read AIOB file from Android devices.
# https://play.google.com/store/apps/details?id=com.loopvector.allinonebackup.smsbackup&hl=en&gl=US
# You do need to charge for this app. Export AIOB file and read it here first.
# The AIOB file is a XML file in fact.


import xml.etree.ElementTree as ET

def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def parse_aiob_file(file_content):
    try:
        root = ET.fromstring(file_content)

        # 提取Type
        backup_type = root.find('Type').text
        print(f"Backup Type: {backup_type}")

        # 提取每个Datum的信息
        for datum in root.findall('.//Datum'):
            datum_id = datum.find('ID').text
            body = datum.find('BODY').text
            sent_date = datum.find('SENT_DATE').text
            received_date = datum.find('RECEIVED_DATE').text
            address = datum.find('ADDRESS').text
            
            #print(f"\nDatum ID: {datum_id}")
            print(f"Body: {body}")
            print(f"Sent Date: {sent_date}")
            print(f"Received Date: {received_date}")
            print(f"from: {address}")
            print("\n")
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")

# 用法示例
#file_path = 'path/to/your/file.aiob'
file_path="aiob/SMS-1708912680479.aiob"
file_content = read_binary_file(file_path)

if file_content:
    parse_aiob_file(file_content)

