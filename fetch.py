import boto3
import datetime
import sys
import os
from progress.bar import Bar

def fetch_iam_resources( wanted_action ):

    client = boto3.client('iam')

    response = client.list_policies(
        Scope='All',
        OnlyAttached=True
    )
    with Bar('Processing...', max=len(response['Policies'])) as bar:
        for policy in response['Policies']:
            arn = policy['Arn']
            version_id = policy['DefaultVersionId']

            policy_version = client.get_policy_version(
                PolicyArn = arn,
                VersionId = version_id
            )

            statement = policy_version['PolicyVersion']['Document']['Statement']

            for pol in statement:
                if any(wanted_action in action for action in pol['Action']):
                    allowed_actions = filter(lambda act: wanted_action in act, pol['Action'] )
                    print(f"\nPolicy Name: {policy['PolicyName']}")
                    print(f"Policy ARN: {arn}")
                    print(f"Allowed Actions for {wanted_action}:")
                    for x in allowed_actions:
                        print(f"\t- {x}")
                    entities = client.list_entities_for_policy(
                        PolicyArn=arn
                    )
                    print("Consumed by:")
                    if len(entities['PolicyGroups']) > 0: 
                        print("\tPolicy Groups:")
                        print(f"\t\t{entities['PolicyGroups']}")
                    if len(entities['PolicyUsers']) > 0: 
                        print("\tPolicy Users:")
                        print(f"\t\t{entities['PolicyUsers']}")
                    if len(entities['PolicyRoles']) > 0: 
                        print("\tPolicy Roles:")
                        print(f"\t\t{entities['PolicyRoles']}")
            bar.next()
 
wanted_action = input("What ACTION are you looking for?\n")
print_flag = input("Do you want to save the output to a file? (Y/N)\n")

file_name = wanted_action+"_ALLOWED_IAM-"+str(datetime.date.today())+".txt"
file_dir = "" # Default value used for validation
if print_flag.upper() == "Y": 
    while(not os.path.isdir(file_dir)):
        file_dir = input(f"Where should '{file_name} be stored? Leave blank for current directory.\n") or "./"

original_stdout = sys.stdout # Save a reference to the original standard output

if print_flag.upper() == "Y":
    with open( file_dir + file_name, 'w+' ) as f:
        sys.stdout = f # Change the standard output to the file we created.
        fetch_iam_resources( wanted_action )
        sys.stdout = original_stdout # Reset the standard output to its original value
else:
    fetch_iam_resources( wanted_action )