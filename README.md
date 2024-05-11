# Path_Planning
A* algorith for an agent to find its way to eat the apples in a maze. Apples represent the stations to stop. Task is the stop at the stations while finding the shortest way. 

Heuristic function i used for this task =

**furtherest station (apple) distance from current situation** + 
**distance of furherest station from the furtherest station**

# Examples
- RED - Stations (Apples)
- BLUE - Agent
- BLACK - WALLS
- GREEN - SOLVED PATH

![Screenshot from 2024-05-11 21-22-04](https://github.com/9Xxi8Q4f/a--labrinth/assets/89272933/f63bae7c-96c1-4f29-b175-56a08b8189db)
![Screenshot from 2024-05-11 21-23-41](https://github.com/9Xxi8Q4f/a--labrinth/assets/89272933/500b322a-ea6b-4d23-be40-a591513f3a43)

### Issues and TODO

- Is not that efficient, takes long to compute, needs rewrite (this is a pretty old project of mine)
- Need better visiulizing with animations
- Node class need more features to keep the algorithm more simple
- Well i can't imageine a better heuristic than this lol

