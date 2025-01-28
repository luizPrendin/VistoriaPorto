import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
import oracledb
import cv2
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from roboflow import Roboflow
import os 
import json
import time
from datetime import datetime
#pip install opencv-python
#pip install roboflow


class MeuApp(App):

    def __init__(self):
        super().__init__()
        self.conn = oracledb.connect(user="rm552475", password="130105",
                                     dsn="oracle.fiap.com.br:1521/orcl")
        print("Conectado no banco de dados")

    def build(self):
        self.screen_manager = ScreenManager()
        self.main_screen = MainScreen(name='main')
        self.second_screen = SecondScreen(name='second')
        self.third_screen = ThirdScreen(name = 'third')
        self.bike_screen = BikeScreen(name = 'bike')
        self.vistoria_screen = VistoriaScreen(name='vistoria')
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.second_screen)
        self.screen_manager.add_widget(self.third_screen)
        self.screen_manager.add_widget(self.bike_screen)
        self.screen_manager.add_widget(self.vistoria_screen)
        return self.screen_manager

class MainScreen(Screen):

    def verf_login(self,*args):
        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            #Realiza a consulta no banco de dados
            cursor.execute("""SELECT * FROM usuarios """)
            users = cursor.fetchall()
            cursor.close()

            
            #Percorre todos os registros do banco de dados
            for user in users:                 
                 #Verifica em todos os registros
                if self.txt_user.text == user[0] and self.txt_senha.text in user[1]:
                    print("Usuario encontrado!")
                    #Retorna a tela de menu
                    return self.tela_menu(instance='main')
            print("Usuario ou senha incorretos!")

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar o usuário:", error.message)


    def tela_menu(self, instance):

        self.manager.current = 'second'
    
    def tela_cad(self, instance):
        self.manager.current = 'third'

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        box = BoxLayout(orientation ="vertical")
        boxNome= BoxLayout(orientation="horizontal")
        boxSenha = BoxLayout(orientation="horizontal")
        self.txt_user = TextInput()
        self.txt_senha = TextInput(password=True,password_mask="*")
        label_username = Label(text="Nome de Usuario: ")
        label_senha= Label(text="Senha: ")
        boxNome.add_widget(label_username)
        boxNome.add_widget(self.txt_user)
        boxSenha.add_widget(label_senha)
        boxSenha.add_widget(self.txt_senha)
        btn_login= Button(text="LOGIN")
        btn_cad = Button(text="CADASTRAR")
        box_btn =BoxLayout(orientation = "horizontal")
        box_btn.add_widget(btn_login)
        box_btn.add_widget(btn_cad)
        
        btn_login.bind(on_press = self.verf_login)
        btn_cad.bind(on_press = self.tela_cad)

        box.add_widget(boxNome)
        box.add_widget(boxSenha)
        box.add_widget(box_btn)

        self.add_widget(box)


