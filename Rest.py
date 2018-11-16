from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy,orm
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.orm import joinedload
from datetime import datetime
from dateutil.parser import parse
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_basicauth import BasicAuth

import json




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'D8SD47'
app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'


db = SQLAlchemy(app)
ma = Marshmallow(app)
basic_auth = BasicAuth(app)
login_manager = LoginManager()
login_manager.init_app(app)
	



#______________________________________Classes para o BD _________________________

class SmartNested(fields.Nested):

    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return {'id': int(getattr(obj, attr + '_id'))}
        return super(SmartNested, self).serialize(attr, obj, accessor)

class Agendamento(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True)
    id_medico = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable = False)
    id_paciente = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable = False)
    cadastro = db.Column(db.String(20), nullable=False)
    inicio = db.Column(db.DateTime, nullable = False)
    fim = db.Column(db.DateTime,nullable = False)
    in_status = db.Column(db.Integer,nullable = False)
    voucher = db.Column(db.String(6))
    valor = db.Column(db.Float)
	



espec_med = db.Table('espec_med',
    db.Column('id_especialiade_medico',db.Integer, primary_key=True),
    db.Column('id_especialidade',db.Integer, db.ForeignKey('especialidade.id')),
    db.Column('id',db.Integer, db.ForeignKey('usuario.id'))
	)	
	
class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    tipo_id = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(15), nullable=False)
    nome = db.Column(db.String(60), nullable=False)
    dt_nascimento = db.Column(db.Date, nullable=False)
    
    especialidades = db.relationship('Especialidade', secondary=espec_med, backref=db.backref('especs', lazy='dynamic'))# Essa linha representa um relacionamento e não uma coluna explicação em https://www.youtube.com/watch?v=OvhoYbjtiKc
    lugares = db.relationship('Lugar', backref = db.backref('lugs', lazy = True))
    documentos = db.relationship('Documento', backref = db.backref('docs', lazy = True))
    agendamentos = db.relationship('Agendamento', backref = db.backref('ags', lazy = 'joined'), foreign_keys = [Agendamento.id_medico])

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meduser_id = db.Column(db.Integer, db.ForeignKey('usuario.id'),nullable = False)
    formacao = db.Column(db.String(100))
    anos_experiencia = db.Column(db.Integer)
    bio = db.Column(db.String(255))
    
    meduser = db.relationship("Usuario", backref=db.backref('medico'), lazy= 'joined')
    horarios = db.relationship("Horario", backref=db.backref('hor'), lazy= 'joined')

	
class Especialidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(50), nullable=False)
    medicos = db.relationship('Usuario', secondary=espec_med, backref=db.backref('medicos_spec', lazy='dynamic'))
	

class Documento(db.Model):
    id_documento = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(50), nullable = False)
    tipo_doc = db.Column(db.String(20))
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
	
class Lugar(db.Model):
    id_lugar = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'),nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    logradouro = db.Column(db.String(250))
    bairro = db.Column(db.String(250))
    complemento = db.Column(db.String(250))
    CEP = db.Column(db.String(8))	
	
class Horario(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_medico = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable = False)
	inicio = db.Column(db.DateTime, nullable = False)
	fim = db.Column(db.DateTime, nullable = False)




    #________________Configuração de schemas para o Marshmallow____

class Usuario_Schema(ma.ModelSchema):
    class Meta:
        model = Usuario


class Horario_Schema(ma.ModelSchema):
	class Meta:
		model = Horario	
		
class Medico_Schema(ma.ModelSchema):
    meduser = SmartNested(Usuario_Schema)    
    horario = SmartNested(Horario_Schema)

    class Meta:
        model = Medico


class Lugar_Schema(ma.ModelSchema):
    class Meta:
        mode1 = Lugar


class Especialidade_Schema(ma.ModelSchema):
    class Meta:
        model = Especialidade


class Documento_Schema(ma.ModelSchema):
    class Meta:	
        model = Documento

class Agendamento_Schema(ma.ModelSchema):
    class Meta:
        model = Agendamento
		


        


		
		
med_schema = Medico_Schema()
lug_schema = Lugar_Schema()
user_schema = Usuario_Schema()
espec_schema = Especialidade_Schema()
doc_schema = Documento_Schema()
age_schema = Agendamento_Schema()
hor_schema = Horario_Schema()

