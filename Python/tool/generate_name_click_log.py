import json

# DIR = "../../data/"
# DIR2 = "../../data2/"
# # Path to the input CSV-like file
# input_file_path = DIR + "log/simulated_click_log.txt"

# # Path to the output JSON file
# output_file_path = DIR2 + "log/simulated_click_log.txt"

DIR = "../../data/"
DIR2 = "../../data2/"

# input_file_path = DIR + "log/simulated_click_log.txt"
# output_file_path = DIR2 + "log/simulated_click_log.txt"

# input_file_path = DIR2 + "log/simulated_click_log.txt"
# output_file_path = DIR2 + "log/simulated_click_log_.txt"
input_file_path = DIR + "log/simulated_click_log.txt"
output_file_path = DIR + "log/simulated_click_log_.txt"

json_objects = []

with open(input_file_path, "r") as input_file:
    for line in input_file:
        fields = line.strip().split(',')

        ip = str(fields[0])
        device_id = str(fields[1])
        session_id = str(fields[2])
        key_words = fields[3].split()
        ad_id = str(fields[4])
        camp_id = str(fields[5])

        json_object = {
            "ip": ip,
            "deviceId": device_id,
            "sessionId": session_id,
            "keyWords": key_words,
            "adId": ad_id,
            "campId": camp_id
        }

        json_objects.append(json_object)

# Write all JSON objects on separate lines in the output file
with open(output_file_path, "w") as output_file:
    for json_object in json_objects:
        output_file.write(json.dumps(json_object) + "\n")
