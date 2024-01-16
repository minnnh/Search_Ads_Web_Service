import os
import sys
import json
import random

BUDGET_FILE = "budget.txt"
FILE_DIR = "../../data/deduped/"

if __name__ == "__main__":
    output_file = FILE_DIR + BUDGET_FILE
    output = open(output_file, "w")
    temp = "{\"campaignId\":8001,\"budget\":1500}"

    for i in range(8001,8900):
        entry = json.loads(temp.strip())
        entry["campaignId"] = i
        entry["budget"] = random.randint(100,2000)
        output.write(json.dumps(entry))
        output.write('\n')

    output.close()

