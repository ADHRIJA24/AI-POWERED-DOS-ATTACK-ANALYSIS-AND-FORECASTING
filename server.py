# from flask import *
# from database import *
# import requests
# import os

# api = Flask(__name__) 


# ipp="192.168.1.32:5001"
# ip="192.168.1.32:5000"

# BLOCKED_IPS_FILE = 'blocked_ips.txt'


# # @api.route('/')

# # def home():
    
# #     return render_template('home.html')

# @api.route('/')
# def home():
#     # Get the user's IP address
#     user_ip = request.remote_addr
    
#     # Check if the IP is in the blocked_ips.txt file
#     if os.path.exists(BLOCKED_IPS_FILE):
#         with open(BLOCKED_IPS_FILE, 'r') as file:
#             blocked_ips = file.read().splitlines()  # Read all lines into a list
#             print("blocked_ips : ",blocked_ips)
#             for iipp in blocked_ips:
#                 print("iipp : ",iipp)
#                 if iipp==ip:
#                     print("*"*50)
#                     return redirect(url_for('block'))
#                 # else:
#                 #     print("#"*100)
#                 #     return redirect(url_for('home'))
#             # if user_ip in blocked_ips:
#             #     print("*"*50)
#             #     # Redirect to the block page if the IP is blocked
#             #     return redirect(url_for('block'))
    
#     # If the IP is not blocked, render the home page
#     return render_template('home.html')


#     # q="select * from blocked where ipaddress='%s' "%(ip)
#     # res=select(q)
#     # if res :
#     #     return render_template('blocked.html')

#     # else:    
#     #     flag=0
#     #     return render_template('home.html')
    


# @api.route('/block')

# def block():
   
#     return render_template('blocked.html')
    


# @api.route('/checkss')
# def checkss():
#     try:
#         # Sending an HTTP GET request to app1 with a query string parameter 'name'
#         response = requests.get(f'http://'+ipp+'/requests?ip='+ip)
#         if response.status_code == 200:
#             data = response.json()
#             print(data['message'])
#             if data['message'] == "blocked":
#                 # Save the blocked IP address to a text file
#                 with open('blocked_ips.txt', 'a') as file:
#                     file.write(ip + '\n')
                
#                 # Send a flag indicating that the user is blocked
#                 return """<script>alert('Your IP Is Blocked By User');window.location='/block'</script>"""
#             else:
#                 return redirect(url_for("checkss"))
#         else:
#             return jsonify({"error": "Failed to fetch data from app1"}), 500
#     except requests.RequestException as e:
#         return jsonify({"error": str(e)})
    


# @api.route('/s_login', methods=['GET'])
# def s_login():
#     # Redirect the user to the client-side login page
#     return redirect(f'http://{ipp}/s_log')





# api.run(debug=True,host="192.168.1.32",port=5000)






from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__)

# Configuration

IPP = "192.168.91.224:5000"  # First app's address
IP = "192.168.91.224:5008"        # This app's IP (port omitted for requests)
BLOCKED_IPS_FILE = 'blocked_ips.txt'

@app.route('/')
def home():
    user_ip = request.remote_addr
    if os.path.exists(BLOCKED_IPS_FILE):
        with open(BLOCKED_IPS_FILE, 'r') as file:
            blocked_ips = file.read().splitlines()
            print("blocked_ips:", blocked_ips)
            if IP in blocked_ips:
                print("*" * 50)
                return redirect(url_for('block'))
    return render_template('home.html')

@app.route('/block')
def block():
    return render_template('blocked.html')

@app.route('/checkss')
def checkss():
    try:
        response = requests.get(f'http://{IPP}/requests?ip={IP}')
        if response.status_code == 200:
            data = response.json()
            print(data['message'])
            if data['message'] == "blocked":
                with open(BLOCKED_IPS_FILE, 'a') as file:
                    file.write(IP + '\n')
                return """<script>alert('Your IP Is Blocked (DOS Attack Detected)');window.location='/block'</script>"""
            else:
                return redirect(url_for("checkss"))
        else:
            return jsonify({"error": "Failed to fetch data from server"}), 5000
    except requests.RequestException as e:
        return jsonify({"error": str(e)})

@app.route('/s_login', methods=['GET', 'POST'])
def s_login():
    return redirect(f'http://{IPP}/s_log')



@app.route('/s_home', methods=['GET', 'POST'])
def s_home():
    return redirect(f'http://{IPP}/s_home')

if __name__ == "__main__":
    app.run(debug=True, host="192.168.91.224", port=5008)