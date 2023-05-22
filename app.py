from flask import Flask, render_template, request, jsonify
import json
import jsonlines
from query import generate_text,load_from_txt
import os 
from datetime import datetime


app = Flask(__name__)
path= os.getcwd()
@app.route("/pushprompts",methods=['POST'])
def push_prompts():
    try:data=request.get_json()
    except Exception as err  : 
        print(err)
        return jsonify({'status':'fail','message':'Please provide the prompts.'}) , 400

    if not data : 
        return jsonify({'status':'fail','message':'Please provide the prompts.'}) , 400

    try : 
        file_list=[]
        prompts=data['prompts']
        for prompt in prompts : 
                now=datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
                try : 
                    with open(f"{path}/{now}.txt",'a+') as f : 
                        f.write(prompt['prompt'] + '\n')
                        f.write(prompt['completion'] + '\n')

                    file_list.append(f"{path}/{now}.txt")
                except Exception as err : 
                    print(err)

    except TypeError as err :
        print(err) 
        return jsonify({'status':'fail','message':'Please provide prompts with json type.'}) , 400
    
    except Exception as err :
        return jsonify({'status':'fail','message':err}) , 400

    try : 
        load_from_txt()
        return jsonify({'status':'success','message':""}) , 200
    
    except Exception as err : 
        print(err)
        return jsonify({'status':'fail','message':str(err)}) , 500

    finally:
        for file in file_list: 
            os.remove(file)
     

@app.route("/query",methods=['POST'])
def query():
    try:data=request.get_json()
    except Exception as err : 
        print(err)
        return jsonify({'status':'fail','message':'Please provide the prompt.'}) , 400
    
    if not data : 
        return jsonify({'status':'fail','message':'Please provide the prompt.'}) , 400
    
    try:
        prompt=data['prompt']
        anser=generate_text(prompt)
        print(anser)
        return jsonify({'status':'success','message': anser }) , 200
    
    except KeyError:
        return jsonify({'status':'fail','message':'Please provide prompt with json type.'}) , 400

    except TypeError : 
        return jsonify({'status':'fail','message':'Please provide prompt with json type.'}) , 400
    
    except Exception as err :
        return jsonify({'status':'fail','message':err}) , 400

    
if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
