
This is Backend Part of the Default Demo Application in which the flask framework of Python
is used for making the Api.

In App.py file the Lambda Handler is defined from where the Function will get called as based on
the Api endpoint which is defined in app_packages folder.

There Are a folder name app_package where all the python files are Stored.

The Api are Defined in Api-Gateway where the Authentication will be  checked if all correct the 
request trasfferd to the Cloud Front which goes to the s3 to collect the Html documnet and exctra.
and the request get transferred to the Lambda function from where the RDS Database is Called as per
the request and data will be return data to that Api.

If You Get The CORS error then you go to the Api Gateway in AWS Account And Enable the CORS.