class SecondScreen(Screen):

    def tela_desenvolvedores(self,instance):
        self.box_op1.clear_widgets()
        self.box_op2.clear_widgets()
        self.box_op3.clear_widgets()
        self.box_vert.clear_widgets()
        btn_voltar =Button(text='voltar',on_press=self.voltar_menu)

        self.box_vert.add_widget(Label(text="99768 - Luiza Nunes de Jesus - REPRESENTANTE"))
        self.box_vert.add_widget(Label(text="99892 - Livia Freitas Ferreira"))
        self.box_vert.add_widget(Label(text="551325 - Renato Sanches Russano Romeu"))
        self.box_vert.add_widget(Label(text="552475 - Luiz Felipe Camargo Prendin"))
        self.box_vert.add_widget(Label(text="99494 - Vinícius de Araújo Camargo"))
        self.box_vert.add_widget(Label(text="550870 - Gabriel de Andrade Baltazar")) 

        self.box_vert.add_widget(btn_voltar)       

    def tela_vistoria(self,intance):
        self.manager.current ='vistoria'

    def tela_bike(self,instance):
        self.manager.current = 'bike'

    def tela_login(self, instance):
        self.manager.current = 'main'

    def voltar_menu(self,*args):
        self.box_vert.clear_widgets()
        return self.telaMenu()

    def telaMenu(self):
        self.box_vert = BoxLayout(orientation="vertical")
        self.box_op1 = BoxLayout(orientation= "horizontal")
        self.box_op2 = BoxLayout(orientation="horizontal")
        self.box_op3 = BoxLayout(orientation="horizontal")
        label = Label(text="MENU:")
        label_op1 = Label(text="Minhas bikes:")
        btn_op1 = Button(text="selecionar")
        self.box_op1.add_widget(label_op1)
        self.box_op1.add_widget(btn_op1)
        btn_op1.bind(on_press=self.tela_bike)
        btn_op2 =Button(text="selecionar")
        self.box_op2.add_widget(Label(text="Vistoria: "))
        self.box_op2.add_widget(btn_op2)
        btn_op2.bind(on_press= self.tela_vistoria)
        btn_op3 = Button(text="selecionar")
        self.box_op3.add_widget(Label(text="Desenvolvedores"))        
        self.box_op3.add_widget(btn_op3)
        btn_op3.bind(on_press=self.tela_desenvolvedores)
        btn_back = Button(text="Voltar")

        btn_back.bind(on_press=self.tela_login)

        self.box_vert.add_widget(label)
        self.box_vert.add_widget(self.box_op1)
        self.box_vert.add_widget(self.box_op2)
        self.box_vert.add_widget(self.box_op3)
        self.box_vert.add_widget(btn_back)

        self.add_widget(self.box_vert)

    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        self.telaMenu()
        


class ThirdScreen(Screen):

    def cadastrar_usuario(self, instance):
        # Obtém os valores dos TextInputs
        username = self.txt_name.text
        senha = self.txt_senha.text

        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            # Executa a inserção na tabela usuarios
            cursor.execute("INSERT INTO usuarios (USERNAME, SENHA) VALUES (:name, :senha)", name=username, senha=senha)
            conn.commit()  # Comita a transação

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()

            print("Usuário cadastrado com sucesso!")

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar o usuário:", error.message)

    def tela_login(self, instance):
        self.manager.current = 'main'

    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)

        box = BoxLayout(orientation="vertical")
        label = Label(text="CADASTRO")
        btn_box =BoxLayout(orientation ="horizontal")
        btn_back = Button(text="Voltar ")
        btn_cad = Button(text="CADASTRAR")
        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_cad)
        
        box_name = BoxLayout(orientation ="horizontal")
        box_senha = BoxLayout(orientation ="horizontal")
        lab_name = Label(text ="Nome de usuario:")
        self.txt_name =TextInput()
        lab_senha = Label(text ="Senha: ")
        self.txt_senha =TextInput()

        box_name.add_widget(lab_name)
        box_name.add_widget(self.txt_name)
        box_senha.add_widget(lab_senha)
        box_senha.add_widget(self.txt_senha)      


        
        btn_cad.bind(on_press=self.cadastrar_usuario)
        btn_back.bind(on_press=self.tela_login)

        box.add_widget(label)
        box.add_widget(box_name)
        box.add_widget(box_senha)
        box.add_widget(btn_box)

        self.add_widget(box)

