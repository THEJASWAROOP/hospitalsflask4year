from flask import Flask, render_template,url_for, request, redirect, flash, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
from flask_mail import Mail, Message
import csv
import flask_excel as excel,jsonify,io

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'ht74tyuggjhjguyu'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'healthcaresystem365@gmail.com'
app.config['MAIL_PASSWORD'] = 'h147258369s'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

docs=UploadSet('docs', tuple('csv'.split()))
app.config['UPLOADED_DOCS_DEST']='static/upload_csv'
configure_uploads(app, docs)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST']='static/upload_files'
configure_uploads(app, photos)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Disease,Sub_disease , Signup,Ayurvedic,Sub_ayurvedic,MedicinesInventoryList, Contact
# Sub_ayurvedic
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
#from database_searchmedicine import medicalstore,medicine, Signup

engine=create_engine("sqlite:///doc.db",
					  connect_args={'check_same_thread':False},
					  echo=True)

# engine1=create_engine("sqlite:///medi.db",
# 					  connect_args={'check_same_thread':False},
# 					  echo=True)

Base.metadata.bind=engine

DBSession=sessionmaker(bind=engine)
session=DBSession()


@app.route('/')
@app.route('/main')
def main():
  return render_template('main.html')

@app.route("/posts")
def myposts():	
	return render_template("sample.html",posts=posts)

@app.route("/about")
def About():	
	return render_template("about.html")


@app.route("/help")
def Help():	
	return render_template("help.html")



@app.route("/hospital")
def Hospital():	
	return render_template("searchhos.html")



@app.route("/search", methods=["GET", "POST"])
def Search():
	if request.method =="POST":
		medicine = session.query(MedicinesInventoryList).filter_by(drugname=request.form['drugName']).all()
		return render_template("search.html", medicines=medicine)
	else:
		return render_template("search.html")


@app.route("/hos", methods=["GET", "POST"])
def hos():
	if request.method =="POST":
		medicine = session.query(MedicinesInventoryList).filter_by(drugname=request.form['drugName']).all()
		return render_template("searchhos.html", medicines=medicine)
	else:
		return render_template("searchhos.html")



@app.route("/contacta")
def Contacta():
	return render_template("contact.html")

@app.route('/profile', methods=["GET","POST"])
@login_required
def profileInfo():
	if request.method == "POST":
		myProfile = session.query(Signup).filter_by(id=request.form['profileId']).one()
		if 'photo' in request.files:
			filename = photos.save(request.files['photo'])
			
			myProfile.image = filename 
			myProfile.name = request.form['name']
			myProfile.email = request.form['email']
			myProfile.mobile = request.form['mobile']
			session.commit()
			return redirect('/profile')
		else:
			myProfile.name = request.form['name']			
			myProfile.email = request.form['email']
			myProfile.mobile = request.form['mobile']
			session.commit()
			return redirect('/addmultiple')
		return redirect('/profile')
	elif current_user.name:
		return render_template('profile.html')
	else:
		return redirect(url_for('home'))
	return render_template('home.html')


# @app.route("/upload", methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         myProfile = session.query(MedicinesInventoryList).filter_by(id=request.form['profileId']).one()
    # return render_template('profile.html')
    # <!doctype html>
    # <title>Upload an excel file</title>
    # <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    # <form action="" method=post enctype=multipart/form-data><p>
    # <input type=file name=file><input type=submit value=Upload>
    # </form>
    # '''


@app.route('/addmultiple', methods=["GET","POST"])
def addmultiple():
	if request.method =="POST":	
		try:
			if request.method =="POST" and 'data_file' in request.files:
				#print('--------------------CSV')
				filename=docs.save(request.files['data_file'])
				with open("static/upload_csv/"+filename) as csvfile:
					reader = csv.DictReader(csvfile)				
					for row in reader:
						#print("----------",row['dosage'],row['Form'],row['lat'],row['lon'],row['signup_id'])
						inventorys = MedicinesInventoryList(drugname=row['DrugName'],
							dosage=row['dosage'], form=row['Form'], 
							lat=request.form['lat'],
		   	                lon=request.form['lon'],
	
							# lat=row['lat'], lon=row['lon'],
							 signup_id=row['signupId'])
						session.add(inventorys)
						session.commit()
				flash("stored safely","success")
				return redirect('/profile')
			else:
				return render_template('upload.html')
		except Exception as e:
			flash('Only CSV Format is Accepted for Uploads','warning')
			return render_template('upload.html')
	else:
		return render_template('upload.html')
	
# @app.route('/store', methods=["POST"])
# def MedicinesInventoryList():



