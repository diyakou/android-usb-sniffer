import subprocess
import json

def run_adb_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=False)
        result.check_returncode()
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode('utf-8'))
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_gallery_data():
    try:
        gallery_command = "adb shell ls /sdcard/DCIM"
        gallery_result = run_adb_command(gallery_command)

        if gallery_result is None:
            return None

        calls_command = "adb shell dumpsys calllog"
        calls_result = run_adb_command(calls_command)
        calls_data = json.loads(calls_result) if calls_result else None

        if calls_result is None:
            return None

        sms_command = "adb shell content query --uri content://sms --projection _id,address,date,body"
        sms_result = run_adb_command(sms_command)
        
        if sms_result is None:
            return None

        file_list = gallery_result.splitlines()

        print("Gallery Data:")
        for file_name in file_list:
            print(file_name)

        print("\nRecent Calls:")
        print(json.dumps(calls_data, indent=2))

        print("\nRecent SMS:")
        print(sms_result)

        return file_list, calls_data, sms_result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

result = get_gallery_data()

if result is not None:
    gallery_data, calls_data, sms_data = result
else:
    print("Failed to retrieve data from the device.")
