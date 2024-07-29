import mysql.connector


def conectar_banco():
    print('AQUI 1 ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    connector = mysql.connector.connect(host="127.0.0.1", user="root", password="")
    print('AQUI 2 ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # Executar a instrução SQL para verificar se o banco de dados existe
    cursor = connector.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "projeto_django";'
    )

    # Obter o número de resultados
    num_results = cursor.fetchone()[0]

    # Fechar a conexão com o banco de dados
    connector.close()

    # Se o número de resultados for maior que zero, o banco de dados existe
    if num_results > 0:
        print("O banco de dados projeto_django existe e esta pronto para uso.")
    else:
        # Conectar-se ao servidor MySQL para criar o banco de dados
        connector = mysql.connector.connect(host="127.0.0.1", user="root", password="")

        # Criar o banco de dados projeto_django
        cursor = connector.cursor()
        cursor.execute("CREATE DATABASE projeto_django;")
        connector.commit()

        # Conectar-se ao banco de dados projeto_django recém-criado
        connector = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="projeto_django",  # Especificar o banco de dados
        )

        cursor = connector.cursor()
        cursor.execute(
            "CREATE TABLE chamados (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), email VARCHAR(255) NOT NULL, tipo_servico VARCHAR(255) NOT NULL, descricao TEXT NOT NULL, situacao varchar (50) NOT NULL);"
        )

        cursor.execute(
            "CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), email VARCHAR(255), senha VARCHAR(255), tipo VARCHAR(255));"
        )

        cursor.execute(
            "CREATE TABLE usuario_chamado (usuario_id INT NOT NULL, chamado_id INT NOT NULL, situacao VARCHAR(255) NOT NULL, PRIMARY KEY (usuario_id, chamado_id), FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE, FOREIGN KEY (chamado_id) REFERENCES chamados(id) ON DELETE CASCADE);"
        )
        connector.commit()
        nome = "admin"
        email = "admin@admin.com"
        senha = "123"
        tipo = "adm"
        sql = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)"
        valores = (nome, email, senha, tipo)
        cursor.execute(sql, valores)
        connector.commit()

        connector.close()

    try:
        banco = mysql.connector.connect(
            host="127.0.0.1", user="root", password="", database="projeto_django"
        )
    except mysql.connector.Error as err:
        print("Erro de conexão com o banco de dados:", err)
        raise

    return banco
