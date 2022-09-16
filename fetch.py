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
            print_policy_flag = False
            entities = { 'PolicyGroups':[], 'PolicyUsers': [], 'PolicyRoles':[] }

            policy_version = client.get_policy_version(
                PolicyArn = arn,
                VersionId = version_id
            )

            statement = policy_version['PolicyVersion']['Document']['Statement']

            for pol in statement: 
                if any(wanted_action in action for action in pol['Action']):
                    print_policy_flag = True
            
            if print_policy_flag:
                    print(f"\nPolicy Name: {policy['PolicyName']}")
                    print(f"Policy ARN: {arn}")
                    print(f"Allowed Actions for {wanted_action}:")

            for pol in statement:
                if any(wanted_action in action for action in pol['Action']):
                    allowed_actions = filter(lambda act: wanted_action in act, pol['Action'] )
                    for x in allowed_actions:
                        print(f"\t- {x}")
                    ent = client.list_entities_for_policy(
                        PolicyArn=arn
                    )
                    entities['PolicyGroups'].append(ent['PolicyGroups']) if ent['PolicyGroups'] not in entities['PolicyGroups'] else entities['PolicyGroups']
                    entities['PolicyUsers'].append(ent['PolicyUsers']) if ent['PolicyUsers'] not in entities['PolicyUsers'] else entities['PolicyUsers']
                    entities['PolicyRoles'].append(ent['PolicyRoles']) if ent['PolicyRoles'] not in entities['PolicyRoles'] else entities['PolicyRoles']

            if len(entities['PolicyGroups']) > 0 or len(entities['PolicyUsers']) > 0 or len(entities['PolicyRoles']) > 0:
                print("Consumed by:")
                if len(entities['PolicyGroups'][0]) > 0: 
                    print("\tPolicy Groups:")
                    for pg in entities['PolicyGroups']:
                        print(f"\t\t{str(pg).strip('[]')}")
                if len(entities['PolicyUsers'][0]) > 0: 
                    print("\tPolicy Users:")
                    for pg in entities['PolicyUsers']:
                        print(f"\t\t{str(pg).strip('[]')}")
                if len(entities['PolicyRoles'][0]) > 0: 
                    print("\tPolicy Roles:")
                    for pg in entities['PolicyRoles']:
                        print(f"\t\t- Role Name: {pg[0]['RoleName']}")
                        print(f"\t\t  Role ID: {pg[0]['RoleId']}")
            bar.next()
 
wanted_action = input("What ACTION are you looking for?\n")
print_flag = input("Do you want to save the output to a file? (Y/N)\n")

file_name = wanted_action+"-"+str(datetime.date.today())+".txt"
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