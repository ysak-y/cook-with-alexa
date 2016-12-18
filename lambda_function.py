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
                ]
            }

    knife_skills = {
            'mince cut': 'http://ekantcookcurry.com/wp-content/uploads/2013/01/img_4144.jpg'
            }

    request.session['state'] = 'READ_INGREDIENT'
    request.session['ingredient_index'] = 0
    request.session['recipe'] = recipe
    message = "ok lets cook {}. Are you ready?".format(recipe['name'])

    return alexa.create_response(message, end_session=False)

@alexa.intent('YesIntent')
def yes_intent_handler(request):

    if request.session['state'] == 'READ_INGREDIENT':
        recipe = request.session['recipe']
        ingredient_index = request.session['ingredient_index']
        ingredient = recipe['ingredients'][ingredient_index]
        message = '{0} {1}.'.format(ingredient['name'], ingredient['amount'])

        card = alexa.create_card(title=ingredient['name'], content=ingredient['amount'])

        if (ingredient_index + 1) == len(recipe['ingredients']):
            message += 'ingredient finish. will read steps'
            request.session['state'] = 'READ_STEP'
            request.session['step_index'] = 0
        else:
            message += 'will read next. okay?'
            request.session['ingredient_index'] = ingredient_index + 1
        return alexa.create_response(message, end_session=False, card_obj=card)

    elif request.session['state'] == 'READ_STEP':

        recipe = request.session['recipe']
        step_index = request.session['step_index']
        step = recipe['steps'][step_index]
        message = '{0}.'.format(step)
        card = alexa.create_card(title='Step {}'.format(step_index), content=step[step_index])

        if (step_index + 1) == len(recipe['steps']):
            message += 'step finish. will read steps'
            request.session['state'] = 'READ_STEP'
        else:
            message += 'will read next. okay?'
            request.session['step_index'] = step_index + 1
        return alexa.create_response(message, end_session=False, card_obj=card)

    else:
        message = 'I cant find answer. one more please'
        return alexa.create_response(message, end_session=False)

@alexa.intent('BackIntent')
def back_intent_handler(request):

    if request.session['state'] == 'READ_INGREDIENT':
        recipe = request.session['recipe']
        ingredient_index = request.session['ingredient_index']
        ingredient = recipe['ingredients'][ingredient_index]
        message = '{0} {1}.'.format(ingredient['name'], ingredient['amount'])

        card = alexa.create_card(title=ingredient['name'], content=ingredient['amount'])

        if (ingredient_index + 1) == len(recipe['ingredients']):
            message += 'ingredient finish. will read steps'
            request.session['state'] = 'READ_STEP'
            request.session['step_index'] = 0
        else:
            message += 'will read next. okay?'
            request.session['ingredient_index'] = ingredient_index + 1
        return alexa.create_response(message, end_session=False, card_obj=card)

    elif request.session['state'] == 'READ_STEP':

        recipe = request.session['recipe']
        step_index = request.session['step_index']
        step = recipe['steps'][step_index]
        message = '{0}.'.format(step)
        card = alexa.create_card(title='Step {}'.format(step_index), content=step[step_index])

        if (step_index + 1) == len(recipe['steps']):
            message += 'step finish. will read steps'
            request.session['state'] = 'READ_STEP'
        else:
            message += 'will read next. okay?'
            request.session['step_index'] = step_index + 1
        return alexa.create_response(message, end_session=False, card_obj=card)

    else:
        message = 'I cant find answer. one more please'
        return alexa.create_response(message, end_session=False)

@alexa.intent('IndexIntent')
def index_intent_handler(request):
    if request.session['state'] == 'READ_INGREDIENT':
        recipe = request.session['recipe']
        ingredient_index = request.session['ingredient_index']
        ingredient = recipe['ingredients'][ingredient_index]
        message = '{0} {1}.'.format(ingredient['name'], ingredient['amount'])

        card = alexa.create_card(title=ingredient['name'], content=ingredient['amount'])

        if (ingredient_index + 1) == len(recipe['ingredients']):
            message += 'ingredient finish. will read steps'
            request.session['state'] = 'READ_STEP'
            request.session['step_index'] = 0
        else:
            message += 'will read next. okay?'
            request.session['ingredient_index'] = ingredient_index + 1
        return alexa.create_response(message, end_session=False, card_obj=card)

    elif request.session['state'] == 'READ_STEP':

        recipe = request.session['recipe']
        step_index = request.session['step_index']
        step = recipe['steps'][step_index]
        message = '{0}.'.format(step)
        card = alexa.create_card(title='Step {}'.format(step_index), content=step[step_index])

        if (step_index + 1) == len(recipe['steps']):
            message += 'step finish. will read steps'
            request.session['state'] = 'READ_STEP'
        else:
            message += 'will read next. okay?'
            request.session['step_index'] = step_index + 1
        return alexa.create_response(message, end_session=False, card_obj=card)

    else:
        message = 'I cant find answer. one more please'
        return alexa.create_response(message, end_session=False)


@alexa.intent('RepeatIntent')
def repeat_intent_handler(request):
    if request.session['state'] == 'READ_INGREDIENT':
        idx = request.session['ingredient_index']
        ingredient = request.session['recipe']['ingredients'][idx]
        message = '{0} {1}.'.format(ingredient['name'], ingredient['amount'])
    elif request.session['state'] == 'READ_STEP':
        idx = request.session['step_index']
        step = request.session['recipe']['steps'][idx]
        message = '{}.'.format(step)
    else:
        message = 'i cant find answer. one more please'

    return alexa.create_response(message, end_session=False)

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
