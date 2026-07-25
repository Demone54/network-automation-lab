from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        result = request.form.to_dict()
        name=result['instance_name']
        device=result['device']
        intf_number=result['intf_number']
        ip_add=result['ip_add']
        shut=result['shutdown']
        if shut == "yes":
            shut = 'null'
        else:
            shut = 'no'
        
        env=Environment(loader=FileSystemLoader('./templates'))
        
        template=env.get_template('service.j2')
        with open('./vars/service_instance.yaml', 'w') as f:
            f.write(template.render(name = name, device = device, intf_number = intf_number, ip_add = ip_add))
        
        template=env.get_template('targets.j2')
        with open('./tests/ping_targets.yaml', 'w') as f:
            f.write(template.render(ip_add = ip_add))
        
        template=env.get_template('R1_interface.j2')
        with open('./vars/R1.yaml', 'w') as f:
            f.write(template.render(shut = shut))

    
    return render_template('service.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