med_schemax = Medico_Schema(many=True)
lug_schemax = Lugar_Schema(many=True)
user_schemax = Usuario_Schema(many=True)
espec_schemax = Especialidade_Schema(many=True)
doc_schemax = Documento_Schema(many=True)
age_schemax = Agendamento_Schema(many=True)
hor_schemax = Horario_Schema(many=True)

db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

#__________________________________Rotas_________________________


@app.route("/rest/medico/<int:med_id>", methods=['GET','POST'])
@basic_auth.required
def getDocto(med_id):
	if(request.method == 'GET'):        
		med = Medico.query.get(med_id)
		obj = med_schema.dump(med)
		return jsonify(obj)
	else:
		med = Medico.query.get(med_id)
		med.meduser_id = request.form['meduser_id']
		med.formacao = request.form['formacao']
		med.anos_experiencia = request.form['anos_experiencia']
		med.bio = request.form['bio']
		
		if db.session.commit() == None:
			return "Medico atualizado"
		
@app.route("/rest/medico", methods=['POST'])
@basic_auth.required
def setDocto():
		med = Medico()
		med.formacao = request.form['formacao']
		med.anos_experiencia = request.form['anos_experiencia']
		med.bio = request.form['bio']
		med.meduser_id = request.form['meduser_id']
		db.session.add(med)
		if db.session.commit() == None:
			return "Medico Criado"
			
@app.route("/rest/espec_med/<int:usr_id>/<int:esp_id>", methods=['GET'])
@basic_auth.required
def addEsp(usr_id,esp_id):
		usr = Usuario.query.get(usr_id)
		esp = Especialidade.query.get(esp_id)
		usr.especialidades.append(esp)
		if db.session.commit() == None:
			return "Especialidade Adicionada"
	
@app.route("/rest/query1", methods=['POST'])
def getDoctos():
	state = request.form['state']
	city = request.form['city']
	id = request.form['id']
	
	query = Medico.query.options(joinedload('meduser')).join(Usuario).join(Lugar).\
	filter(Lugar.estado == state, Lugar.cidade == city,Usuario.especialidades.any(Especialidade.id == id),Medico.id == Usuario.id).all()
	output = med_schemax.dump(query) #https://www.youtube.com/watch?v=kRNXKzfYrPU usar esse para passar do query pro JSON
	return jsonify(output)


	
@app.route("/rest/agendamento/<int:ag_id>", methods=['GET', 'POST'])
def agendamento(ag_id):
	if(request.method == 'GET'):        
		ag = Agendamento.query.get(ag_id)
		obj = age_schema.dump(ag)
		return jsonify(obj)
	else:
		ag = Agendamento.query.get(ag_id)
		ag.id_medico = request.form['id_medico']
		ag.id_paciente = request.form['id_paciente']
		ag.cadastro = request.form['cadastro']
		ag.inicio = parse(request.form['inicio'])
		ag.fim = parse(request.form['fim'])
		ag.valor = request.form['valor']
		ag.voucher = request.form['voucher']
		ag.in_status = request.form['in_status']
		if db.session.commit() == None:
			return "Agendamento atualizado"

@app.route("/rest/agendamento", methods=['POST'])
def marca():
	ag = Agendamento()
	ag.id_medico = request.form['id_medico']
	ag.id_paciente = request.form['id_paciente']
	ag.cadastro = request.form['cadastro']
	ag.in_status = request.form['in_status']
	ag.inicio = parse(request.form['inicio'])
	ag.fim = parse(request.form['fim'])
	ag.voucher = request.form['voucher']
	ag.valor = request.form['valor']

	db.session.add(ag)
	if db.session.commit() == None:
			return "Agendamento criado"

			
@app.route("/rest/usuario", methods=['POST'])
@basic_auth.required
def usuarioreg():
	user = Usuario()
	user.email = request.form['email']
	user.tipo_id = request.form['tipo_id']
	user.senha = request.form['senha']
	user.nome = request.form['nome']
	user.dt_nascimento = parse(request.form['dt_nascimento'])

	db.session.add(user)
	if db.session.commit() == None:
		return 'Usuario criado'

		
