import subprocess
from simulation.gridworld import GridWorld

if __name__ == "__main__":
    grid = GridWorld(size=(10,10))
    grid.walls = [(1,1),(1,3)]
    print(grid.walls)
    while True:
        grid.render()
        print()
        ans = input("choose an action (l,r,u,d) : ")
        subprocess.run(['clear'], shell=False)
        if ans == 'q':
            break
        else:
            grid.move(ans)
