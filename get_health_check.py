import boto3

session = boto3.session.Session(profile_name='infor-int')
health=session.client(service_name='health',region_name='us-east-1')

#Varibales 
service_accepted=['EC2', 'S3', 'FSX', 'EFS', 'EBS', 'RDS','DIRECTCONNECT']
arn =[]

#Class

# To get service arn 
for service in service_accepted:
    response = health.describe_events()
    for each_item in response['events']:
        if each_item['eventScopeCode'] == 'ACCOUNT_SPECIFIC' and each_item['service'] == service:
            #print(each_item)
            arn.append(each_item['arn'])
            
# To use service arn to get description
for arns in arn:
    response_arn = health.describe_event_details(
    eventArns=[arns]
    )
    break
    for test in response_arn.get('successfulSet'):
          print(test.get('event')['region'])
          print(test.get('event')['arn'])