class BikeScreen(Screen):

    def salvar(self,instance):
        
        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            self.salvar_em_json(self.txt_marca.text,self.txt_modelo.text,self.txt_aro.text)
            #lendo arquivo json
            

           
            # Executa a inserção na tabela usuarios
            cursor.execute("INSERT INTO bikes (id,marca,modelo,aro) VALUES (SQ_BIKE.NEXTVAL,:marca, :modelo, :aro)", marca = self.txt_marca.text, modelo = self.txt_modelo.text, aro=self.txt_aro.text)
            conn.commit()  # Comita a transação

            # Fecha o cursor e a conexão
            cursor.close()
            conn.close()
            
            print("Bike cadastrada com sucesso!")
            return self.tela_anterior(instance)

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar a Bike:", error.message)


    def tela_cadastrar(self,*args):
        self.box_cad.clear_widgets()
        self.box_alt.clear_widgets()
        self.box_excl.clear_widgets()
        self.box_btn.clear_widgets()

        self.box_cad.add_widget(Label(text="Informe a marca:"))
        self.txt_marca=TextInput(_hint_text="Caloi,Bmx...")
        self.box_cad.add_widget(self.txt_marca)
        self.box_alt.add_widget(Label(text="Informe o modelo"))
        self.txt_modelo=TextInput(_hint_text="Caloi10,proX...")
        self.box_alt.add_widget(self.txt_modelo)

        self.box_excl.add_widget(Label(text="Informe o aro:"))
        self.txt_aro=TextInput(_hint_text="Aro16,aro15...")
        self.box_excl.add_widget(self.txt_aro)

        self.btn_salvar= Button(text="Cadastrar")
        btn_back = Button(text="Voltar")

        self.box_btn.add_widget(self.btn_salvar)
        self.box_btn.add_widget(btn_back)
        self.btn_salvar.bind(on_press=self.salvar)
        btn_back.bind(on_press=self.tela_anterior)

    def atualizar(self,instance):
        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            
            #Realiza a consulta no banco de dados
            cursor.execute(f"""UPDATE bikes 
                           SET marca = :marca, modelo= :modelo, aro = :aro
                            WHERE id ={self.valor} """, marca = self.txt_nvmarca.text, modelo = self.txt_nvmodelo.text, aro =self.txt_nvaro.text)
            conn.commit()
            print("Bike alterada!")
            cursor.close()
            conn.close()
            return self.voltar_tela(instance)


        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar a Bike:", error.message)

            
    def salvar_em_json(self, marca, modelo, aro):
        dados = {
            "marca": marca,
            "modelo": modelo,
            "aro": aro
        }

        try:
            if not os.path.exists("bicicletas.json"):
                with open("bicicletas.json", 'w') as arquivo:
                    json.dump([], arquivo)

            with open("bicicletas.json", 'r') as arquivo:
                try:
                    data = json.load(arquivo)
                except json.JSONDecodeError:  # Lidar com um arquivo vazio ou inválido
                    data = []

            data.append(dados)

            with open("bicicletas.json", 'w') as arquivo:
                json.dump(data, arquivo, indent=4)

        except Exception as e:
            print("Erro ao salvar no arquivo JSON:", e)

    
    def tela_alt_bike(self,instance):
        self.box.clear_widgets()
        self.box_horz.clear_widgets()        
        self.box_marca = BoxLayout(orientation ="horizontal")
        self.box_modelo = BoxLayout(orientation ="horizontal")
        self.box_aro = BoxLayout(orientation ="horizontal")
        self.box_btn = BoxLayout(orientation ="horizontal")        

        
        self.valor = instance.valor
        marca= instance.marca
        modelo= instance.modelo
        aro= instance.aro
        
        

        
        self.txt_nvmarca =TextInput(_hint_text=f"{marca}")
        

        
        self.txt_nvmodelo =TextInput(_hint_text=f"{modelo}")
        

        
        self.txt_nvaro=TextInput(_hint_text=f"{aro}")
            


        
        btn_atualizar= Button(text="ALTERAR")
        btn_voltar = Button(text="Voltar")
        btn_voltar.bind(on_press=self.voltar_tela)
        btn_atualizar.bind(on_press=self.atualizar)
        self.box_btn.add_widget(btn_atualizar)
        self.box_btn.add_widget(btn_voltar)
        self.box_marca.add_widget(Label(text=f"MARCA"))
        self.box_marca.add_widget(self.txt_nvmarca)
        self.box_modelo.add_widget(Label(text="MODELO"))
        self.box_modelo.add_widget(self.txt_nvmodelo)
        self.box_aro.add_widget(Label(text="ARO"))
        self.box_aro.add_widget(self.txt_nvaro)
        self.box.add_widget(self.box_marca)
        self.box.add_widget(self.box_modelo)
        self.box.add_widget(self.box_aro)
        self.box.add_widget(self.box_btn)

            
    def tela_excl_bike(self,instance):
        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()
            modelo = instance.modelo
            cursor.execute("DELETE FROM BIKES WHERE MODELO = :modelo", modelo = modelo)
            conn.commit()
            print("Bike excluida!")
            cursor.close()
            conn.close()
            return self.voltar_tela(instance)

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar a Bike:", error.message)

        

    def tela_alterar(self,*args):
        self.box_cad.clear_widgets()
        self.box_alt.clear_widgets()
        self.box_excl.clear_widgets()
        self.box_btn.clear_widgets()
        self.box.clear_widgets()

        
        self.box.add_widget(Label(text="Selecione sua bike para alterar:"))
        

        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            #Realiza a consulta no banco de dados
            cursor.execute("""SELECT * FROM bikes """)
            bikes = cursor.fetchall()
            cursor.close()

            
            #Percorre todos os registros do banco de dados
            cont = 0
            for bike in bikes:
                 cont+= 1
                 self.box_horz =BoxLayout(orientation ="horizontal")
                 self.btn_select = Button(text ="selecionar")
                 self.btn_select.valor = cont
                 self.btn_select.marca = bike[1]
                 self.btn_select.modelo = bike[2]
                 self.btn_select.aro = bike[3]
                 self.btn_select.bind(on_press=self.tela_alt_bike)  
                 self.box_horz.add_widget(Label(text=f"{cont}: {bike[2]}"))
                 self.box_horz.add_widget(self.btn_select)
                 self.box.add_widget(self.box_horz)

            btn_voltar= Button(text="voltar")
            self.box.add_widget(btn_voltar)
            btn_voltar.bind(on_press = self.tela_anterior)

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar a Bike:", error.message)

    def tela_excl(self,*args):
        self.box_cad.clear_widgets()
        self.box_alt.clear_widgets()
        self.box_excl.clear_widgets()
        self.box_btn.clear_widgets()
        self.box.clear_widgets()

        self.box.add_widget(Label(text="Selecione uma bike que queira excluir:"))
        

        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            #Realiza a consulta no banco de dados
            cursor.execute("""SELECT * FROM bikes """)
            bikes = cursor.fetchall()
            cursor.close()

            
            #Percorre todos os registros do banco de dados
            cont = 0
            for bike in bikes:
                 cont+= 1
                 self.box_horz =BoxLayout(orientation ="horizontal")
                 self.btn_select = Button(text ="EXCLUIR")
                 self.btn_select.valor = cont
                 self.btn_select.marca = bike[1]
                 self.btn_select.modelo = bike[2]
                 self.btn_select.aro = bike[3]
                 self.btn_select.bind(on_press=self.tela_excl_bike)  
                 self.box_horz.add_widget(Label(text=f"{cont}: {bike[2]}"))
                 self.box_horz.add_widget(self.btn_select)
                 self.box.add_widget(self.box_horz)
            
            btn_voltar=Button(text="voltar")
            self.box.add_widget(btn_voltar)
            btn_voltar.bind(on_press=self.voltar_tela)

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar a Bike:", error.message)


    def tela_menu(self,instance):
        self.manager.current = 'second'

    def tela_bike(self,*args):
            
            self.box = BoxLayout(orientation ="vertical")
            self.box_cad = BoxLayout(orientation ="horizontal")
            self.box_excl = BoxLayout(orientation ="horizontal")
            self.box_alt = BoxLayout(orientation ="horizontal")
            self.box_btn = BoxLayout(orientation ="horizontal")
            btn_cad= Button(text="selecionar")
            btn_alt= Button(text="selecionar")
            btn_excl= Button(text="selecionar")
            btn_back = Button(text="Voltar")
            btn_cad.bind(on_press=self.tela_cadastrar)
            btn_alt.bind(on_press = self.tela_alterar)
            btn_excl.bind(on_press = self.tela_excl)
            btn_back.bind(on_press=self.tela_menu)
            self.box_btn.add_widget(btn_back)

            self.box_cad.add_widget(Label(text="Cadastrar"))
            self.box_cad.add_widget(btn_cad)
            self.box_alt.add_widget(Label(text="Alterar"))
            self.box_alt.add_widget(btn_alt)
            self.box_excl.add_widget(Label(text="Excluir"))
            self.box_excl.add_widget(btn_excl)


            self.box.add_widget(self.box_cad)
            self.box.add_widget(self.box_alt)
            self.box.add_widget(self.box_excl)
            self.box.add_widget(self.box_btn)        
            self.add_widget(self.box)

    def voltar_tela(self,instance):
        self.box_horz.clear_widgets()
        self.box.clear_widgets()
        self.tela_bike()

    def tela_anterior(self,instance):
        self.box_cad.clear_widgets()
        self.box_alt.clear_widgets()
        self.box_excl.clear_widgets()
        self.box_btn.clear_widgets()
        self.box.clear_widgets()
        
        self.tela_bike()


    def __init__(self, **kwargs):
        super(BikeScreen, self).__init__(**kwargs)
        
        self.tela_bike()

