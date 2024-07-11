from base import *

common=Blueprint("common",__name__)

@common.route("/uploads/<fname>",methods=["GET"])
def uploads_data(fname):
    
    return send_file(os.path.join(os.getcwd(),"uploads",fname))
