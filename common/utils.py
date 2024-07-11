from base import *

def time_stamp():
    time_staing=str(datetime.timestamp(datetime.now()))
    time_staing=time_staing.replace(".","")
    return time_staing

def file_name(filee):
    print(filee,"fileefilee")
    fileNameExt=filee.filename.split(".")[-1]
    fileName=".".join(filee.filename.split(".")[0:-1])
    file_final_name=fileName+"_fp_"+time_stamp()+"."+fileNameExt
    return file_final_name

def form_to_json(req_form):
    json_data={}
    
    for i in req_form:
        json_data[i]=req_form.get(i)
        
    return json_data