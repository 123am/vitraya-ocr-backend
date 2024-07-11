from base import *

publisher=Blueprint("publisher",__name__)

reader = easyocr.Reader(['en'])


@publisher.route("/addContent",methods=["POST"])
@token_auth_check
def addContent(current_user):
    coverImage_file=request.files.get("coverImage[]")
    req_form=request.form
    file_name=cutils.file_name(coverImage_file)
    path=os.path.join("uploads",file_name)
    full_path=os.path.join(os.getcwd(),"uploads",file_name)
    coverImage_file.save(full_path)
    
    result = reader.readtext(full_path,detail=2)
    print(req_form,full_path,"req_form")
    img = cv2.imread(full_path)
    
    # print(img,"imgimgimgimg")
    
    # for i in img:
    #     print(i,"dsadsada")
    
    print(result,"resultresultresult")

    json_data=cutils.form_to_json(req_form)
    
    txt=[]
    teq=""
    for detection in result:
        print(detection)
        txt.append(detection[1].strip())
        teq=teq+detection[1].strip()+" "
    json_data["txt"]="<br/>".join(txt)
    json_data["tee"]=teq
    

    with open(full_path, "rb") as f:
        encoded_image = base64.b64encode(f.read())
        encoded_image_string = encoded_image.decode('utf-8')
        print(encoded_image,"encoded_image")
        json_data["encoded_image"]=encoded_image_string
    
    
    json_data["coverImage"]=path
    json_data["userId"]=current_user["uniqueId"]
    
    print(json_data)
    
    data=cmo.insertion("contents",json_data)

    data["msg"]="Content Added Successfully"

    return data,201



@publisher.route("/addFromCart",methods=["POST"])
@token_auth_check
def addFromCart(current_user):
    
    data=request.get_json()
    data["userId"]=current_user["uniqueId"]
    resp=cmo.insertion("userCart",data)
    
    
    
    return resp,201

@publisher.route("/checkoutCart",methods=["POST"])
@token_auth_check
def checkoutCart(current_user):
    
    
    
    data=request.get_json()
    data_r=getMyCart(True)
    
    print(data_r,"data_rdata_r")
    

    subTotal=data_r["data"]["totalSum"]
    tax=data_r["data"]["tax"]
    AddOn=data_r["data"]["addOns"]
    Tax_price=subTotal/tax
    
    total_cart_price=AddOn+subTotal+Tax_price
    msg=""
    
    if(int(Tax_price)!=int(data["Tax_price"])):
        msg+=f"Tax price modified. original {Tax_price} modified {data['Tax_price']}"
    
    if(int(AddOn)!=int(data["Addons"])):
        msg+=f"Addons price modified. original {AddOn} modified {data['Addons']}"
    
    if(int(subTotal)!=int(data["subTotal"])):
        msg+=f"subTotal price modified. original {subTotal} modified {data['subTotal']}"
    
    if(int(tax)!=int(data["tax"])):
        msg+=f"tax price modified. original {tax} modified {data['tax']}"
        
    if(int(total_cart_price)!=int(data["total_cart_price"])):
        msg+=f"total_cart_price price modified. original {total_cart_price} modified {data['total_cart_price']}"
        
        
    
    data["userId"]=current_user["uniqueId"]
    
    if(msg!=""):
        data["msg"]=msg
        cmo.insertion("checkOut_fraud",data)
        
    ctr=[
        {
            '$sort': {
                '_id': -1
            }
        }
    ]
    ctr_data=cmo.finding_aggregate("checkOut",ctr)["data"]
        
    InvId="INVOICE-000001"
    if(len(ctr_data)!=0):
        invVal=ctr_data[0]["invoiceId"]
        
        invVal=invVal.replace("INVOICE-","")
        InvId=f"INVOICE-{'0'*(6-len(str(int(invVal))))}{int(invVal)+1}"
        
    newData={
        "tax":tax,
        "AddOn":AddOn,
        "Tax_price":Tax_price,
        "total_cart_price":total_cart_price,
        "invoiceId":InvId,
        "data":data_r["data"]["result"]
    }
    
    resp = cmo.real_deleting_many("userCart",{"userId":current_user["uniqueId"]})
    
    resp=cmo.insertion("checkOut",newData)
    
    resp["msg"]=f"Checkout Successfully of payment {total_cart_price}"   
    
    
    
    
    return resp,201


@publisher.route("/subFromCart",methods=["POST"])
@token_auth_check
def subFromCart(current_user):
    
    data=request.get_json()
    data["userId"]=current_user["uniqueId"]
    resp=cmo.real_deleting("userCart",data)
    
    return resp,200




