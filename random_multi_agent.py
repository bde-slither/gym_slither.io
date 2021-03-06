import argparse
import sys

import gym
import gym_multi_envs
from gym import wrappers, logger
from gym_multi_envs.wrappers import MultiMonitor
class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        if type(observation) is dict:
            print(observation)
        return self.action_space.sample()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('env_id', nargs='?', default='ball_paddle-v0', help='Select the environment to run')
    parser.add_argument('--obs_type', nargs='?', default='Image', help='Select observation type.')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)
    env = gym.make(args.env_id)
    n_agents = env.n_agents
    if args.env_id == 'ball_paddle-v0':
        env.set_obs_type(args.obs_type)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = '/tmp/random-agent-results'
    env = MultiMonitor(env, directory=outdir, force=True)
    env.seed(123)
    agents =[]
    for action_space in env.action_space.spaces:
        agents.append(RandomAgent(action_space))

    episode_count = 1
    reward = 0
    done = False

    for i in range(episode_count):
        ob = env.reset()
        while True:
            done = [False, False]
            actions = ()
            for i in range(n_agents):
                actions+=(agents[i].act(ob, reward, done),)
            ob, reward, done, _ = env.step(actions)
            if done[0]:
                break
            # Note there's no env.render() here. But the environment still can open window and
            # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.

    # Close the env and write monitor result info to disk
    env.close()
