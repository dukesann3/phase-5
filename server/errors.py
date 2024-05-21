
ERRORS = {
    "VAL-001": {
        "message": "Search query is blank. It needs a query.",
        "explanation": "Occurs when search query is blank.",
        "action": "Please enter a search query."
    },
    "VAL-002": {
        "message": "There are no search results.",
        "explanation": "Occurs when search results is empty.",
        "action": "Please re-input search query for a better result."
    },
    "VAL-003": {
        "message": "Friend request could not be sent.",
        "explanation": "Occurs when there is an error at the reciever or sender level.",
        "action": "Make sure friend request was not sent twice or make sure friend request was sent to a user that exists"  
    },
    "VAL-004": {
        "message": "Friend request response could not be sent.",
        "explanation": "Occurs when friend request response is anything other than accepted or rejected.",
        "action": "Make sure to send either accepted or rejected as your response."  
    },
    "VAL-005": {
        "message": "Friend request response could not be sent.",
        "explanation": "Occurs when there is an error at the reciever or sender level.",
        "action": "Make sure friend request was not sent twice or make sure friend request was sent to a user that exists."  
    },
    "VAL-006": {
        "message": "Post could not be posted.",
        "explanation": "Occurs when location and caption are not included in the post.",
        "action": "Make sure to provide sufficient information in the post information form."  
    },
    "VAL-007": {
        "message": "Password could not be created.",
        "explanation": "Occurs when password is less than 5 characters.",
        "action": "Please re-input your password to have 5 or more characters."  
    },
    "VAL-008": {
        "message": "Username could not be created.",
        "explanation": "Occurs when another user has the same username.",
        "action": "Please re-input a different username."  
    },
    "VAL-009": {
        "message": "Comment could not be created.",
        "explanation": "Occurs when comment text and post information are not included in the request.",
        "action": "Make sure to provide sufficient information in the comment information form."  
    },
    "VAL-010": {
        "message": "Comment could not be created.",
        "explanation": "Occurs when a comment is an empty string.",
        "action": "Make sure to have at least one character in the comment box when editting it."  
    },
    "VAL-011": {
        "message": "Post could not be liked.",
        "explanation": "Occurs when a post has already been liked by the user.",
        "action": "No action necessary."  
    },
    "VAL-012": {
        "message": "Comment could not be liked.",
        "explanation": "Occurs when a comment has already been liked by the user.",
        "action": "No action necessary."  
    },
    "DB-001": {
        "message": "User profile picture could not be uploaded to server.",
        "explanation": "Occurs when image path is corrupted.",
        "action": "Please wait until developers to fix this issue. Fingers crossed."  
    },
    "DB-002": {
        "message": "User profile picture could not be editted.",
        "explanation": "Occurs when image path is corrupted.",
        "action": "Please wait until developers to fix this issue. Fingers crossed."  
    },
    "DB-003": {
        "message": "Post image could not be uploaded to server.",
        "explanation": "Occurs when image path is corrupted.",
        "action": "Please wait until developers to fix this issue. Fingers crossed."  
    },
    "DB-004": {
        "message": "Post image could not be editted.",
        "explanation": "Occurs when image path is corrupted.",
        "action": "Please wait until developers to fix this issue. Fingers crossed."  
    },
    "DB-005": {
        "message": "User profile directory could not be created.",
        "explanation": "Occurs when profile directory path is corrupted.",
        "action": "Please wait until developers to fix this issue. Fingers crossed."  
    },
    "NET-001": {
        "message": "Unable to reach server.",
        "explanation": "Occurs when internet connection is unstable.",
        "action": "Ensure you have a stable internet connection and try again."  
    },
    "NET-002": {
        "message": "Network timeout. Please check your internet connection.",
        "explanation": "Occurs when the network request times out.",
        "action": "Please try again later. Possibly database is undergoing troubles."  
    },
    "AUTH-001": {
        "message": "Could not log into account.",
        "explanation": "Occurs when either username or password is incorrect.",
        "action": "Please check your credentials and try again."  
    },
    "AUTHZ-001": {
        "message": "User not logged in.",
        "explanation": "This operation requires user authentication.",
        "action": "Please log in to your account and try again."  
    },
}

class NetworkError(Exception):
    def __init__(self, code, message, explanation, action):
        self.code = code
        self.message = message
        self.explanation = explanation
        self.action = action
        super().__init__(self.message)

class ValidationError(Exception):
    def __init__(self, code, message, explanation, action):
        self.code = code
        self.message = message
        self.explanation = explanation
        self.action = action
        super().__init__(self.message)

class AuthenticationError(Exception):
    def __init__(self, code, message, explanation, action):
        self.code = code
        self.message = message
        self.explanation = explanation
        self.action = action
        super().__init__(self.message)

class AuthorizationError(Exception):
    def __init__(self, code, message, explanation, action):
        self.code = code
        self.message = message
        self.explanation = explanation
        self.action = action
        super().__init__(self.message)

class DatabaseError(Exception):
    def __init__(self, code, message, explanation, action):
        self.code = code
        self.message = message
        self.explanation = explanation
        self.action = action
        super().__init__(self.message)

def raise_error(error_code):
    error = ERRORS.get(error_code)

    if not error:
        raise Exception("Unknown error code.")
    
    if error_code.startswith("VAL"):
        raise ValidationError(
            code=error_code,
            message=error["message"],
            explanation=error["explanation"],
            action=error["action"]
        )
    
    elif error_code.startswith("DB"):
        raise DatabaseError(
            code=error_code,
            message=error["message"],
            explanation=error["explanation"],
            action=error["action"]   
        )
    
    elif error_code.startswith("NET"):
        raise NetworkError(
            code=error_code,
            message=error["message"],
            explanation=error["explanation"],
            action=error["action"]   
        )
    
    elif error_code.startswith("AUTH"):
        raise AuthenticationError(
            code=error_code,
            message=error["message"],
            explanation=error["explanation"],
            action=error["action"]   
        )
    
    elif error_code.startswith("AUTHZ"):
        raise AuthorizationError(
            code=error_code,
            message=error["message"],
            explanation=error["explanation"],
            action=error["action"]   
        )

    else:
        raise Exception("Unknown error category.")
    
def error_to_dict(error):
    return(
        {
            "message": error.message,
            "explanation": error.explanation,
            "action": error.action
        }
    )

network_error = {        
        "message": "Unable to reach server.",
        "explanation": "Occurs when internet connection is unstable.",
        "action": "Ensure you have a stable internet connection and try again."
        } 


    


