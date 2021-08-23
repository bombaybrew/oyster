import requests
import csv
import os
import json
import glob

CMS_DATASET_URL = "http://localhost:8000/dataset"
DATASET_PATH = "./data/*.csv"
MAX_ROW_PER_DATASET = 500
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def upload_datasets():

    result = glob.glob(DATASET_PATH)
    for dataset in result:
        print("--- PROCESSING : ", dataset)
        upload_csv(dataset)

def upload_csv(csv_input):

    try:
        dataset_id = create_cms_dataset(csv_input)

        with open(csv_input) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                if line_count > MAX_ROW_PER_DATASET:
                    break

                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    data = {}
                    data['data'] = str(row[0])
                    upload_cms(dataset_id, data)
                    line_count += 1
    except Exception as err:
        print(err)


def create_cms_dataset(name):
    base_name = os.path.basename(name).split(".")[0]
    data = {
        "name": base_name
    }
    try:
        response = requests.post(
            CMS_DATASET_URL, data=json.dumps(data), headers=headers)
        return response.json().get("id")
    except Exception as err:
        print(err)


def upload_cms(dataset_id, data):
    try:
        response = requests.post(
            CMS_DATASET_URL+"/"+dataset_id, data=json.dumps(data), headers=headers)
        print(response.text)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    upload_datasets()
