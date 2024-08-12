from django.shortcuts import render, redirect
from .forms import UsuarioForm
from .conectar import conectar_banco
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def page_login(request):
    request.session['id'] = ''
    request.session['tipo'] = ''
    form = UsuarioForm()
    return render(request, 'main/page_login.html', {'form': form})

def processa_login(request):
    banco = conectar_banco()
    cursor = banco.cursor()
    
    email = request.POST['email']
    senha = request.POST['senha']

    dados = (email, senha)
    sql = 'SELECT * FROM usuarios WHERE email=%s AND senha=%s;'
    cursor.execute(sql, dados)
    usuario_existe = cursor.fetchone()
    print(f'USUARIO ->> {usuario_existe}')
    
    cursor.close()
    banco.close()
    if usuario_existe:
        print('login realizado!!')
        print(usuario_existe[0])
        request.session['id'] = usuario_existe[0]
        request.session[ 'tipo' ] = usuario_existe[4]
        return redirect('page_home')
    else:
        print('usuario nao cadastrado!')
        return redirect('page_login')
            
def processa_criar_chamados(request):
    nome = request.POST['nome']
    email = request.POST['email']
    descricao = request.POST['descricao']
    tipo_servico = request.POST['tipo_servico']
    
    banco = conectar_banco()
    cursor = banco.cursor()
    
    sql = "INSERT INTO chamados (nome, email, tipo_servico, descricao, situacao) VALUES (%s, %s, %s, %s, %s)"
    
    dados = (nome, email, tipo_servico, descricao, 'Em espera')
    cursor.execute(sql, dados)#os valores vao ser adicionados ao comando sql na ordem que sao passados
    banco.commit()
    print('SALVOU COM SUCESSO!!')
    return redirect('page_home')

def processa_cadastro(request):
    banco = conectar_banco()
    cursor = banco.cursor()
    email = request.POST['email']
    nome = request.POST['nome']
    senha = request.POST['senha']
    tipo = request.POST['tipo']
    
    sql = '''
        INSERT INTO usuarios (email, nome, senha, tipo) VALUES (%s, %s, %s, %s);
    '''
    dados = (email, nome, senha, tipo)
    cursor.execute(sql, dados)
    banco.commit()
    
    return redirect('page_home')
    
def page_atualizar_usuario(request, id):
    return render(request, 'main/page_atualizar_usuario.html', {'id': id})

def processa_atualizar_usuario(request, id):
    banco = conectar_banco()
    cursor = banco.cursor()
    
    novo_nome = request.POST['nome']
    novo_email = request.POST['email']
    nova_senha = request.POST['senha']
    dados = (novo_nome, novo_email, nova_senha, id)
    cursor.execute('UPDATE usuarios SET nome=%s, email=%s, senha=%s WHERE id=%s', dados)
    banco.commit()
    
    banco.close()
    cursor.close()
    
    return redirect('page_mostrar_usuarios')

def excluir_usuario(request, id):
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id=%s;', (id, ))
    
    banco.commit()
    banco.close()
    cursor.close()
    return redirect('page_home')

def page_home(request):
    #validação do login
    if not request.session.get('id'):
        return redirect('page_login')
    else:
        usuario_id = request.session.get('id') #id do usuario logado
        banco = conectar_banco()
        cursor = banco.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE id=%s', (usuario_id, ))
        usuario_logado = cursor.fetchone()
        print(f'USUARIO LOGADO -> {usuario_logado}')
            #pega os chamados que foram finalizados
        sql = '''
            SELECT * FROM chamados as ct
            INNER JOIN usuario_chamado as uc
            ON uc.chamado_id=ct.id
            WHERE uc.usuario_id=%s AND uc.situacao = 'Finalizado';
        '''
        cursor.execute(sql, (usuario_id, ))
        sql = cursor.fetchall()

        sql2 = '''
            SELECT * FROM chamados
            WHERE situacao = 'Finalizado';
        '''
        cursor.execute(sql2)
        sql2 = cursor.fetchall()
        print(f'2 -> {sql2}')
            
        print(f'USUARIO LOGADO -> {request.user}')
        context = {
            'sql': sql,
            'sql2': sql2,
            'usuario_logado': usuario_logado
        }
        return render(request, 'main/page_home.html', context)

def page_criar_chamado(request):
    if not request.session.get('id'):
        return redirect('page_login')
    if request.session.get('tipo') == 'tec':
        return redirect('page_home')
    return render(request, 'main/page_criar_chamado.html')

