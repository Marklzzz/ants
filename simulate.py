from controller import Env
from tqdm import tqdm
import json

import config


def start():
    config.update()
    env = Env(1 / config.FPS)
    steps = 10000
    with open('file.txt', 'w') as f:
        for step in tqdm(range(steps)):
            env.step()
            d = dict()
            d['ants'] = [{
                'pos': ant.pos.astype(int).tolist(),
                'current_target': ant.current_target #saves current target for later vizualization
            } for ant in env.ants]
            d['targets'] = [{'pos': target.pos.astype(int).tolist(),
                             'type': target.target_type,
                             'size': target.size,
                             'health': target.health} for target in env.targets]
            f.write(json.dumps(d) + '\n')





