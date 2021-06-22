# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

roomTemperatures = {
    "floor 1": 39,
    "floor 2": 28,
    "floor 3": 45,
    "floor 4": 27,
    "floor 5": 34,
    "floor 6": 19,
    "floor 7": 30,
    "floor 8": 48
    }

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hi, Welcome to Museum of Docklands voice assitant skill. Please ask your question related to building systems"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
        
        
class DailyUpdateIntentHandler(AbstractRequestHandler):
        
    """Handler for Daily Update Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DailyUpdate")(handler_input)

    def handle(self, handler_input):
        logging.info('Daily Update Handler')

        speak_output = 'Here are your updates for today. Average energy consumption is forecasted to be 37 kilowatts and peak consumption between 12 pm to 2 pm. Air handling unit system, Asset number SHU, in floor 5 needs urgent maintenance.    '  
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
class TemperatureIntentHandler(AbstractRequestHandler):
        
    """Handler for Temperature Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CICTemperature")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        room = slots['floor'].value
        logging.info(room)

        speak_output = None
        
        if room is None:
            speak_output = 'You need to specify the floor number.Example is floor 1'

        else:
            if room in roomTemperatures:
                inletroomTemp = roomTemperatures[room]
                outletroomTemp=inletroomTemp + 2
                logging.info(inletroomTemp)

                speak_output = 'The inlet temperature in {room} is {temp} and outlet temperature is {output} in degree celsius.'.format(room=room,temp=inletroomTemp,output=outletroomTemp)
            else:
                speak_output = 'Sorry I could not find the temperature of {room}'.format(room=room)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class AlarmStatusIntentHandler(AbstractRequestHandler):
    """Handler for AlarmStatus Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AlarmStatus")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        floor = slots['floor'].value
        logging.info(floor)

        speak_output = None
        
        if floor is None:
            speak_output = 'You need to specify the floor number. Example response is floor one'

        else:
            if floor in roomTemperatures:
                inletroomTemp = roomTemperatures[floor]
                alarmTemp=inletroomTemp - 10 
                logging.info(inletroomTemp)

                speak_output = 'Last updated 7 seconds ago, Wet plant alarms status in {floor} is ON. HWS flow temperature is {inletroomTemp} and alarm threshold is below {alarmTemp} in degree celsius'.format(floor=floor,inletroomTemp=inletroomTemp,alarmTemp=alarmTemp)
            else:
                speak_output = 'Sorry I could not find the temperature of {floor}'.format(floor=floor)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
class SystemAwakeIntentHandler(AbstractRequestHandler):
    """Handler for Awake Device Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SystemAwake")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        system = slots['system'].value
        status = slots['status'].value
        logging.error('System is' + system)
        logging.error('Status is' + status)

        logging.info(building_systems[system])
        speak_output = None
        
        if system is None and status is None :
            speak_output = 'You need to specify the system and action'

        else:
            if system in building_systems:
                logging.info(system)
                logging.info(building_systems[system])
                if status == "ON" or status == "on":
                    building_systems[system] = True
                    speak_output = '{system} has been turned on'.format(system=system)

                elif status == "OFF" or status == "off":
                    building_systems[system] = False
                    speak_output = '{system} has been turned off'.format(system=system)

                else:
                    speak_output = 'Sorry I could not find the action you would like to proceed'

            else:
                speak_output = 'Sorry I could not find the {system} in the building.'.format(system=system)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I am available to answer your questions related to Building systems. What do you want to know?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. Can you please read manual and try asking question"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DailyUpdateIntentHandler())
sb.add_request_handler(TemperatureIntentHandler())
sb.add_request_handler(AlarmStatusIntentHandler())
sb.add_request_handler(SystemAwakeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
