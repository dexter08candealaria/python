import boto3
from datetime import datetime, timedelta
import csv

session = boto3.session.Session(profile_name='dexter-test')
client = session.client('iam')
users = client.list_users()

flaggedUsers = []
flaggedUserThreshold = 10

for key in users['Users']:
        flaggedUser = {}
        username = key['UserName']
        
        # List access keys through the pagination interface.
        paginator = client.get_paginator('list_access_keys')

        for response in paginator.paginate(UserName=username):
                accessKeyMetadata = response['AccessKeyMetadata']
                
                # Check if user has some keys, if not continue with next user in the list 
                if len(accessKeyMetadata) != 0:
                        accessKeyId = accessKeyMetadata[0]['AccessKeyId']
                        accessKeyLastUsedResponse = client.get_access_key_last_used(AccessKeyId=accessKeyId)
                        accessKeyLastUsed = accessKeyLastUsedResponse['AccessKeyLastUsed']
                        lastUsedDate = (accessKeyLastUsed.get('LastUsedDate'))
                        
                        if lastUsedDate == None:
                            pass
                        else:
                            lastActivity = datetime.now(lastUsedDate.tzinfo) - lastUsedDate
                            accessKeyCreationDate = accessKeyMetadata[0]['CreateDate']
                            accessKeyAge = datetime.now(accessKeyCreationDate.tzinfo) - accessKeyCreationDate
                            
                        if lastActivity.days >= flaggedUserThreshold or accessKeyAge.days >= flaggedUserThreshold:
                                flaggedUser['username'] = key['UserName']
                                flaggedUser['accessKeyId'] = accessKeyId
                                flaggedUser['lastActivity'] = lastActivity.days
                                flaggedUser['accessKeyAge'] = accessKeyAge.days
                                flaggedUsers.append(flaggedUser)
                else:
                        continue

                        
                        
# Print all the flagged users
tocsv = []
for users in flaggedUsers:
    Username = users['username']
    AccessKeyId = users['accessKeyId']
    LastActivity = users['lastActivity']
    AccessKeyAge = users['accessKeyAge']
    tocsv.append([Username,AccessKeyId,LastActivity,AccessKeyAge])

with open('access_result_{}.csv'.format(session.profile_name), 'a') as f:
    accesskey_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    accesskey_writer.writerow(['Username', 'AccessKeyId', 'LastActivity','AccessKeyAge'])
    for row in tocsv:
        accesskey_writer.writerow(row)
f.close()
    