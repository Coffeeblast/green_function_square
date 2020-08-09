import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

def green(x,y,x0,y0,N):
    result=0.0
    for i in range(N):
        alpha=(i+1)*np.pi
        for j in range(N):
            beta=(j+1)*np.pi
            lam=-(alpha**2+beta**2)
            result += (4/lam)*np.sin(alpha*x0)*np.sin(alpha*x)*np.sin(beta*y0)*np.sin(beta*y)
    return result

class App():
    def __init__(self):
        self.N=2
        self.x0=0.25
        self.y0=0.5
        x=np.linspace(0,1,50)
        y=np.linspace(0,1,50)
        self.X,self.Y=np.meshgrid(x,y)
        self.fig=Figure()

        self.CreateUI()

        self.ax=Axes3D(self.fig)
        self.PlotGraph()

    def CreateUI(self):
        root=tk.Tk()
        root.wm_title("Green function")

        #### create frames
        fr_graph=tk.Frame(root,padx=5,pady=5)
        fr_graph.pack(side=tk.LEFT)
        fr_UI=tk.Frame(root)
        fr_UI.pack(side=tk.RIGHT)
        fr_display=tk.Frame(fr_UI,padx=5,pady=5,highlightbackground="black",highlightthickness=1)
        fr_display.pack(side=tk.TOP)
        fr_buttons=tk.Frame(fr_UI,padx=5,pady=5)
        fr_buttons.pack(side=tk.BOTTOM)

        #### create information labels
        self.wN_text=tk.StringVar()
        self.wN_text.set("N = "+str(self.N))
        wN=tk.Label(fr_display,textvariable=self.wN_text)
        wN.pack(side=tk.TOP)

        self.wLoc_text=tk.StringVar()
        self.wLoc_text.set("(x_0,y_0) = "+"("+str(self.x0)+","+str(self.y0)+")")
        wLoc=tk.Label(fr_display,textvariable=self.wLoc_text)
        wLoc.pack(side=tk.TOP)

        #### create canvas and navigation toolbar
        self.canvas=FigureCanvasTkAgg(self.fig,master=fr_graph)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

        toolbar=NavigationToolbar2Tk(self.canvas,fr_graph)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

        #### buttons for add / subtract N
        buttonAdd=tk.Button(master=fr_buttons,text="N --> N+1",command=self.AddN)
        buttonSub=tk.Button(master=fr_buttons,text="N --> N-1",command=self.SubN)
        buttonAdd.pack(side=tk.TOP,expand=1)
        buttonSub.pack(side=tk.TOP,expand=1)

        #### widgets for changing coordinates of the charge
        fr_coords_x=tk.Frame(master=fr_buttons)
        fr_coords_x.pack(side=tk.TOP)

        lab_x0=tk.Label(master=fr_coords_x,text="x_0: ")
        self.ent_x0=tk.Entry(master=fr_coords_x)
        lab_x0.pack(side=tk.LEFT)
        self.ent_x0.pack(side=tk.RIGHT)

        fr_coords_y=tk.Frame(master=fr_buttons)
        fr_coords_y.pack(side=tk.TOP)

        lab_y0=tk.Label(master=fr_coords_y,text="y_0: ")
        self.ent_y0=tk.Entry(master=fr_coords_y)
        lab_y0.pack(side=tk.LEFT)
        self.ent_y0.pack(side=tk.RIGHT)

        buttonSet=tk.Button(master=fr_buttons,text="Set (x0,y0)",command=self.Set)
        buttonSet.pack(side=tk.BOTTOM,expand=1)

    def PlotGraph(self):
        self.ax.cla()
        green_fun=green(self.X,self.Y,self.x0,self.y0,self.N)
        self.ax.plot_surface(self.X,self.Y,green_fun)
        self.ax.plot(np.array([self.x0]),np.array([self.y0]),np.array([0.0]),marker='o',markersize=8,color="red")
        self.ax.plot(np.array([self.x0,self.x0]),np.array([0,1]),np.array([0,0]),color="red",linewidth=1,marker="")
        self.ax.plot(np.array([0,1]),np.array([self.y0,self.y0]),np.array([0,0]),color="red",linewidth=1,marker="")
        zmin,zmax=self.ax.get_zlim()
        self.ax.plot(np.array([self.x0,self.x0]),np.array([self.y0,self.y0]),np.array([zmin,zmax]),color="red",linewidth=1,marker="")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.set_title("N = "+str(self.N))
        self.canvas.draw()

        self.wN_text.set("N = "+str(self.N))
        self.wLoc_text.set("(x_0,y_0) = "+"("+str(self.x0)+","+str(self.y0)+")")

    def AddN(self):
        if self.N<=200:
            self.N+=1
            print('N=',self.N)
            self.PlotGraph()

    def SubN(self):
        if self.N>=2:
            self.N-=1
            print('N=',self.N)
            self.PlotGraph()

    def Set(self):
        try:
            x0=float(self.ent_x0.get())
            y0=float(self.ent_y0.get())
            self.x0,self.y0=float(x0),float(y0)
            self.wLoc_text.set("(x_0,y_0) = "+"("+str(self.x0)+","+str(self.y0)+")")
            self.PlotGraph()
        except ValueError:
            messagebox.showinfo("Error","Enter x_0, and y_0, that are numbers!")

def main():
    myApp=App()
    tk.mainloop()

main()