import pandas as pd

from pymgrid_config import *


if __name__ == "__main__":
    microgrid = create_microgrid()

    for j in range(10):
        # choose random action for microgrid
        action = microgrid.sample_action(strict_bound=True)
        microgrid.run(action)

    print(microgrid.get_log(drop_singleton_key=True))
