from flask import Flask, request, render_template,url_for
from flask_cors import cross_origin
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pyodbc

connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-R099RR8Q;'
                      'Database=crime;'
                      'Trusted_Connection=yes;');

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/datareport", methods = ["GET", "POST"])
@cross_origin()
def data():
    option = request.form['exampleRadios']

    if option == 'optn1':
        data = pd.read_sql("SELECT * FROM police_station", connection)
        result=data.to_html()

    elif option == 'optn2':
        data = pd.read_sql("SELECT * FROM ipc", connection)
        result=data.to_html()

    elif option == 'optn3':
        data = pd.read_sql("SELECT * FROM police_officer", connection)
        result=data.to_html()
        sns.barplot(x='p_name',y='number_of_cases_solved',data=data, palette="rocket")
        plt.xlabel('Police Station')
        plt.ylabel('Number of Cases Solved')
        plt.title('Police Station v/s Number of Cases Solved' )
        plt.savefig('static/images/police__officer.jpg')
        result=append_html(result,['images/police__officer.jpg'])
        
    elif option == 'optn4':
        data = pd.read_sql("SELECT * FROM fir", connection)
        result=data.to_html()

    elif option == 'optn5':
        data = pd.read_sql("SELECT * FROM casesz", connection)
        result=data.to_html()

    elif option == 'optn6':
        data = pd.read_sql("SELECT * FROM victim", connection)
        result=data.to_html()

    elif option == 'optn7':
        data = pd.read_sql("SELECT * FROM criminal", connection)
        result=data.to_html()

    elif option == 'optn8':
        v1= request.form['Insert_PS_v1']
        v2= request.form['Insert_PS_v2']
        v3= request.form['Insert_PS_v3']
        v4= request.form['Insert_PS_v4']
        record=[v1,v2,v3,v4]
        cursor=connection.cursor()
        insrt="INSERT INTO police_station VALUES(?,?,?,?)"
        cursor.execute(insrt,record)
        data = pd.read_sql("SELECT * FROM police_station", connection)
        result=data.to_html()

    elif option == 'optn9':
        v1= request.form['Delete_criminal']
        cursor=connection.cursor()
        dele="DELETE FROM criminal where c_id=?"
        cursor.execute(dele,v1)
        data = pd.read_sql("SELECT * FROM criminal", connection)
        result=data.to_html()

    elif option == 'optn10':
        v1= request.form['Update_fir1']
        v2= request.form['Update_fir2']
        record=[v2,v1]
        cursor=connection.cursor()
        update="UPDATE fir SET complainant_name=? WHERE fir_no=?"
        cursor.execute(update,record)
        data = pd.read_sql("SELECT * FROM fir", connection)
        result=data.to_html()
    else:
        result="PLEASE SELECT AN OPTION!!"
    return result

def append_html(result,image_names):
    for i in image_names:
        result=result+"<img src=\"{{url_for('static',filename="+i+")}}\">"
        return result

if __name__ == "__main__":
    app.run(debug=True)

