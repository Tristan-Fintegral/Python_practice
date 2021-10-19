import time
import logging
import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def generate_log_normal_shocks(vol, num_shocks=780):
    """Generate a vector of log normal shocks with given volatility.

    Log shock = exp(vol * N(0,1))
    S1 = S0 * (Log shock)

    :param float vol: Volatility in standard units
    :param int num_shocks: Number of shocks to produce
    :return [int]: Vector of shocks
    """
    rand_norm_vector = np.random.normal(loc=0, scale=1, size=num_shocks)
    shock_vector = np.exp(vol * rand_norm_vector)

    return shock_vector


def timer(dont_log):
    logger.info(f'Accepting arguments for dont log for timer: {dont_log}.')

    def wrap(outer_func):
        logger.info(f'Creating timed function for {outer_func}.')

        def inner(*args, **kwargs):
            logger.info(f'Running modified function {inner}.')
            t1 = time.time()
            func_outputs = outer_func(*args, **kwargs)
            t2 = time.time()
            elapsed_time = t2 - t1
            if not dont_log:
                logger.info(f'Modified function ran in {elapsed_time} seconds.')
            return func_outputs

        logger.info(f'Returning modified function {inner}.')
        return inner

    return wrap


@timer(dont_log=True)
def waste_o_time(dragon_fruit):
    logger.info(f'Your dragon fruit is called {dragon_fruit}.')
    time.sleep(np.random.uniform(0,1))
    return dragon_fruit*10


def main():

    # x = generate_log_normal_shocks(vol=0.1, num_shocks=1000000)
    # timed_shocks = timer(generate_log_normal_shocks)
    # x2 = timed_shocks(vol=0.1, num_shocks=1000000)
    d_fruit = waste_o_time(dragon_fruit='tony')
    temp = 1


if __name__ == '__main__':
    main()
