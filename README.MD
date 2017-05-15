<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [**CSV Merge API**](#csv-merge-api)
  - [Dependencies](#dependencies)
  - [API End-points](#api-end-points)
    - [**`POST`** *`/files`*](#post-files)
    - [**`POST`** *`/files/:request_id`*](#post-filesrequest_id)
    - [**`DELETE`** *`/files/:request_id`*](#delete-filesrequest_id)
  - [Usage Instructions](#usage-instructions)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# **CSV Merge API**

This repo contains code to merge two *.csv files : `daily.csv` & `companies.csv`

## Dependencies
- [Python 2.7.13](https://www.python.org/downloads/release/python-2713/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)
- [flask](https://github.com/pallets/flask)

## API End-points

### **`POST`** *`/files`*
Submit a new file merge request.

- #### **Content-Type:** ```multipart/form-data```

- #### **Data Params:**

    - `daily.csv` *file*
    - `companies.csv` *file*
    - `start_date` *string* **MM/DD/YY (eg. 03/11/16)**
    - `end_date` *string* **MM/DD/YY (eg. 03/15/16)**
    - `n` *integer* **Skip Interval (>0)**

- #### **Responses:**
    * Success:
        * Response Code : 200
        * Headers: 
             - Content-Type: `text/csv`
             - Id: **integer** : *request_id*
             - Content-Disposition: `attachment; filename=merged_file.csv`
    * Error :
        * Response Code : 500 

### **`POST`** *`/files/:request_id`*
Retrieve past file merge record by ID from database.

- #### **Responses:**
    * ##### Success:
        * Response Code : 200
        * Headers: 
             - Content-Type: `application/json`
        * Body:
             - Sample Response : 
                 ```
                 {
                     "companies": [['C1', 'Company 1'], ['C1', 'Company 2']],
                     "created_at": "2017-05-13 00:50:06.158587",
                     "daily_vals": [['C1', '1/1/17', '32'], ['C2', '1/1/17', '3']],
                     "end_date": "1/1/17",
                     "n": 1,
                     "sender_ip": "127.0.0.1",
                     "start_date": "12/31/16"
                 }
                 ```
        
    * ##### Error :
        * Response Code : 404
        * Headers: 
             - Content-Type: `application/json`
        * Body :
             * Sample Response : ```{"message": "Request ID : <int> not found"}```
        

### **`DELETE`** *`/files/:request_id`*
Delete record from database.

- #### **Responses:**
    * ##### Success:
        * Response Code : 200
        * Headers: 
             - Content-Type: `application/json`        
    * ##### Error :
        * Response Code : 404
        * Headers: 
             - Content-Type: `application/json`
        * Body :
             * Sample Response : ```{"message": "Request ID : <int> not found"}```


## Usage Instructions

1. Set required permissions to the setup script
```chmod +x setup.sh```
2. Run the setup script
```sudo -H ./setup.sh <port-no>```
This will launch an instance of the web application listening on the specified port-no.
3. Make API Calls to the end-points
    - Merge CSV file
    ```
    curl -i -X POST \
      http://<ip>:<port>/csvmerge/api/1.0.0/files \
      -H 'content-type: multipart/form-data \
      -F daily.csv=@<path-to-daily.csv> \
      -F companies.csv=@<path-to-companies.csv> \
      -F start_date=12/31/16 \
      -F end_date=1/11/17 \
      -F n=1
    ```
    - Retrieve Record by ID
    ```
    curl -X POST \
      http://<ip>:<port>/csvmerge/api/1.0.0/files/<request-id>
    ```
    - Delete Record
    ```
    curl -X DELETE http://<ip>:<port>/csvmerge/api/1.0.0/files/<request-id>
    ```