@app.route("/rest/lugar/<int:lug_id>", methods=['GET','POST'])
@basic_auth.required
def getlug(lug_id):
	if request.method == 'GET':
		lug = Lugar.query.get(lug_id)
		obj = lug_schema.dump(lug)
		return jsonify(obj)
	else:	
		lug = Lugar.query.get(lug_id)
		lug.id = request.form['id']
		lug.estado = request.form['estado']
		lug.cidade = request.form['cidade']
		lug.logradouro = request.form['logradouro']
		lug.bairro = request.form['bairro']
		lug.complemento = request.form['complemento']
		lug.CEP = request.form['CEP']

		if db.session.commit() == None:
			return 'Usuario atualizado'	

	
@app.route("/rest/lugar", methods=['POST'])
@basic_auth.required
def lugarreg():
	lug = Lugar()
	lug.id = request.form['id']
	lug.estado = request.form['estado']
	lug.cidade = request.form['cidade']
	lug.logradouro = request.form['logradouro']
	lug.bairro = request.form['bairro']
	lug.complemento = request.form['complemento']
	lug.CEP = request.form['CEP']

	db.session.add(lug)
	if db.session.commit() == None:
		return 'Lugar criado'
		
@app.route("/rest/especialidade/<int:esp_id>", methods=['GET','POST'])
@basic_auth.required
def getesp(esp_id):
	if request.method == 'GET':
		esp = 	query.get(esp_id)
		obj = lug_schema.dump(esp)
		return jsonify(obj)
	else:
		esp = Especialidade.query.get(esp_id)
		esp.Especialidade = request.form['especialidade']
		if db.session.commit() == None:
			return 'Especialidade atualizada'	

	
@app.route("/rest/especialidade", methods=['POST'])
@basic_auth.required
def especialidadereg():
	esp = Especialidade()
	esp.Especialidade = request.form['especialidade']

	db.session.add(esp)
	if db.session.commit() == None:
		return 'especialidade criada'
		
@app.route("/rest/documento/<int:doc_id>", methods=['GET','POST'])
@basic_auth.required
def getDoc(doc_id):
	if request.method == 'GET':
		doc = Documento.query.get(doc_id)
		obj = doc_schema.dump(doc)
		return jsonify(obj)
	else:
		doc = Documento.query.get(doc_id)
		doc.Documento = request.form['documento']
		doc.tipo_doc = request.form['tipo_doc']
		doc.id = request.form['id']
		if db.session.commit() == None:
			return 'Documento atualizado'	

	
@app.route("/rest/documento", methods=['POST'])
@basic_auth.required
def docreg():
	doc = Documento()
	doc.documento = request.form['documento']
	doc.tipo_doc = request.form['tipo_doc']
	doc.id = request.form['id']
	db.session.add(doc)
	if db.session.commit() == None:
		return 'Documento criado'
		
@app.route("/rest/horario/<int:hor_id>", methods=['GET','POST'])
@basic_auth.required
def getHor(hor_id):
	if request.method == 'GET':
		hor = Horario.query.get(hor_id)
		obj = doc_schema.dump(hor)
		return jsonify(obj)
	else:
		hor = Horario.query.get(hor_id)
		hor.id_medico = request.form['id_medico']
		hor.inicio= parse(request.form['inicio'])
		hor.fim = parse(request.form['fim'])
		if db.session.commit() == None:
			return 'Horario atualizado'	

	
@app.route("/rest/horario", methods=['POST'])
@basic_auth.required
def horreg():
	hor = Horario()
	hor.id_medico = request.form['id_medico']
	hor.inicio= parse(request.form['inicio'])
	hor.fim = parse(request.form['fim'])
	db.session.add(hor)
	if db.session.commit() == None:
		return 'Horario criado'
		
@app.route("/rest/horarios/<int:med_id>", methods=['GET'])
@basic_auth.required
def horariosget(med_id):
	med = Medico.query.get(med_id)
	return jsonify((hor_schemax.dump(med.horarios)))

	
		
@app.route("/rest/agendamentos", methods=['GET'])
@login_required
def getagendamentos():
	return jsonify((age_schemax.dump(current_user.agendamentos)))
	


		
@app.route('/login', methods=['POST'])
def loginUser():
	user = Usuario.query.filter_by(email = request.form['email']).first()
	if user.senha == request.form['senha']:
		login_user(user)
		return 'Logado'
	else :
		return 'Senha incorreta'
		
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Você está deslogado!'
		


if __name__ == '__main__':
    app.run(debug=True)
