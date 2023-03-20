from flask_restful import Api, Resource, reqparse


class UserApiHandler(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'message': "Hello Api Handler"
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    args = parser.parse_args()

    print(args)
    email = args['email']
    password = args['password']
    status = False
    if email and password:
        status = True
        if email == "kaymakasm@gmail.com" and password == "kanarya10":

            message = "Successfuly logged!"
        else:
            message = "Wrong email or password!"
      
    else:
      status = False
      message = "No Msg"
    
    final_ret = {"status": status, "message": message}

    return final_ret