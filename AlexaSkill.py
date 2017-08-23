import abc

class AlexaSkill(object):
   __metaclass__ = abc.ABCMeta

   def __init__(self, version, session, request, context):
      self.intents = dict()
      self.version = version
      self.session = session
      self.request = request
      self.context = context

   # Request Format #
   # https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#RequestFormat
   def processRequest(self):
      if self.session['new']:
         self.onSessionStarted()
      if 'accessToken' not in self.session['user']:
         return self.onNotLinked()
      if self.request['type'] == 'LaunchRequest':
         return self.onLaunch()
      if self.request['type'] == 'IntentRequest' and \
         (self.request['dialogState'] == 'STARTED' or \
          self.request['dialogState'] == 'IN_PROGRESS'):
          return self.finishDialog()
      if self.request['type'] == 'IntentRequest':
         return self.onIntent()
      if self.request['type'] == 'SessionEndedRequest':
         return self.onSessionEnded()
   
   @abc.abstractmethod
   def onSessionStarted(self):
      pass

   @abc.abstractmethod
   def onLaunch(self):
      pass 
   
   def finishDialog(self):
      directives = []
      directives.append({
          'type' : 'Dialog.Delegate'
      })
      response = self.__buildResponse(directives=directives)
      return self.__buildFullResponse(version=self.version, response=response)

   def onIntent(self):
      intent = self.request['intent']['name']
      return self.intents[intent]['handler'](self.request['intent'])

   def onNotLinked(self):
      outputSpeech = {
         'type' : 'PlainText',
         'text' : "Please go to your Alexa app and link your account."
      }
      card = {
         "type" : "LinkAccount"
      }
      response = self.__buildResponse(outputSpeech=outputSpeech, card=card, shouldEndSession=True)
      return self.__buildFullResponse(version=self.version, response=response) 
       
   @abc.abstractmethod
   def onSessionEnded(self):
      pass
   
   # Response Format #
   # https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#ResponseFormat
   def __buildResponse(self, **kwargs):
      response = dict()
      response['outputSpeech'] = kwargs.get('outputSpeech', None)
      response['card'] = kwargs.get('card', None)
      response['reprompt'] = kwargs.get('reprompt', None)
      response['shouldEndSession'] = kwargs.get('shouldEndSession', None)
      response['directives'] = kwargs.get('directives', None)
      return response

   def __buildFullResponse(self, **kwargs):
      fullResponse = dict()
      fullResponse['version'] = kwargs.get('version') # required
      fullResponse['sessionAttributes'] = kwargs.get('sessionAttributes', None)
      fullResponse['response'] = kwargs.get('response') # required
      return fullResponse

   # TODO: add sessionAttributes as optional arg
   def tell(self, outputSpeech):
      response = self.__buildResponse(outputSpeech=outputSpeech, shouldEndSession=True)
      return self.__buildFullResponse(version=self.version, response=response)

   # TODO: add sessionAttributes as optional arg
   def tellWithCard(self, outputSpeech, card): 
      response = self.__buildResponse(outputSpeech=outputSpeech, card=card, shouldEndSession=True)
      return self.__buildFullResponse(version=self.version, response=response)
 
   # TODO: add sessionAttributes as optional arg
   def ask(self, outputSpeech, reprompt):
      response = self.__buildResponse(outputSpeech=outputSpeech, reprompt=reprompt, shouldEndSession=False)
      return self.__buildFullResponse(version=self.version, response=response)
 
   # TODO: add sessionAttributes as optional arg
   def askWithCard(self, outputSpeech, reprompt, card):
      response = self.__buildResponse(outputSpeech=outputSpeech, reprompt=reprompt, card=card, shouldEndSession=False)
      return self.__buildFullResponse(version=self.version, response=response)