def page_cadastro(request):
    if not request.session.get('id'):
        return redirect('page_login')
    if request.session.get('tipo') != 'adm':
        return redirect('page_home')
    # if not request.session.get('tipo')
    print(f'TIPO -> {request.session.get('tipo')}')
    return render(request, 'main/page_cadastro.html')

def page_mostrar_chamados(request):
    print(f'SESSION ID -> {request.session['id']}')
    if not request.session.get('id'):
        return redirect('page_login')
    if request.session.get('tipo') == 'job':
        return redirect('page_home')
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM chamados WHERE situacao = 'Em espera';")
    sql = cursor.fetchall()

    banco.close()
    cursor.close()
    return render(request, 'main/page_mostrar_chamados.html', {'sql': sql})

def page_mostrar_usuarios(request):
    if not request.session.get('id'):
        return redirect('page_login')
    if request.session.get('tipo') != 'adm':
        return redirect('page_home')
    banco = conectar_banco()
    cursor = banco.cursor()
    
    usuario_id = request.session.get('id')
    
    #garante que o usuario não vá excluir o proprio cadastro
    cursor.execute('SELECT * FROM usuarios WHERE usuarios.id != %s', (usuario_id, ))
    sql = cursor.fetchall()
    return render(request, 'main/page_mostrar_usuarios.html', {'sql': sql})

def page_mostrar_meus_chamados(request):
    if not request.session.get('id'):
        return redirect('page_login')
    if request.session.get('tipo') == 'job':
        return redirect('page_home')
    banco = conectar_banco()
    cursor = banco.cursor()
    usuario_id = request.session.get('id') #id do usuario logado
    
    #pega os chamados referentes ao usuario logado
    sql = '''
        SELECT * FROM chamados as ct
        INNER JOIN usuario_chamado as uc
        ON uc.chamado_id=ct.id
        WHERE uc.usuario_id=%s AND uc.situacao = 'Em atendimento'
    '''
    
    #pega os chamados que foram finalizados
    sql2 = '''
        SELECT * FROM chamados as ct
        INNER JOIN usuario_chamado as uc
        ON uc.chamado_id=ct.id
        WHERE uc.usuario_id=%s AND uc.situacao = 'Finalizado'
    '''
    
    cursor.execute(sql, (usuario_id, ))
    sql = cursor.fetchall()
    
    cursor.execute(sql2, (usuario_id, ))
    sql2 = cursor.fetchall()
    
    print(f'SQL ->> {sql2}')
    
    context = {
        'sql': sql,
        'sql2': sql2
    }
    return render(request, 'main/page_mostrar_meus_chamados.html', context)

def atribui_atendimento(request, id):#id que esta sendo recebido no template (id do contato que for clicado) e esta sendo passado em urls.py
    usuario_id = request.session.get('id') #id do usuario logado
    
    banco = conectar_banco()
    cursor = banco.cursor()

    #muda a situação na tabela contatos
    sql = 'UPDATE chamados SET situacao = %s WHERE id = %s'
    dados = ('Em atendimento', int(id)) #para nao ter erros, garantir que o id recebido é um INT( id do contato )
    cursor.execute(sql, dados)
    banco.commit()
    
    #insere os dados na tabela usuario_contato
    sql2 = 'INSERT INTO usuario_chamado (usuario_id, chamado_id, situacao) VALUES (%s, %s, %s);'#inserindo o registro de atribuição ao usuario na tabela de historicos (usuario_contato)
    dados = (int(usuario_id), int(id), 'Em atendimento')
    cursor.execute(sql2, dados)
    banco.commit()
    
    return redirect('page_mostrar_chamados')

def finalizar_chamado(request, id):#id que esta sendo recebido no template (id do contato que for clicado) e esta sendo passado em urls.py
    banco = conectar_banco()
    cursor = banco.cursor()
    
    cursor.execute("UPDATE chamados SET situacao = 'Finalizado' WHERE id = %s", (id, ))
    cursor.execute("UPDATE usuario_chamado SET situacao = 'Finalizado' WHERE chamado_id = %s", (id, ))
    banco.commit()
    return redirect('page_mostrar_meus_chamados')

def lista_admin(request):
    banco = conectar_banco()
    cursor = banco.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE tipo = 'adm';")
    lista = cursor.fetchall()
    
    return render(request, 'main/lista_admin.html', {'lista': lista})