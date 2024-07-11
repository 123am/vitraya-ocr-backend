from base import *

auth=Blueprint("auth",__name__)


@auth.route("/login",methods=["POST"])
def login():

    
    data=request.get_json()
    aggr=[
        {
            '$match': {
                'username': data["username"],
                'password': data["password"]
            }
        },{
            '$lookup': {
                'from': 'userRole', 
                'localField': 'userRole', 
                'foreignField': '_id', 
                'as': 'userRoleData'
            }
        }, {
            '$unwind': {
                'path': '$userRoleData', 
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$addFields': {
                'userRoleName': '$userRoleData.userRole', 
                'userRole': {
                    '$toString': '$userRole'
                }, 
                'uniqueId': {
                    '$toString': '$_id'
                }
            }
        }, {
            '$project': {
                'userRoleData': 0, 
                '_id': 0,
                "password":0
            }
        }
    ]
    
    data_r=cmo.finding_aggregate("userAuth",aggr)
    print(data_r)
    print(os.environ.get("SECRET"),'os.environ.get("SECRET")')
    if(len(data_r["data"])>0):
        encoded = jwt.encode(data_r["data"][0], os.environ.get("SECRET"), algorithm="HS256")
        
        data_e=data_r["data"][0]
        data_e["token"]=encoded
        data_r["data"]=data_e
        return data_r,200
        
        
        
    else:
        data_r["msg"]="Invalid Credentials"
        data_r["status"]=400
        data_r["data"]=[]
        return data_r,400


@auth.route("/listUserRole",methods=["GET"])
def listUserRole():

    aggr=[
        {
            '$addFields': {
                'uniqueId': {
                    '$toString': '$_id'
                }
            }
        }, {
            '$project': {
                '_id': 0
            }
        }
    ]

    data_r=cmo.finding_aggregate("userRole",aggr)

    return data_r,200


@auth.route("/register",methods=["POST"])
def register():

    data=request.get_json()
    aggr=[{'$match': {'username': data["username"]}}]
    data_r=cmo.finding_aggregate("userAuth",aggr)
    if(len(data_r["data"])>0):
        data_r["msg"]="UserName is already exist"
        data_r["status"]=400
        data_r["data"]=[]
        return data_r,400


    data=cmo.insertion("userAuth",data)

    data["msg"]="User Register Successfully"

    return data,201