class VistoriaScreen(Screen):

    def convert_image(self,file_path):
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        return binary_data
    
    def salva_imgdb(self,img):
        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO imagens(img)VALUES(:image)",image=img)
            conn.commit()
            cursor.close()
            conn.close()
            print("Imagem salva no banco de dados")

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar a Bike:", error.message)
    def agendar(self,*args):
        dataVistoria = self.txt_data.text
        data = datetime.today().strftime('%A, %B %d, %Y %H:%M:%S')
        print(f"Ótimo realizamos o seu pedido para vistoria na data: {dataVistoria}\n {data}")
        time.sleep(3.2)
        
    
    def tela_pvisto(self,instance):
        self.box_horz.clear_widgets()
        self.box.clear_widgets()
        self.boxbtn = BoxLayout(orientation ="horizontal")

        self.box_horz.add_widget(Label(text="Informe uma data:"))
        self.txt_data= TextInput(hint_text='DD/MM/AAAA')
        self.box_horz.add_widget(self.txt_data)

        #self.modelo = instance.modelo
        
        btn_voltar = Button(text="voltar")
        btn_voltar.bind(on_press=self.voltar_pvisto)
        btn_agendar =Button(text="agendar")
        btn_agendar.bind(on_press=self.agendar)

        self.boxbtn.add_widget(btn_voltar)
        self.boxbtn.add_widget(btn_agendar)
        
        self.box.add_widget(self.box_horz)
        self.box.add_widget(self.boxbtn)


    def preVistoria(self,instance):
        self.limpar_tela()

        self.box.add_widget(Label(text="Selecione uma de suas bikes para a vistoria:"))
        

        try:
            # Cria uma conexão com o banco de dados Oracle
            conn = oracledb.connect(user="rm552475", password="130105", dsn="oracle.fiap.com.br:1521/orcl")
            cursor = conn.cursor()

            #Realiza a consulta no banco de dados
            cursor.execute("""SELECT * FROM bikes """)
            bikes = cursor.fetchall()
            cursor.close()

            
            #Percorre todos os registros do banco de dados
            cont = 0
            for bike in bikes:
                 cont+= 1
                 self.box_horz =BoxLayout(orientation ="horizontal")
                 self.btn_select = Button(text ="selecionar")
                 self.btn_select.valor = cont
                 self.btn_select.marca = bike[1]
                 self.btn_select.modelo = bike[2]
                 self.btn_select.aro = bike[3]
                 self.btn_select.bind(on_press=self.tela_pvisto)  
                 self.box_horz.add_widget(Label(text=f"{cont}: {bike[2]}"))
                 self.box_horz.add_widget(self.btn_select)
                 self.box.add_widget(self.box_horz)

            btn_voltar= Button(text="voltar")
            self.box.add_widget(btn_voltar)
            btn_voltar.bind(on_press = self.voltar_pvisto)

        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao cadastrar a Bike:", error.message)       

    def vistoria_bike(self,instance):
        self.limpar_tela()

        self.capture = cv2.VideoCapture(0)  # Inicializa a captura de vídeo da câmera

        # Cria um widget de imagem para exibir a pré-visualização
        self.preview_image = Image()
        self.add_widget(self.preview_image)

        # Cria um widget de imagem para exibir a visualização da câmera
        self.camera_image = Image()
        self.add_widget(self.camera_image)

        # Cria um botão para tirar fotos
        self.box_btn= BoxLayout(orientation ="horizontal")
        self.btn_capture = Button(text='Tirar Foto', size_hint=(None, None))
        self.btn_capture.bind(on_press=self.capture_image)
        
        btn_voltar= Button(text="voltar", size_hint=(None, None))
        btn_voltar.bind(on_press = self.voltar_visto)

        self.box_btn.add_widget(self.btn_capture)
        self.box_btn.add_widget(btn_voltar)
        self.add_widget(self.box_btn)


        # Inicia a atualização da visualização em tempo real
        Clock.schedule_interval(self.update_camera, 1 / 120.0)  #min 30 fps

    def update_preview(self, texture):
        self.preview_image.texture = texture

    def update_camera(self, dt):
        # Lê um quadro da câmera
        ret, frame = self.capture.read()

        if ret:
            # Atualiza a visualização em tempo real com o quadro da câmera
            texture = self.convert_frame_to_texture(frame)
            self.camera_image.texture = texture

    def capture_image(self, instance):
        # Lê um quadro da câmera
        ret, frame = self.capture.read()

        # Salva a imagem
        if ret:
            cv2.imwrite('captured_image.jpg', frame)
            print("Foto tirada e salva como captured_image.jpg")

            self.img_convertida = self.convert_image('captured_image.jpg')
            self.salva_imgdb(self.img_convertida)
            # Atualiza a pré-visualização com a foto capturada
            texture = self.convert_frame_to_texture(frame)
            self.update_preview(texture)

            rf = Roboflow(api_key="tAOZU1nzuwxLPdZHLTfy")
            project = rf.workspace().project("identificacao-de-bikes")
            model = project.version(1).model

            #cria arquivo local da imagem capturada 
            print(model.predict("captured_image.jpg", confidence=40, overlap=30).json())

            # visualização da predição da imagem
            model.predict("captured_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

            # fornece o link para sua imagem de predição
            # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())
    
    # Converte o quadro para o formato textura suportado pelo Kivy
    def convert_frame_to_texture(self, frame):
        
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture
    
    def close_popup(self, instance):
        self.box.remove_widget(self.box_aviso)

    def tela_vistoria(self,*args):
        self.box = BoxLayout(orientation ="vertical")
        self.box_preVisto= BoxLayout(orientation="horizontal")
        self.box_vistoria= BoxLayout(orientation="horizontal")
        self.box_aviso = BoxLayout(orientation="horizontal")
        popup = Popup(title='AVISO!!',
        content=Label(text='Antes de realizar a vistoria verifique se seu dispositivo possui webcam ou camera'),
        size_hint=(None, None), size=(800, 100))
        btn_previsto = Button(text="Selecionar")
        btn_visto = Button(text="Selecionar")
        btn_aviso = Button(text="X",size_hint=(None, None),size=(100,100))
        btn_aviso.bind(on_press= self.close_popup)
        btn_previsto.bind(on_press = self.preVistoria)
        btn_visto.bind(on_press=self.vistoria_bike)
        btn_voltar= Button(text="voltar",on_press=self.tela_menu)

        #self.box_aviso.add_widget(Label(text='Aviso: Antes de realizar a vistoria verifique se seu dispositivo possui webcam ou camera'))
        self.box_aviso.add_widget(popup)
        self.box_aviso.add_widget(btn_aviso)
    
        self.box.add_widget(self.box_aviso)
        self.box.add_widget(Label(text="Escolha o que deseja fazer: "))
        self.box_preVisto.add_widget(Label(text="PRÉ-VISTORIA"))
        self.box_preVisto.add_widget(btn_previsto)
        self.box_vistoria.add_widget(Label(text="VISTORIA"))
        self.box_vistoria.add_widget(btn_visto)

        self.box.add_widget(self.box_preVisto)
        self.box.add_widget(self.box_vistoria)
        
        self.box.add_widget(btn_voltar)
        self.add_widget(self.box)
    
    
    def voltar_pvisto(self,instance):
        self.box_horz.clear_widgets()
        self.box.clear_widgets()
        return self.tela_vistoria(instance)
    
    def voltar_visto(self,instance):
        
        self.box_btn.clear_widgets()
        self.clear_widgets()
        #self.limpar_tela()
        return self.tela_vistoria(instance)

    def limpar_tela(self,*args):
        self.box_preVisto.clear_widgets()
        self.box_vistoria.clear_widgets()
        self.box.clear_widgets()

    def tela_menu(self,intance):
        self.manager.current ='second'
    

    def __init__(self, **kwargs):
        super(VistoriaScreen,self).__init__(**kwargs)
    
        self.tela_vistoria()
    


if __name__ == '__main__':
    MeuApp().run()
