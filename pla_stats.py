# TODO FOCUS -> Logging, clean code, doc strings, well thought out functions
import logging
from scipy.stats import ks_2samp, spearmanr

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def pla_stats(fo_pnl, risk_pnl):
    """
    :param fo_pnl: HTPL is produced by revaluing the positions held at the end of the previous day using the market data
    at the end of the current day.
    :param risk_pnl: RTPL is the daily trading desk-level P&L produced by the valuation engine of the trading desk’s
    risk management model.
    :return Spearman and ks values

    kolmogorov-smirnov(ks): test metric to assess the similarity of the distributions of RTPL and HPL.
    Spearman Correlation: metric to assess correlation between RTPL and HPL.

    """
    logger.info(
        f"Calculating pla statistics for fo_pnl and risk_pnls of "
        f"length {len(fo_pnl)} & {len(risk_pnl)}."
    )
    ks_values = ks_2samp(fo_pnl, risk_pnl).statistic
    spear_values = spearmanr(fo_pnl, risk_pnl).correlation

    return spear_values, ks_values


def main():
    ret = pla_stats([1,2,3,4,5], [2,3,4,5,5])
    logger.info(f'PLA stats returned {ret}.')


if __name__ == '__main__':
   main()
