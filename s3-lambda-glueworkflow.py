import json
import boto3
print('Loading function')

def lambda_handler(event, context):
    # Extract bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Extract folder path and file name from the object key
    folder_path, file_name = '/'.join(object_key.split('/')[:-1]), object_key.split('/')[-1]
    
    # Extract the specific operation from the event
    operation = event['Records'][0]['eventName']
    
    # Print the operation, folder path, and the file name
    print("Operation '{}' performed in folder: s3://{}/{} for file: {}".format(operation, bucket_name, folder_path, file_name))


    # Initialize AWS Glue client
    glue_client = boto3.client('glue')
    
    # Specify the name of the Glue workflow to trigger
    workflow_name = 'sbst-run-migration'
    
    try:
        # Start the workflow run
        response = glue_client.start_workflow_run(Name=workflow_name)
        
        # Print the response
        print("Workflow run started successfully:", response)
        
        return {
            'statusCode': 200,
            'body': 'Workflow run started successfully'
        }
    except Exception as e:
        # Handle any errors
        print("Error starting workflow run:", e)
        return {
            'statusCode': 500,
            'body': 'Error starting workflow run'
        }
