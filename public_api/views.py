"""
view.py
This file contains the code for the public API.
"""

from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from django.utils import timezone
from studies.models import *
from studies.views import *
from django.core.exceptions import *


class PublicAPIView(APIView):
    """
    The class that represents the public API. Since it is manipulating Data
    table as of now, its name will be DataView. In the future, it might be
    renamed.
    """
    
    renderer_classes = (JSONRenderer,)
    authentication_classes = (#authentication.SessionAuthentication,
                              authentication.TokenAuthentication,
                              authentication.BasicAuthentication)
    """
    Notably, Session Authentication has been disabled. So to access the data
    in Tangra, follow these steps:
    - Use Basic Authentication to obtains a token for a user by using GET
      with value get=token.
    - Then for each data to be sent into Tangra, put the token into the header.
    - After the user is done, clear the token from the memory.
    """

    def get(sef, request, format=None):
	"""
	Support the GET method in the API. Currently, it allows for a token to
	be obtained for a user.
	
	- request: The user information and the data sent from the the user side.
	
	Return a response accompanying with HTTP code. If successful, a JSON 
	with the token will be returned; simply access 'token' to obtain it.
	In the case of failure, 'error' will be included in JSON and the
	message can be read from there.
	"""
	
	try:
	    if request.QUERY_PARAMS["get"] == "token":
		
		from rest_framework.authtoken.models import Token
				
		c = Token.objects.filter(user=request.user).count()
		
		# In this portal, a new token is made if a user has no token.
		
		if c > 0:
		    t = Token.objects.get(user=request.user)
		    return Response({"token":str(t), "defail":"success"}, status=status.HTTP_200_OK)
		else:
		    t = Token.objects.create(user=request.user)
		    return Response({"token":str(t)}, status=status.HTTP_201_CREATED)
	    else:
		return Response({"detail" : "Bad request", 
		                 "data": str(request.GET)}, 
		                status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
	    return Response({"detail" : str(e), "data":str(request.GET)}, status=status.HTTP_400_BAD_REQUEST) 


    def post(self, request, format=None):
        """
        Support the POST method in the API.
	
	- request: The user information and the data sent from the user side.
	
	Return a response along with a JSON. There is no need to pry into JSON
	to know whether an operation succeeds or not since HTTP code is also
	attached to it. However, if there is a failure, look for 'error' in
	the JSON as it contains the exception message.
        """
        
        try:
	    
		
	    """
	    Note that the data sent via POST must be a JSON and it must follow
	    this format:
	    - study: the study's API name.
	    - timestamp: a datetime string following the format of YYYY-MM-DD HH:MM:SS.
	      It can also be "now" which uses the time when the server receives
	      the data instead.
	    - datum: a string, can be of any format
	    """
	    
	    # Set up the date.
	    t = str(timezone.now())
	    if request.DATA.has_key("timestamp"):
		if request.DATA["timestamp"] != "now":
		    t = request.DATA["timestamp"]
	    
	    # Get the user stage and make sure that the user is allowed to access it.
	    study = Study.objects.get(api_name=request.DATA["study"])
	    us = UserStage.objects.get(group_stage__stage__study=study,
	                               group_stage__stage__url=request.DATA["stage"],
	                               user=request.user, status=1)
	    
	    # Finally create a new data.
	    new_data = Data.objects.create(user=request.user,
	                                   timestamp=t,
	                                   user_stage=us,
	                                   datum=request.DATA['datum'])
	    
	    # Check out for complete signal.
	    if request.DATA.has_key("completed"):
		print(request.DATA["completed"])
		us.complete_stage()
		next_us = get_next_user_stage(request.user, study)
				
		if next_us != None:
		    next_us.start_stage()

	    
	    # Return the JSON string message.
	    return Response({"detail" : "success"}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
	    return Response({"detail" : "User is not registered for this study or the study doesn't exist."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)