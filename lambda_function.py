"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa
import json
import util

def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {
            'user_name' : 'SomeRandomDude',
            'appliication': {
                'application': ''
                }
            } # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}

    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
    return alexa.route_request(request_obj, metadata)


def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.respond('Just ask').with_card('Hello World')
alexa.default(default_handler)


@alexa.request("LaunchRequest")
def launch_request_handler(request):
    ''' Handler for LaunchRequest '''
    return alexa.create_response(message="Hello Welcome to My Recipes!")


@alexa.request("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")

@alexa.intent('StartCookingIntent')
def start_cooking_intent_handler(request):
    recipe = {
            'name': 'marinated chicken and paprika',
            'steps': [
                'Cut the chicken thighs, onion, paprika in a size easy to eat',
                'Stir fry paprika and onions with pepper and salt with a frying pan and take out once on a dish',
                'Bake the chicken thigh from the skin with a frying pan',
                'Put chicken thighs in the corner of the pan, add sugar and soy sauce, sake, vinegar in a frying pan, boil at a stretch, put 2 as well',
                'Mix with chopsticks while heating as everything fits',
                'Completion with dishes on the plate',
            ],
            'ingredients':[
                {
                    'name': 'chicken thign',
                    'amount': 'one'
                    },
                {
                    'name': 'onion',
                    'amount': 'one'
                    },
                {
                    'name': 'paprika',
                    'amount': 'one'
                    },
                {
                    'name': 'salt',
                    'amount': 'proper amount'
                    },
                {
                    'name': 'sugar',
                    'amount': 'one tablespoon '
                    },
                {
                    'name': 'soy sause',
                    'amount': 'two tablespoon'
                    },
                {
                    'name': 'sake',
                    'amount': 'two tablespoon'
                    },
                {
                    'name': 'vinegar',
                    'amount': 'one tablespoon'
                    },
                ],
            'IngredientIndex': -1,
            'StepIndex': -1
            }

    knife_skills = {
            'mince-cut': 'http://ekantcookcurry.com/wp-content/uploads/2013/01/img_4144.jpg'
            }

    request.session['State'] = 'READ_INGREDIENT'
    request.session['Recipe'] = recipe
    request.session['KnifeSkill'] = knife_skills
    message = "ok lets cook {}. Are you ready?".format(recipe['name'])

    return alexa.create_response(message, end_session=False)

def create_resource_message(state, index, resources):
    message = ''
    if state == 'READ_INGREDIENT':
        ingredient = resources[index]
        message += '{0} {1}'.format(ingredient['name'], ingredient['amount'])
        if (index + 1) == len(resources):
            message += '. Will read step.'
        else:
            message += '. Will read next. okay?'
    elif state == 'READ_STEP':
        step = resources[index]
        message += step
        if (index + 1) == len(resources):
            message += '. Finish. Lets eat!!'
        else:
            message += '. Will read next. okay?'
    else:
        return 'Sorry, I cant find answer'

    return message

def create_resource_card(state, index, resources):
    if state == 'READ_INGREDIENT':
        ingredient = resources[index]
        return alexa.create_card(title=ingredient['name'], content=ingredient['amount'])
    elif state == 'READ_STEP':
        step = resources[index]
        return alexa.create_card(title='Step {}'.format(index), content=step)
    else:
        return 'Sorry, I cant find answer'

def create_resource_response(request):
    state = request.session['State']
    recipe = request.session['Recipe']
    if state == 'READ_INGREDIENT':
        index = recipe['IngredientIndex']
        message = create_resource_message(state, index, recipe['ingredients'])
        card = create_resource_card(state, index, recipe['ingredients'])
        return alexa.create_response(message, end_session=False, card_obj=card)

    elif state == 'READ_STEP':
        index = recipe['StepIndex']
        message = create_resource_message(state, index, recipe['steps'])
        card = create_resource_card(state, index, recipe['steps'])

        return alexa.create_response(message, end_session=False, card_obj=card)
    else:
        message = 'I cant find answer. one more please'
        return alexa.create_response(message, end_session=False)

@alexa.intent('NextIntent')
def next_intent_handler(request):
    end_session = False
    if request.session['State'] == 'READ_INGREDIENT':
        request.session['Recipe']['IngredientIndex'] += 1
        if (request.session['Recipe']['IngredientIndex'] + 1) == len(request.session['Recipe']['ingredients']):
            request.session['State'] = 'READ_STEP'
    elif request.session['State'] == 'READ_STEP':
        request.session['Recipe']['StepIndex'] += 1
        if (request.session['Recipe']['StepIndex'] + 1) == len(request.session['Recipe']['steps']):
            end_session = True
    else:
        return create_response('I cant understand it.', end_session=end_session)

    return create_resource_response(request)

@alexa.intent('BackIntent')
def back_intent_handler(request):
    if request.session['State'] == 'READ_INGREDIENT':
        request.session['Recipe']['IngredientIndex'] -= 1
    elif request.session['State'] == 'READ_STEP':
        request.session['Recipe']['StepIndex'] -= 1
    else:
        return create_response('I cant understand it.', end_session=False)

    return create_resource_response(request)


@alexa.intent('IndexIntent')
def index_intent_handler(request):
    index = request.slots['Index']
    if request.session['State'] == 'READ_INGREDIENT':
        request.session['Recipe']['IngredientIndex'] = index
    elif request.session['State'] == 'READ_STEP':
        request.session['Recipe']['StepIndex'] = index
    else:
        return create_response('I cant understand it.', end_session=False)

    return create_resource_response(request)

@alexa.intent('RepeatIntent')
def repeat_intent_handler(request):
    return create_resource_response(request)

@alexa.intent('KnifeSkillIntent')
def knife_skill_intent_handler(request):
    skill_name = request.slots['skill_name']
    skill_name = skill_name.replace(' ', '-')
    knife_skills = request.session['KnifeSkill']
    if skill_name in knife_skills:
        message = 'This is {}'.format(skill_name)
        card = alexa.create_card(title=skill_name, content=knife_skills[skill_name], card_type='Standard')
        image = {
                'smallImageUrl': 'http://ekantcookcurry.com/wp-content/uploads/2013/01/img_4144.jpg',
                'largeImageUrl': 'http://ekantcookcurry.com/wp-content/uploads/2013/01/img_4144.jpg'
                }
        card['image'] = image
        return alexa.create_response(message, card_obj=card, end_session=False)
    else:
        return alexa.create_response('I cant find answer.')

if __name__ == "__main__":    
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve','-s', action='store_true', default=False)
    args = parser.parse_args()
    
    if args.serve:        
        ###
        # This will only be run if you try to run the server in local mode 
        ##
        print('Serving ASK functionality locally.')
        import flask
        server = flask.Flask(__name__)
        @server.route('/')
        def alexa_skills_kit_requests():
            request_obj = flask.request.get_json()
            return lambda_handler(request_obj)
        server.run()
