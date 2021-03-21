from flask import Flask, render_template, request, url_for, redirect, flash
import urllib
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config["DEBUG"] = True

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=DESKTOP-T7D96U5;"
                                 "DATABASE=DB01;"
                                 "Trusted_Connection=yes") 

app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = secrets.token_urlsafe(32)

db = SQLAlchemy(app)

#REGION MODELS
class Produto(db.Model):
    __tablename__ = "Produto"
    idProduto = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(50))
    CodigoEmbalagem = db.Column(db.String(20))
    
class Cliente(db.Model):
    __tablename__ = "Cliente"
    idCliente = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20))
    Idade = db.Column(db.Integer)

class Venda(db.Model):
    __tablename__ = "Venda"
    idVenda = db.Column(db.Integer, primary_key=True)
    fkCliente = db.Column(db.Integer, db.ForeignKey('Cliente.idCliente'))
    fkProduto = db.Column(db.Integer, db.ForeignKey('Produto.idProduto'))
    Quantidade = db.Column(db.Integer)
    

#REGION HOME PAGE
@app.route("/", methods=["GET"])
def HomePage():
    if request.method == 'GET':
        return render_template("Home.html")


@app.route("/Product", methods=["GET"])
def RedirectProduct():
    if request.method == "GET":
        return redirect(url_for("HomeProduct"))
    
    
@app.route("/Client", methods=["GET"])
def RedirectClient():
    if request.method == "GET":
        return redirect(url_for("HomeClient"))
    
    
@app.route("/Buy", methods=["GET"])
def RedirectBuy():
    if request.method == "GET":
        return redirect(url_for("HomeBuy"))
    
    

#REGION PRODUCT REGISTRATION
@app.route("/CadastraProduto", methods=["GET", "POST"])
def HomeProduct():
    if request.method == 'GET':
        return render_template("ProductRegistration.html", produtos=Produto.query.all())

@app.route("/CadastraProduto/adicionar", methods=["POST"])
def Productadd():
    produto = Produto(
                        Descricao=request.form["prodDescricao"],
                        CodigoEmbalagem=request.form["prodEmbalagem"]
                    )
    
    if produto.Descricao != '' and produto.CodigoEmbalagem != '':
        db.session.add(produto) 
        db.session.commit()
        flash('Produto Cadastrado com Sucesso','success')
        return redirect(url_for('HomeProduct'))
    else:
        flash('Falha ao Cadastrar Produto','danger')
        return redirect(url_for('HomeProduct'))


@app.route("/CadastraProduto/atualizar", methods=["POST"])
def ProductUpdate():
    _description = request.form.get("new")
    codigo = request.form.get("cod")
    
    if codigo != None:
        produto = Produto.query.filter_by(idProduto=codigo).first()
        
        if _description != '':
            if _description != produto.Descricao: 
                produto.Descricao = _description
                db.session.commit()
                
                flash('Produto Atualizado com Sucesso','success')
                return redirect(url_for('HomeProduct'))
            else:
                flash('Nova Descrição é Igual a Anterior','warning')
                return redirect(url_for('HomeProduct'))     
        else:
            flash('Erro ao Atualizar Produto','danger')
            return redirect(url_for('HomeProduct'))
    
@app.route("/CadastraProduto/apagar", methods=["POST"])
def ProductDelete():
    codigo = request.form.get("description")
    produto = Produto.query.filter_by(idProduto=codigo).first()
    venda = Venda.query.filter_by(fkProduto=codigo).first()
    
    if venda == None:
        db.session.delete(produto)
        db.session.commit()
        flash('Produto Excluido com Sucesso','success')
        return redirect(url_for('HomeProduct'))
    else:
        flash('Falha ao Excluir Produto ( Existe Vendas vinculada a esse Produto )','danger')
        return redirect(url_for('HomeProduct'))
    


