#cretaing a unique token/string for activating the user of the account
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

#making class which will generate token that is inheritance to the passwordResetTokenGenerator
class TokenGenerator(PasswordResetTokenGenerator):
  #making function inside the class
  def _make_hash_value(self,user,timestamp):

    #returning texttype with unique code for the user
    return (
        text_type(user.pk) + text_type(timestamp) 
    
    )
 #calling the class
generate_token = TokenGenerator()