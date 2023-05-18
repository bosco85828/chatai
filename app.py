from flask import Flask, render_template, request, jsonify
import json
import jsonlines

app = Flask(__name__)

@app.route("/pushprompts",methods=['POST'])
def push_prompts():
    try:data=request.get_json()
    except Exception as err  : 
        print(err)
        return jsonify({'status':'fail','message':'Please provide the prompts.'}) , 400

    if not data : 
        return jsonify({'status':'fail','message':'Please provide the prompts.'}) , 400

    try : 
        prompts=data['prompts']
        for prompt in prompts : 
                prompt['prompt'] = prompt['prompt'] + " ->"
                prompt['completion'] = f" {prompt['completion']} END"

    except TypeError : 
        return jsonify({'status':'fail','message':'Please provide prompts with json type.'}) , 400
    
    except Exception as err :
        return jsonify({'status':'fail','message':err}) , 400

    try : 
        with jsonlines.open('data.jsonl', mode='a') as writer:
            writer.write_all(prompts)

        return jsonify({'status':'success','message':''}) , 200
    
    except Exception as err : 
        return jsonify({'status':'fail','message':err}) , 500     

    
    
if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