@app.route("/diseases")	
def showDiseases():
	disease = session.query(Disease).all()
	return render_template("disease.html",myres=disease)

@app.route("/ayurvedic")	
def showAyurvedic():
	ayurvedic = session.query(Ayurvedic).all()
	return render_template("ayurvedic.html",myayu=ayurvedic)



@app.route("/signup",methods=["GET","POST"])	
def signup():
	if request.method == "POST":
		filename = photos.save(request.files['file1'])
		saveData = Signup(name=request.form['usr'],
			               email=request.form['email'],
			               lat=request.form['lat'],
			               lon=request.form['lon'],
			               image= filename,
			               mobile=request.form['tel'],
			               creatpassword=request.form['pwd1'],
			               conformpassword=request.form['pwd2'])

		print(request.form['usr'],request.form['email'], request.form['lat'],request.form['lon'],filename, request.form['tel'],request.form['pwd1'],request.form['pwd2'])

		session.add(saveData)
		session.commit()
		return redirect('/login')
	else:
		#mySignup = session.query(Signup).all()
		return render_template("signup.html")





@app.route("/contact",methods=["GET","POST"])	
def contacts():
	if request.method == "POST":
		f = Contact(name=request.form['name'],
					email=request.form['email'],
					comments=request.form['comments'])
		#print(request.form['name'],request.form['email'], request.form['comments'])

		session.add(f)
		session.commit()
		flash("feedback send successfully:")
		return redirect('/main')
	else:
		return render_template("home.html")




@app.route("/menus/<int:disease_id>", methods=["GET"])	
def showMenus(disease_id):
	item = session.query(Sub_disease).filter_by(disease_id=disease_id)
	return render_template("Sub_disease.html",menu=item)



@app.route("/menu/<int:ayurvedic_id>", methods=["GET"])	
def showMenu(ayurvedic_id):
	item = session.query(Sub_ayurvedic).filter_by(ayurvedic_id=ayurvedic_id)
	return render_template("Sub_ayurvedic.html",men=item)


# @app.route('/addrestaurants', methods=["GET","POST"])
# def addrestaurant():
# 	if request.method == "POST" and 'docs'in request.files:
# 		filename = docs.save(request.files['docs'])
# 		restaurants = Restaurant(name=request.form['name'],image=filename)
# 		session.add(restaurants)
# 		session.commit()
# 		flash("New Restaurant Created:")
# 		return redirect('/restaurants')
# 	else:
# 		return render_template("addrestaurant.html")


@app.route('/adddisease', methods=["GET","POST"])
def adddisease():
	if request.method == "POST":
		filename = photos.save(request.files['photo'])
		diseases = Disease(name=request.form['name'],image=filename)
		session.add(diseases)
		session.commit()
		flash("New Disease Created:")
		return redirect('/diseases')
	else:
		return render_template("adddisease.html")

@app.route('/addayurvedic', methods=["GET","POST"])
def addayurvedic():
	if request.method == "POST":
		filename = photos.save(request.files['photo'])
		ayurvedics = Ayurvedic(name=request.form['name'],image=filename)
		session.add(ayurvedics)
		session.commit()
		flash("New Disease Created:")
		return redirect('/ayurvedic')
	else:
		return render_template("addayurvedic.html")







# @app.route('/medicalstore', methods=["GET","POST"])
# def medicalstore():
# 	if request.method == "POST":
# 		filename = photos.save(request.files['photo'])
# 		store = store(name=request.form['name'],image=filename)
# 		session.add(store)
# 		session.commit()
# 		flash("New medicalstore add:")
# 		return redirect('/diseases')
# 	else:
# 		return render_template("signup.html")



@app.route('/editdisease/<int:t_id>', methods=["GET","POST"])
def editdisease(t_id):
	if request.method == "POST":
		editdisease =session.query(Disease).filter_by(id=t_id).one()
		editdisease.name= request.form['name']
		filename = photos.save(request.files['photo'])
		editdisease.image= filename
		session.commit()
		return redirect('/diseases')
	else:
		editdisease=session.query(Disease).filter_by(id=t_id).one()
		return render_template("editdisease.html", editdisease=editdisease)


@app.route('/editayurvedic/<int:s_id>', methods=["GET","POST"])
def editayurvedic(s_id):
	if request.method == "POST":
		editayurvedic =session.query(Ayurvedic).filter_by(id=s_id).one()
		editayurvedic.name= request.form['name']
		filename = photos.save(request.files['photo'])
		editayurvedic.image= filename
		session.commit()
		return redirect('/ayurvedic')
	else:
		editayurvedic=session.query(Ayurvedic).filter_by(id=s_id).one()
		return render_template("editayurvedic.html", editayurvedic=editayurvedic)


