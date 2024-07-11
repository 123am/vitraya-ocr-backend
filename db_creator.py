from base import *

if(os.environ.get("DB_HOST") and os.environ.get("DB_PORT")):
    
    for i in ["Publisher","Subscriber"]:
        cmo.insertion("userRole",{"userRole":i})
        