#REGION CLIENTE REGISTRATION
@app.route("/CadastraCliente", methods=["GET"])
def HomeClient():
    if request.method == "GET":
        return render_template("ClientRegistration.html", clientes=Cliente.query.all())
    
    
@app.route("/CadastraCliente/adicionar", methods=["POST"])
def Clientadd():
    if request.form["cliNome"] != '' and request.form["cliIdade"] != '':
        cliente = Cliente(
                            FirstName=request.form["cliNome"],
                            Idade=int(request.form["cliIdade"])
                        )
        if cliente.Idade > 0:
            db.session.add(cliente) 
            db.session.commit()
            flash('Cliente Cadastrado com Sucesso','success')
            return redirect(url_for('HomeClient'))
        else:
            flash('Idade não pode ser igual á Zero','danger')
            return redirect(url_for('HomeClient'))
    else:
        flash('Falha ao Cadastrar Cliente','danger')
        return redirect(url_for('HomeClient'))


@app.route("/CadastraCliente/atualizar", methods=["POST"])
def ClientUpdate():
    _description = request.form.get("new")
    codigo = request.form.get("cod")
    
    if codigo != None:
        cliente = Cliente.query.filter_by(idCliente=codigo).first()

        if _description != '':
            if _description != cliente.FirstName: 
                cliente.FirstName = _description
                db.session.commit()
                
                flash('Nome do Cliente Atualizado com Sucesso','success')
                return redirect(url_for('HomeClient'))
            else:
                flash('Nome digitado é Igual ao Anterior','warning')
                return redirect(url_for('HomeClient'))     
        else:
            flash('Erro ao Atualizar Cliente','danger')
            return redirect(url_for('HomeClient'))    
    
    
@app.route("/CadastraCliente/apagar", methods=["POST"])
def ClientDelete():
    codigo = request.form.get("description")
    cliente = Cliente.query.filter_by(idCliente=codigo).first()
    venda = Venda.query.filter_by(fkCliente=codigo).first()
    
    if venda == None:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente Excluido com Sucesso','success')
        return redirect(url_for('HomeClient'))
    else:
        flash('Erro Ao Excluir Cliente ( Existe Venda Registradas para esse Cliente )','danger')
        return redirect(url_for('HomeClient'))    
    
#REGION BUY
@app.route("/CadastraCompra")
def HomeBuy():
    if request.method == "GET":
        result = db.session.query(Venda, Cliente, Produto). \
                select_from(Venda).join(Cliente). \
                join(Produto).all()
                        
        
    return render_template("Buy.html", clientes = Cliente.query.all(), \
                            produtos = Produto.query.all(), \
                            lista = result)
    
@app.route("/CadastraCompra/adicionar", methods=["POST"])
def Buyadd():
    Intqtd = request.form.get("sQtd")
    IntCliente = request.form.get("sCliente")
    IntProduto = request.form.get("sProduto")    

    venda = Venda(
                    fkCliente=int(IntCliente),
                    fkProduto=int(IntProduto),
                    Quantidade=int(Intqtd)                   
                )
    
    if venda.fkCliente != 0 and venda.fkProduto != 0 and venda.Quantidade != 0:
        db.session.add(venda)
        db.session.commit()
        flash('Venda Cadastrada Com Sucesso','success')
        return redirect(url_for("HomeBuy"))
    else:
        flash('Falha ao Cadastrar Venda','danger')
        return redirect(url_for("HomeBuy"))


@app.route("/CadastraCompra/apagar", methods=["POST"])
def BuyDelete():
    codigo = request.form.get("description")
    venda = Venda.query.filter_by(idVenda=codigo).first()
    
    if codigo != None:
        db.session.delete(venda)
        db.session.commit()
        flash('Venda Excluida com Sucesso','success')
        return redirect(url_for('HomeBuy'))
    else:
        flash('Erro Ao Excluir Venda','danger')
        return redirect(url_for('HomeBuy'))    
    
if __name__ == "__main__":
    app.run(debug=True)