@app.route('/del_ayurvedic/<int:s_id>', methods=["GET"])
def deleteayurvedic(t_id):
	deleteayurvedic=session.query(Ayurvedic).filter_by(id=s_id)
	deleteayurvedic.delete()
	session.commit()
	try:
		imagePath='./static/upload_files/'+delFolderImage.image
		os.remove(imagePath)
	except Exception as e:
		return redirect('/ayurvedic')
	flash("Deleted Disease","info")
	return redirect('/ayurvedic')




@app.route('/confirmDel_disease/<int:disease_id>', methods=["GET"])
def confirmDeleteDisease(t_id):
	deletedisease = session.query(Disease).filter_by(id=disease_id).one()
	return render_template("deletedisease.html",deletedisease=deletedisease)




@app.route('/del_disease/<int:t_id>', methods=["GET"])
def deletedisease(t_id):
	deletedisease=session.query(Disease).filter_by(id=t_id)
	deletedisease.delete()
	session.commit()
	try:
		imagePath='./static/upload_files/'+delFolderImage.image
		os.remove(imagePath)
	except Exception as e:
		return redirect('/diseases')
	flash("Deleted Disease","info")
	return redirect('/diseases')




@app.route('/displaySub_disease/<int:t_id>', methods=["GET"])
def Diseasemenuitems(t_id):
		displayMenu=session.query(Sub_disease).filter_by(disease_id=t_id)
		return render_template("displaySub_disease.html", items=displayMenu)

@app.route('/displaySub_ayurvedic/<int:s_id>', methods=["GET"])
def ayurvedicmenuitems(s_id):
		displayMenu=session.query(Sub_ayurvedic).filter_by(ayurvedic_id=s_id)
		return render_template("displaySub_ayurvedic.html", items=displayMenu)


@app.route('/login',methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	try:
		if request.method == "POST":
			emp = session.query(Signup).filter_by(email=request.form['email'],creatpassword=request.form['password']).first()			
			if emp:
				login_user(emp)
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('main'))
			else:
				flash("Login Failed, Please Check & Try Again ...!","danger")
				return render_template("login.html", title="Login")
		else:
			return render_template("login.html", title="Login")
		
	except Exception as e:
		flash("Login Failed, Please Check & Try Again ...!","danger")
		return render_template("login.html", title="Login")
	else:
		return render_template("login.html", title="Login")


@app.route("/verifyEmail", methods=["GET","POST"])
def emailVerify():
	try:	
		if request.method == "POST":
			person = session.query(Signup).filter_by(email= request.form['emailSend']).first()
					
			if person:		
				print('------------ABC--------------',request.form['emailSend'])
				data = ''
				data += 'Welcome To Sharing Hands, Caring Hearts Portal  : <br>'
				data += 'Your Username : <h3>' + person.email + '</h3>'
				data += 'Your Password : <h3>' + person.creatpassword + '</h3>'					
				print(data)
				msg = Message('Hello', sender = 'healthcaresystem365@gmail.com', recipients = [request.form['emailSend']])
				print(msg)
				msg.body = data
				msg.html =msg.body
				mail.send(msg)
				flash("Email Sent Successfully...!","info")
				return render_template('login.html')
			else:
				flash("No One Exists with " + request.form['emailSend'] + "...!","warning")
				return render_template('login.html')
		else:
			return render_template('login.html')
	except Exception as e:
		flash("No One Exists with " + request.form['emailSend'] + "...!","danger")
		return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main'))
  


if __name__ == '__main__':
	app.config['SECRET_KEY'] = 'e7a9804ba98684deefd88d6a6c8cd0db'
	login_manager = LoginManager(app)
	login_manager.login_view = 'login'
	login_manager.login_message_category = 'info'

	@login_manager.user_loader
	def load_user(user_id):
		return session.query(Signup).get(int(user_id))
	app.debug = True
	app.run(host = '0.0.0.0', port =7000)		

  


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port =7000)



#InventorList
# f = request.files['data_file']
#     # if not f:
#     #     return "No file"

#     # stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
#     # csv_input = csv.reader(stream)
#     # #print("file contents: ", file_contents)
#     # #print(type(file_contents))
#     # print(csv_input)
#     # for row in list(csv_input)[1:]:
#     # 	print(row)
#     # 	student=MedicinesInventoryList(drugid=row[0],

#     # 						drugname=row[1],
#     # 						dosage=row[2],
#     # 						 form=row[3],
#     # 						lat=row[4],
#     # 						lon=row[5],
#     # 						signup_id=row[6]
#     # 						)
#     # 	session.add(student)
#     # session.commit()