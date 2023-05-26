from flask import Flask, render_template, request, jsonify
import json
import jsonlines
from query import generate_text,load_from_txt
import os 
from dotenv import load_dotenv
from datetime import datetime
from tgbot import send_msg

load_dotenv()

key_dict={
    'JLB':os.getenv('JLB_OPENAI_API_KEY'),
    'ETY':os.getenv('ETY_OPENAI_API_KEY')
}

app = Flask(__name__)
path= os.getcwd()

@app.route("/pushprompts",methods=['POST'])
def push_prompts():
    try:
        data=request.get_json()
    except Exception as err  : 
        return jsonify({'status':'fail','message':str(err)}) , 400

    if not data : 
        return jsonify({'status':'fail','message':'Please provide the prompts.'}) , 400

    try : 
        file_list=[]
        prompts=data['prompts']
        merchant=data['merchant'].upper() 
        if merchant in key_dict : 
            os.environ['OPENAI_API_KEY']=key_dict[merchant]

        try : 
            os.mkdir(f"{path}/{merchant}-rawdata")
        except FileExistsError: pass 

        for prompt in prompts : 
                now=datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
                
                with open(f"{path}/{merchant}-rawdata/{now}.txt",'a+') as f : 
                    f.write(prompt['prompt'] + '\n')
                    f.write(prompt['completion'] + '\n')

                
                file_list.append(f"{path}/{merchant}-rawdata/{now}.txt")
                

    except KeyError as err :
        return jsonify({'status':'fail','message':f'Please provide the {str(err)}'}) , 400
    
    except TypeError as err :
        print(err) 
        return jsonify({'status':'fail','message':'Please provide prompts with json type.'}) , 400
    
    except Exception as err :
        return jsonify({'status':'fail','message':str(err)}) , 500

    try :
        load_from_txt(merchant)
        return jsonify({'status':'success','message':""}) , 200

    except Exception as err : 
        return jsonify({'status':'fail','message':str(err)}) , 500

    finally:
        try : 
            for file in file_list: 
                os.remove(file)
        except Exception as err : 
            pass
     

@app.route("/query",methods=['POST'])
def query():
    try:
        data=request.get_json()

    except Exception as err : 
        return jsonify({'status':'fail','message':'Please provide the prompt.'}) , 400
    
    if not data : 
        return jsonify({'status':'fail','message':'Please provide the prompt.'}) , 400
    
    try:
        prompt=data['prompt']
        merchant=data['merchant'].upper()
        if merchant in key_dict : 
            os.environ['OPENAI_API_KEY']=key_dict[merchant]
            
        anser=generate_text(prompt,merchant)
        print(anser)
        return jsonify({'status':'success','message': anser }) , 200
    
    except KeyError as err :
        return jsonify({'status':'fail','message':f'Please provide the {str(err)}'}) , 400

    except TypeError as err : 
        return jsonify({'status':'fail','message':str(err)}) , 400
    
    except Exception as err :
        return jsonify({'status':'fail','message':str(err)}) , 400

    
if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
