from codrone_edu.swarm import *

swarm = Swarm()

swarm.auto_connect()
swarm.start_threading()

swarm.all_takeoff()
#swarm.all_hover(2)
swarm.all_move(p=40, seconds=1.5, r=0, y=0, t=0)
#swarm.all_turn_degree(180)
#swarm.all_move(p=40, seconds=1, r=0, y=0, t=0)
#swarm.all_turn_degree(180)

swarm.all_land()

swarm.close_all()
