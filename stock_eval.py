# ---------------------------------------------- PROGRAMA: LUCRO DA AÇÃO --------------------------------------------- #
#                  Este programa foi criado para responder ao desafio de programação da empresa Atados.                #
#                                                   2020@JoseSalgueiro                                                 #
#                                             Todos os Direitos Reservados                                             #
# -------------------------------------------------------------------------------------------------------------------- #


# ----- IMPORTS ----- #
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk

# ----- Variáveis Globais ----- #
XL_FONT = ("Verdana", 16)
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


# ---------------------------- GUIAPP ------------------------- #
#    Classe core do aplicativo que coordena todas as páginas    #
# ------------------------------------------------------------- #
class GuiApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_state('zoomed')
        tk.Tk.iconbitmap(self, default="images/atados.ico")
        tk.Tk.wm_title(self, "Desafio de Programação Atados - José Salgueiro")
        container = tk.Frame(self, width=1350, height=750)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container["bg"] = "#ffffff"

        # ----- Incluir aqui telas adicionais, se necessário (para efeitos de escalabilidade) ----- #
        self.frames = {}
        for F in (StartPage,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# -------------------------- StartPage ------------------------ #
#                   Tela Inicial da Aplicação                   #
# ------------------------------------------------------------- #
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ffffff")
        print("Console - O Lucro da Ação.")
        print("\n\nFECHAR ESTA JANELA ENCERRA A APLICAÇÃO!!!")
        print("\n2020@JoséSalgueiro - Todos os Direitos Reservados!!!")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.main_frame = tk.Frame(self, background="white")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")
        # Usar estas variáveis de instância para inicializar os gráficos
        self.fig1 = None
        self.ax1 = None
        self.canvas1 = None
        self.x1list = []
        self.y1list = []
        self.fig2 = None
        self.ax2 = None
        self.canvas2 = None
        self.x2list = []
        self.y2list = []

        # ----- Barra de Topo com o ícone ----- #
        self.top_frame = tk.Frame(self.main_frame, bg="#4A4A4A")
        self.top_frame.grid(row=0, column=0, sticky='E,W')
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        atados_logo = Image.open("images/atados-small.PNG")
        render = ImageTk.PhotoImage(atados_logo)
        img = tk.Label(self.top_frame, image=render, bg="#4A4A4A")
        img.image = render
        img.grid(row=0, column=0, sticky=tk.W)
        program_title = tk.Label(self.top_frame, text="O LUCRO DA AÇÃO",
                                 font=LARGE_FONT, bg="#4A4A4A", foreground="#68d1e9")
        program_title.grid(row=0, column=1, sticky='E,W')

        # ----- Area de Trabalho ----- #
        self.body_frame = tk.Frame(self.main_frame, bg='#ffffff')
        self.body_frame.grid(row=1, column=0, sticky='N,S,E,W')
        self.body_frame.grid_rowconfigure(4, weight=1)
        self.body_frame.grid_columnconfigure(1, weight=1)

        self.input_frame = tk.Frame(self.body_frame, bg="#4A4A4A")
        self.input_frame.grid(row=0, column=0, sticky="news", columnspan=2, pady=20)
        self.input_frame.columnconfigure(1, weight=1)

        self.seph1 = ttk.Separator(self.body_frame, orient="horizontal")
        self.seph1.grid(column=0, row=2, columnspan=2, pady=10, sticky='we')

        self.output_frame = tk.Frame(self.body_frame, bg="#4A4A4A")
        self.output_frame.grid(row=4, column=0, sticky="news", columnspan=2, pady=(20, 5))
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(2, weight=1)
        self.output_frame.grid_rowconfigure(4, weight=1)

        # ----- Area de Input ----- #
        input_label = ttk.Label(self.input_frame, background="#4A4A4A", foreground="#68d1e9", font=LARGE_FONT,
                                text="Insira os preços diários das ações separadas por espaços (ex: 15 23 35 64 ):")
        input_label.grid(column=0, row=0, pady=(10, 10), padx=(10, 5), sticky=tk.W)
        self.value_list = tk.StringVar()
        self.tx_value_list = tk.Entry(self.input_frame, textvariable=self.value_list)
        self.tx_value_list.grid(column=1, row=0, pady=10, padx=(0, 20), sticky="news")
        self.photo_start = tk.PhotoImage(file=r"images//start.png")
        self.button_start = tk.Button(self.input_frame, image=self.photo_start, compound=tk.CENTER, width=40, height=40,
                                      command=lambda: self.start_calculations())
        self.button_start.grid(row=0, column=2, padx=(0, 20), pady=5)

        # ----- Area de Resultados ----- #
        self.output_label = ttk.Label(self.output_frame, background="#4A4A4A", foreground="#68d1e9", font=LARGE_FONT,
                                      text="RESULTADOS:")
        self.output_label.grid(column=0, row=0, pady=(10, 10), padx=(10, 5), columnspan=3, sticky=tk.W)
        self.plot1_label = ttk.Label(self.output_frame, background="#4A4A4A", foreground="#68d1e9", font=NORM_FONT,
                                     text="LUCRO MÁXIMO OBTIDO PARA CADA VALOR DIÁRIO DE AÇÃO:")
        self.plot1_label.grid(column=0, row=2, pady=(5, 10), padx=(10, 5), sticky=tk.W)
        self.plot2_label = ttk.Label(self.output_frame, background="#4A4A4A", foreground="#68d1e9", font=NORM_FONT,
                                     text="LUCROS OBTIDOS COM VENDAS DE AÇÃO NO DIA X:")
        self.plot2_label.grid(column=2, row=2, pady=(5, 10), padx=(10, 5), sticky=tk.W)

        self.create_plots()  # Inicia os gráficos

        # ----- Rodapé ----- #
        self.footer1_label = ttk.Label(self.body_frame, background="#ffffff", foreground="#4A4A4A", font=NORM_FONT,
                                       text="2020@JOSESALGUEIRO", anchor="center")
        self.footer1_label.grid(column=0, row=6, columnspan=3, sticky="EW")
        self.footer2_label = ttk.Label(self.body_frame, background="#ffffff", foreground="#4A4A4A", font=NORM_FONT,
                                       text="TODOS OS DIREITOS RESERVADOS.", anchor="center")
        self.footer2_label.grid(column=0, row=7, columnspan=3, sticky="EW")

    def start_calculations(self):
        if len(self.tx_value_list.get()) == 0:
            self.popupmsg("Please add the stock values in the textbox separated by spaces.")
        else:
            self.process_values()

    def process_values(self):
        #  Se as listas não estiverem vazias, apagá-las
        if self.x1list:
            self.x1list.clear()
        if self.y1list:
            self.y1list.clear()
        if self.x2list:
            self.x2list.clear()
        if self.y2list:
            self.y2list.clear()

        try:
            strvalue_list = self.tx_value_list.get().split()
            stockvalue_list = [float(strvalue) for strvalue in strvalue_list]
            self.x1list = [x + 1 for x in range(0, len(strvalue_list))]

            # Para cada valor diário de ação, calcular os lucros possiveis. Isto é feito subtraindo o valor atual a cada
            # valor subsquente na lista.
            sublist = [stockvalue_list[i:] for i in range(0, len(stockvalue_list)-1)]
            profitlist = []
            for valuelist in sublist:
                init_value = valuelist[0]
                profit_sublist = [value - init_value for value in valuelist]
                profitlist.append(profit_sublist)

            self.y1list = [max(profits) for profits in profitlist]
            self.y1list.append(0.0)
            if max(self.y1list) == 0.0:
                self.output_label["text"] = "RESULTADOS: É IMPOSSIVEL OBTER LUCRO NESTE INTERVALO DE TEMPO!!!"
            else:
                maxprofit_day = self.y1list.index(max(self.y1list)) + 1  # Calcula o dia com o máximo lucro
                self.y2list = profitlist[maxprofit_day - 1]  # Lê os lucros possiveis para esse dia
                self.x2list = [maxprofit_day + i for i in range(0, len(self.y2list))]
                max_sellprofitday = self.y2list.index(max(self.y2list)) + maxprofit_day
                self.output_label["text"] = "RESULTADOS: O MAIOR LUCRO É OBTIDO QUANDO COMPRAMOS A AÇÂO NO " \
                                            + str(maxprofit_day) + "º DIA E VENDEMOS NO " + str(max_sellprofitday) \
                                            + "º dia!"
                self.create_plots()
        except ValueError:
            self.popupmsg("Erro lendo lista de dados. Por favor insira os valores das ações separados por espaços. " \
                          "Ex: '15 35 64 22'")

    def popupmsg(self, msg):
        popup = tk.Tk()

        def leavemini():
            popup.destroy()

        popup.wm_title("!")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", padx=50, pady=20)
        B1 = ttk.Button(popup, text="OK!", command=leavemini)
        B1.pack(side="bottom", pady=(0, 20))
        popup.mainloop()

    def create_plots(self):
        font = {'family': 'sans-serif', 'sans-serif': ['Tahoma'], 'weight': 'bold', 'size': 8}
        matplotlib.rc('font', **font)

        self.fig1 = Figure(figsize=(6, 4), dpi=100)
        self.ax1 = self.fig1.add_subplot(1, 1, 1)
        self.fig1.legend(loc=10, fontsize="small")
        self.ax1.bar(np.asarray(self.x1list), np.asarray(self.y1list), label=["Lucro Maximo"], color="#68d1e9")
        self.ax1.set_xlabel("Dia de Compra da Ação")
        self.ax1.set_ylabel("Lucro máximo Possível")
        for i, v in enumerate(self.y1list):
            self.ax1.text(self.x1list[i] - 0.15, v + 0.01, str(v), color='blue', fontweight='bold')
        if not self.x1list:
            self.ax1.set_xticks(np.arange(0, 5, 1))
            self.ax1.set_yticks(np.arange(0, 5, 1))
        else:
            self.ax1.set_xticks(np.asarray(self.x1list))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.output_frame)
        self.canvas1.get_tk_widget().grid(row=4, column=0, padx=15, pady=10, sticky='NSEW')

        self.fig2 = Figure(figsize=(6, 4), dpi=100)
        self.ax2 = self.fig2.add_subplot(1, 1, 1)
        self.fig2.legend(loc=10, fontsize="small")
        self.ax2.bar(self.x2list, self.y2list, label=["Lucro"], color="#68d1e9")
        self.ax2.set_xlabel("Dia de Venda da Ação")
        self.ax2.set_ylabel("Lucro Obtido")
        for i, v in enumerate(self.y2list):
            self.ax2.text(self.x2list[i] - 0.15, v + 0.01, str(v), color='blue', fontweight='bold')
        if not self.x2list:
            self.ax2.set_xticks(np.arange(0, 5, 1))
            self.ax2.set_yticks(np.arange(0, 5, 1))
        else:
            self.ax2.set_xticks(np.asarray(self.x2list))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.output_frame)
        self.canvas2.get_tk_widget().grid(row=4, column=2, padx=15, pady=10, sticky='NSEW')


# Define a App
app = GuiApp()
app.geometry("1350x800")

# -------------------#
#    Inicia o GUI    #
# -------------------#
app.mainloop()
