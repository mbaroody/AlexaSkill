import abc

class AlexaSkill(object):
   __metaclass__ = abc.ABCMeta

   def __init__(self, version, session, request, context):
      self.intents = dict()
      self.version = version
      self.session = session
      self.request = request
      self.context = context

   @abc.abstractmethod
   def onSessionStarted(self):
      pass

   @abc.abstractmethod
   def onLaunch(self):
      pass 

   def onIntent(self):
      intent = self.request['intent']['name']
      return self.intents[intent]['handler']()

   def onNotLinked(self):
      outputSpeech = {
         'type' : 'PlainText',
         'text' : "Please go to your Alexa app and link your account."
      }
      
      card = {
         "type" : "LinkAccount"
      }

      reprompt = {}

      shouldEndSession = True
      version = self.version
      sessionAttributes = {}
      response = self.__buildResponse(outputSpeech, card, reprompt, shouldEndSession)
      return self.__buildFullResponse(version, sessionAttributes, response) 
       
   @abc.abstractmethod
   def onSessionEnded(self):
      pass

   # Request Format #
   # https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#RequestFormat
   def processRequest(self):
      if self.session['new']:
         self.onSessionStarted()

      if 'accessToken' not in self.session['user']:
         return self.onNotLinked()

      if self.request['type'] == 'LaunchRequest':
         return self.onLaunch()
      
      if self.request['type'] == 'IntentRequest':
         return self.onIntent()
      
      if self.request['type'] == 'SessionEndedRequest':
         return self.onSessionEnded()
   
   # Response Format #
   # https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#ResponseFormat
   def __buildResponse(self, outputSpeech, card, reprompt, shouldEndSession):
      return {
         'outputSpeech' : outputSpeech,
         'card' : card,
         'reprompt' : reprompt,
         'shouldEndSession' : shouldEndSession
      }

   def __buildFullResponse(self, version, sessionAttributes, response):
      return {
         'version' : version,
         'sessionAttributes' : sessionAttributes,
         'response' : response
      }

   def tell(self, version, sessionAttributes, outputSpeech):     
      outputSpeech = {
         'type' : 'PlainText',
         'text' : 'Welcome to Connected Home. What would you like to do?'
      }

      card = {}

      reprompt = {}

      shouldEndSession = True
        
      response = self.__buildResponse(outputSpeech, card, reprompt, shouldEndSession)
      
      return self.__buildFullResponse(version, sessionAttributes, response)

   def tellWithCard(self, version, sessionAttributes, outputSpeechText, cardTitle, cardText, cardImages): 
      outputSpeech = {
         'type' : 'PlainText',
         'text' : outputSpeechText
      }

      card = {
         'type' : 'Standard',
         'title' : cardTitle,
         'text' : cardText,
         'image' : cardImages
      }


      reprompt = {}
      
      shouldEndSession = True
      
      response = self.__buildResponse(outputSpeech, card, reprompt, shouldEndSession)
      
      return self.__buildFullResponse(version, sessionAttributes, response)
 
   def ask(self, version, sessionAttributes, outputSpeechText, repromptText): 
      outputSpeech = {
         'type' : 'PlainText',
         'text' : outputSpeechText
      }

      card = {}

      reprompt = {
         'outputSpeech' : {
            'type' : 'PlainText',
            'text' : repromptText
         }
      }

      shouldEndSession = False

      response = self.__buildResponse(outputSpeech, card, reprompt, shouldEndSession)

      return self.__buildFullResponse(version, sessionAttributes, response)
 
   def askWithCard(self, version, sessionAttributes, outputSpeechText, cardTitle, cardText, cardImages, repromptText):
      outputSpeech = {
         'type' : 'PlainText',
         'text' : outputSpeechText
      }

      card = {
         'type' : 'Standard',
         'title' : cardTitle,
         'text' : cardText,
         'image' : cardImages
      }


      reprompt = {
         'outputSpeech' : {
            'type' : 'PlainText',
            'text' : repromptText
         }
      }

      shouldEndSession = False

      response = self.__buildResponse(outputSpeech, card, reprompt, shouldEndSession)

      return self.__buildFullResponse(version, sessionAttributes, response)
