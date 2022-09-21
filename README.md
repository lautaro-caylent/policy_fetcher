# Policy Fetcher
This humble script is meant to help you make security assessment by checking how many **attached** policies are using a given **policy action**, it will also list all the Groups, Users and Roles that consume these policies and output everything into a formated text File.

The script uses the provided **action** string to look for any policies that contain given action. It's **not** necessarily a complete action, you can use a "wildcard" search by providing an incomplete action. See the examples directory for outputs given the following action strings:
- "**route53**": Every action that contains route53 in it, this would search for all route53 related policies (E.g. route53:*).
- "**ec2:Delete**": Every delete action over EC2 resources (E.g. ec2:DeleteLaunchTemplate, ec2:DeleteNatGateway, ec2:DeleteRouteTable).
- "**ec2:TerminateInstances**": Only policies allowing this specific action.

## Prerequisites
 - Have CLI access to the AWS account where to look for the policies.
 - Python version >= 3.8 installed.
 - AWS CLI version 2 installed.
 - Having a **VALID** policy action, please check [here](https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html) for all available actions.

## How to use the script
1. Download this repository to your local machine.
2. Change directory into the repository root folder.
3. Install dependencies by using:
   ```
   pip install -r requirements.txt
   ```
4.  Configure your AWS credentials, either by environment variables or local profile.
5.  Run the python script by using:
    ```
    python fetch.py
    ```
6.  Follow the instructions provided in the terminal.


## Considerations
This initial version of the script has **only** been tested in a Linux distribution. 

If you find any issues or improvements to be done to this script, please open an issue or contact lautaro.baltar@caylent.com.
