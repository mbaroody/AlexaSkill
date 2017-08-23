from YourCustomSkill import YourCustomSkill

def lambda_handler(event, context):
    skill = YourCustomSkill(event['version'], event['session'], event['request'], context)
    return skill.processRequest()
