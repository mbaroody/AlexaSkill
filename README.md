# Example Usage
```python
from AlexaSkill import AlexaSkill

class YourCustomSkill(AlexaSkill):

    def __init__(self, version, session, request, context):
        super(YourCustomSkill, self).__init__(version, session, request, context)
        self.intents['SomeIntent'] = dict();
        self.intents['SomeIntent']['handler'] = self.SomeIntentHandler;

    def onSessionStarted(self):
        # implement this how you want
        return

    def onLaunch(self):
        # implement this how you want
        return

    def onSessionEnded(self):
        # implement this how you want
        return

    def SomeIntentHandler() 
        outputSpeech = {
            'type' : 'PlainText'
        }
        if intent['slots']['CustomSlot']['value'] == 'some value':
            outputSpeech['text'] = 'alexa found out you said some value'
        else:
            outputSpeech['text'] = 'alexa sucks, in that it can return a value you have not defined in a custom slot. you suck, alexa!'
        return self.tell(outputSpeech)            
```