@publisher.route("/listContent",methods=["GET"])
@token_auth_check
def listContent(current_user):

    aggr=[
        {
            '$match': {
                'userId': current_user["uniqueId"]
            }
        },{
            '$addFields': {
                'uniqueId': {
                    '$toString':"$_id"
                }
            }
        },{
            '$project': {
                '_id': 0
            }
        }
    ]

    data_r=cmo.finding_aggregate("contents",aggr)

    return data_r,200



@publisher.route("/checkOuthistory",methods=["GET"])
def checkOuthistory():

    aggr=[
        {
            '$addFields': {
                'uniqueId': {
                    '$toString':"$_id"
                }
            }
        },{
            '$project': {
                '_id': 0
            }
        }
    ]

    data_r=cmo.finding_aggregate("checkOut",aggr)

    return data_r,200

@publisher.route("/pro_listContent",methods=["GET"])
@token_auth_check
def pro_listContent(current_user):

    aggr=[
        {
            '$match': {
                'userId': current_user["uniqueId"]
            }
        },{
            '$addFields': {
                'uniqueId': {
                    '$toString':"$_id"
                }
            }
        },{
            '$project': {
                '_id': 0
            }
        }
    ]

    data_r=cmo.finding_aggregate("contents",aggr)

    return data_r,200



@publisher.route("/getMyCart",methods=["GET"])
@token_auth_check
def getMyCart(current_user,ApiCall=None):

    aggr=[
        {
            '$match': {
                'userId': current_user["uniqueId"]
            }
        }, {
            '$addFields': {
                'productUniqueId': {
                    '$toObjectId': '$productUniqueId'
                }, 
                'userId': {
                    '$toObjectId': '$userId'
                }
            }
        }, {
            '$group': {
                '_id': '$productUniqueId', 
                'count': {
                    '$sum': 1
                }, 
                'productUniqueId': {
                    '$first': '$productUniqueId'
                }
            }
        }, {
            '$lookup': {
                'from': 'contents', 
                'localField': 'productUniqueId', 
                'foreignField': '_id', 
                'as': 'result'
            }
        }, {
            '$unwind': {
                'path': '$result', 
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$addFields': {
                'result.count': '$count', 
                'result.price': {
                    '$toInt': '$result.price'
                }, 
                'result.uniqueId': {
                    '$toString': '$productUniqueId'
                }
            }
        }, {
            '$addFields': {
                'result.totalSum': {
                    '$multiply': [
                        '$result.price', '$result.count'
                    ]
                }
            }
        }, {
            '$replaceRoot': {
                'newRoot': '$result'
            }
        }, {
            '$facet': {
                'totalPrice': [
                    {
                        '$group': {
                            '_id': None, 
                            'totalSum': {
                                '$sum': '$totalSum'
                            }
                        }
                    }
                ], 
                'result': [
                    {
                        '$addFields': {
                            'result': '$result'
                        }
                    },{
                        '$project': {
                            '_id': 0
                        }
                    }
                ]
            }
        }
    ]
    
    print(aggr)
    data_r=cmo.finding_aggregate("userCart",aggr)
    data_r["data"]=data_r["data"][0]
    
    
    data_r["data"]["totalSum"]=data_r["data"]["totalPrice"][0]["totalSum"] if len(data_r["data"]["totalPrice"])>0 else 0
    data_r["data"]["tax"]=10
    data_r["data"]["addOns"]=2000 if data_r["data"]["totalSum"] != 0 else 0
    data_r["data"]["tax_price"]=data_r["data"]["totalSum"]/data_r["data"]["tax"]
    data_r["data"]["totalPrice"]=data_r["data"]["totalSum"]+data_r["data"]["tax_price"] +data_r["data"]["addOns"]
    
    if(ApiCall!=None):
        return data_r
    return data_r,200





@publisher.route("/getHistroy",methods=["GET"])
def getHistroy():

    aggr=[
        {
            '$project': {
                '_id': 0
            }
        }
    ]

    data_r=cmo.finding_aggregate("contents",aggr)

    return data_r,200


@publisher.route("/addTOCart",methods=["POST"])
@token_auth_check
def addTOCart(current_user):
    
    print(current_user["uniqueId"],"current_usercurrent_user")

    data=request.get_json()
    data["userId"]=current_user["uniqueId"]
    print(data)
    
    dtq=cmo.insertion("userCart",data)
    
    dtq["msg"]="Product Add to Cart Successfully"
    
    return dtq,201
