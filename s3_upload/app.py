from flask import Flask, jsonify
from app_packages.files import * 

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def fn_upload(event) :
    data = upload_file(event)
    return data

@app.route('/view', methods=['GET'])
def fn_view(event) :
    data = view_file(event)
    return data

def lambda_handler(event, context):

    # return {
    #     'statusCode': 200,
    #     'body': event
    # }

    method = event['context']['http-method']
    resource_path = event['context']['resource-path']
    with app.app_context():
        if method == 'POST':
            if resource_path == '/upload':
                resData = fn_upload(event)
                # return event
            else :
                resData = {
                    'statusCode': 200,
                    'body': "error: Request to Invalid Resource"
                }
            return {
                'statusCode': 200,
                'body': resData
            }
        elif method == 'GET':
            if resource_path == '/view':
                resData = fn_view(event)
            else :
                resData = {
                    'statusCode': 200,
                    'body': "error: Request to Invalid Resource"
                }
            return {
                'statusCode': 200,
                'body': resData
            }
        else:
            return {
                'statusCode': 400,
                'body': jsonify({'error': 'Unsupported HTTP method'})
            }
        
if __name__ == '__main__':
    app.run(debug=True)
