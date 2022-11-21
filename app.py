from flask import Flask,request

import os

from flask_cors import CORS

from flask import jsonify



app = Flask("DockerJS")

CORS(app)

@app.route('/')

def home():

 return jsonify({"status":"Hello World...!"})



@app.route('/images')

def images():

 return jsonify({"status":"This will show all information about Docker Images and manage them."})



@app.route('/launch')

def launch():

 return jsonify({"status":"This will help you to manage docker containers and launch them."})



@app.route('/delete')

def delete():

 return jsonify({"status":"This will help you to stop or delete containers...!"})



@app.route('/containers')

def containers():

 return jsonify({"status":"This will help you to get details about containers...!"})



@app.route('/expose')

def expose():

 return jsonify({"status":"This will help you to expose container to outside port...!"})



@app.route('/inspect')

def inspect():

 return jsonify({"status":"This will help you to find ip of host if any container exposed to host port...!"})





################# IMAGES ROUTES ######################

@app.route('/showimages')

def textdata():

 os.system('docker images |  awk \'{print $1,$2}\' > images.txt' )

 b=open('./images.txt','r')

 a=b.read()

 return jsonify({"status":a})



@app.route('/pullimage',methods=["POST"])

def pullimage():

 val = request.json

 #val = jsonify(val)

 if('image_name' in val.keys()):

  #print(val['hello']=="")

  print("Image name = {} ".format(val['image_name']))

  os.system("docker pull {} > images.txt".format(val['image_name']))

 else:

  os.system(r"echo \"No Image Name\" &> images.txt")

 b=open('./images.txt','r')

 a=b.read()

 if(len(a)==0 or len(a)==26):

  return jsonify({"status":"Invalid Image Name..!"})

 else:

  return jsonify({"status":"Image downloaded successfully...!"})



@app.route('/deleteimage',methods=["POST"])

def deleteimage():

 val = request.json     

 #val = jsonify(val)

 if('image_name' in val.keys()):

  #print(val['hello']=="")

  print("Image name = {} ".format(val['image_name']))

  return_code=os.system("docker image rm {}".format(val['image_name']))

  if(return_code==0):

   return jsonify({"status":"Deleted Imaged {}...!".format(val['image_name'])})

  else: 

   return jsonify({"status":"Image not exists or any container might be using this image...!"})



############################ IMAGE ROUTES ##########################################





########################### INSPECT CONTAINERS ####################################



@app.route('/inspectcontainer',methods=["POST"])

def inspectcontainer():

 val = request.json

 if('container_name' in val.keys()):

  print("Container name = {}".format(val['container_name']))

  return_code = os.system("docker inspect {}".format(val['container_name']))

  if(return_code==0):

   os.system("docker inspect {} > images.txt".format(val['container_name']))

   b=open('images.txt','r')

   a=b.read()

   return jsonify({"status":a})

  else:

   return jsonify({"status":"No Container or Invalid Container Name Given...!"})

 else:

  return jsonify({"status":"Invalid Container Name Given...!"})

######################### INSPECT CONTAINERS #######################################

######################### DELETE ALL CONTAINERS ########################################

@app.route('/deleteall')

def deleteall():

 os.system("docker rm -f $(docker ps -qa)")

 return jsonify({"status":"All containers are deleted...!"})

######################### DELETE ALL CONATINERS #########################################



######################### STOP CONTAINER ################################################



@app.route('/stopcontainer',methods=["POST"])

def stopcontainer():

 val = request.json

 #val = jsonify(val)

 if('container_name' in val.keys()):

  #print(val['hello']=="")

  print("Container name = {} ".format(val['container_name']))

  a=os.system("docker stop {} ".format(val['container_name']))

  if(a==0):

   return jsonify({"status":"Container stopped successfully...!"})

  else:

   return jsonify({"status":"Container doesn't exists...!"})

 else:

  return jsonify({"status":"Invalid Container...!"})



######################## STOP CONTAINER ###############################################

######################### DELETE CONTAINER ############################################

@app.route('/deletecontainer',methods=["POST"])

def deletecontainer():

 val = request.json

 if('container_name' in val.keys()):

  os.system("docker rm -f {} > images.txt".format(val['container_name']))

  b=open('images.txt','r')

  a=b.read()

  if(len(a)==0):

   return jsonify({"status":"No container with the given name..!"})

  else:

   

   return jsonify({"status":"Container deleted...!"})

 else:

  return jsonify({"status":"Invalid Container Name...!"})

######################## DELETE CONTAINER ############################################

@app.route('/showcontainers')

def showcontainers():

 os.system("docker ps -a > images.txt")

 b=open('images.txt','r')

 a=b.read()

 return jsonify({"status":a})



@app.route('/showc',methods=["POST","GET"])

def showc():

 val=request.json

 if('container_name' in val.keys()):

  os.system('docker ps -a | grep {} > images.txt'.format(val['container_name']))

  b=open('images.txt','r')

  a=b.read()

  if(len(a)==0):

   return jsonify({"status":"No container found with this name...!"})

  else:

   return jsonify({"status":a})

 else:

  return jsonify({"status":"Invalid container name...!"})







##################### LOGS OF A CONTAINER



@app.route('/viewlogs',methods=["POST"])

def viewlogs():

 val = request.json

 if('container_name' in val.keys()):

  a=os.system("docker logs {}".format(val['container_name']))

  if(a==0):

   os.system("docker logs {} > images.txt".format(val['container_name']))

   a=open('images.txt','r')

   b=a.read()

   return jsonify({"status":b})

  else:

   return jsonify({"status":"No container found...!"})

 else:

  return jsonify({"status":"Invalid Container Name...!"})





####################### LAUNCH CONTAINER ######################33



@app.route('/launchc',methods=["POST"])

def launchc():

 val=request.json

 print(val['container_name'])

 print(len(val['container_name']))

 if(len(val['container_name'])!=0):

  ret = os.system('docker ps -a | grep {}'.format(val['container_name']))

  if(ret==0):

   return jsonify({"status":"Container with the given name already exists..."})

  else:

   if(len(val['image_name'])!=0):

    rc = os.system('docker images | grep {}'.format(val['image_name']))

    if(rc==0):

     if(len(val['host_port'])!=0 and len(val['container_port'])!=0):

      os.system('docker run -dit --name {} -p {}:{} {} > run.txt'.format(val['container_name'],val['host_port'],val['container_port'],val['image_name']))

      b=open('run.txt','r')

      a=b.read()

      return jsonify({"status":a})

     else:

      os.system('docker run -dit --name {} {} > run.txt'.format(val['container_name'],val['image_name']))

      b=open('run.txt','r')

      a=b.read()

      return jsonify({"status":a})

    else:

     return jsonify({"status":"Download Image first...!"})

   else:

    return jsonify({"status":"Invalid Image Name given...!"})

 else:

  return jsonify({"status":"Invalid Container Name given...!"})