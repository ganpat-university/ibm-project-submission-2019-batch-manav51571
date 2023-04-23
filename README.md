Crime Prediction System

Our crime prediction project utilizes machine learning algorithms to analyze and interpret patterns in crime data, enabling us to accurately predict potential crime hotspots. This tool empowers law enforcement agencies to take proactive measures and implement targeted strategies to prevent crimes before they occur, ultimately creating safer communities.

Built With
Python,
Flask,
HTML,
CSS,
JavaScript

Make sure that you have the following:
Python 3.10 or higher and pip (which comes with Python 3+),flask,An environment to work in - something like Jupyter or Spyder

To clone the repo :

git clone https://github.com/ganpat-university/ibm-project-submission-2019-batch-manav51571

Install Python packages :

pip install -r requirements.txt

Run App File:

python app.py

To Add SSL Certificate :

1)Download OpenSSL from https://thesecmaster.com/procedure-to-install-openssl-on-the-windows-platform/

2)Run the following command to generate the SSL certificate :
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

This command will generate a self-signed SSL certificate with a validity of 365 days.
Copy the `cert.pem` and `key.pem` files to the directory where your Flask application is located.

3)Add this code to your app.py file :
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert.pem', 'key.pem')
app.run(ssl_context=context)

This will configure your Flask application to use the SSL certificate when running.
Now your application should now be accessible over HTTPS on port 443.

Security Features :

Cross-Site Request Forgery,
Cookies Protection,
Talisman - Provide Web Security,
Proper HTTP headers and 
Input validation on Backend and Frontend for XSS attack   
