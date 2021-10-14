import logging
import scenario_generator
import option_price

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    spot_0 = 100
    vol = 0.2
    rfr = 0.005
    div = 0
    shocks = scenario_generator.generate_log_normal_shocks(
        vol=vol, num_shocks=100
    )
    spot_prices = shocks*spot_0
    for spot in spot_prices:
        shocks = option_price.create_bsm_process(
            spot=spot, vol=vol, rfr=rfr, div=div
        )

if __name__ == '__main__':
    main()

