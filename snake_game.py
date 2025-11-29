import tkinter as tk, random

S=20; W=30; H=20   # cell size, width, height

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(tk.Tk(), width=W*S, height=H*S, bg="black", highlightthickness=0)
        self.master.title("Snake <100 lines")
        self.pack()
        self.bind_all("<Key>", self.key)
        self.reset()
        self.mainloop()

    def reset(self):
        self.snake=[(5,10),(4,10),(3,10)]
        self.dir=(1,0)
        self.food=self.new_food()
        self.after_id=None
        self.run=True
        self.step()

    def new_food(self):
        cells=[(x,y) for x in range(W) for y in range(H) if (x,y) not in self.snake]
        return random.choice(cells)

    def key(self,e):
        k=e.keysym
        d={"Up":(0,-1),"Down":(0,1),"Left":(-1,0),"Right":(1,0)}
        if k in d:
            nx,ny=d[k]
            if (nx,ny)!=(-self.dir[0],-self.dir[1]):
                self.dir=(nx,ny)
        if k.lower()=="r": self.reset()

    def step(self):
        if not self.run: return
        x,y=self.snake[0]
        dx,dy=self.dir
        nx,ny=(x+dx)%W,(y+dy)%H
        if (nx,ny) in self.snake:
            self.game_over()
            return
        self.snake.insert(0,(nx,ny))
        if (nx,ny)==self.food:
            self.food=self.new_food()
        else:
            self.snake.pop()

        self.draw()
        self.after_id=self.after(100, self.step)

    def draw(self):
        self.delete("all")
        # food
        fx,fy=self.food
        self.create_rectangle(fx*S,fy*S,fx*S+S,fy*S+S,fill="red")
        # snake
        for i,(x,y) in enumerate(self.snake):
            c="white" if i==0 else "green"
            self.create_rectangle(x*S,y*S,x*S+S,y*S+S,fill=c)

    def game_over(self):
        self.run=False
        self.delete("all")
        self.create_text(W*S/2,H*S/2,text="GAME OVER\nR = Restart",fill="white",font=("Consolas",20))

Snake()
