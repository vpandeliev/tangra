Using the Public API
====================

In the current stage, the public API is designed for sending over Tangra data to the Tangra server. The data can be sent from any website or app. However, to use Tangra, it must follow these steps. It is important the the public API must be used over HTTPS for security.

1. Get the token
----------------
The public API uses token for sending over data. The token must first be obtained. There are two methods:

1. The user logs into your site and goes to https://yoursite/get_token. Then, the user copies the token and pastes into an input. This is the most secure method, but can be cumbersome.

2. The user sends a GET request with the following header to the server:
	'Authorization : Basic *'
The star represents an encrypted user name and password. In Javascript, it can be obtained with btoa(username + ":" + password). The request is sent to https://yoursite/api/?get=token. If every goes smoothly, the server will return JSON with a token in it. To extract it, find a string with the key "token". In case of error, a JSON will also be returned, but no token in it.

2. Use the token
----------------

Gather the data as usual and send it through POST to https://yoursite/api/ with this header:
	'Authornization : Token token'
token here means the token that you have obtained.

3. Remove the token
-------------------

For maximum security, remove the token from the memory once you are done with the program.

Token Database
==============

In Tangra, you also have a token database. What you should frequently do to the database is to clear out the tokens. You do not need to worry about generating tokens for your users; when a user tries to obtain a token when he or she does not have it, the public API will automatically create one by itself.

Note that do not clear the tokens during the experiments or some participants may not be able to send everything over!