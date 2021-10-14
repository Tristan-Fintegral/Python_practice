# TODO FOCUS -> Logging, clean code, doc strings, well thought out functions
import logging
from time import asctime

from scipy.stats import ks_2samp, spearmanr

logger = logging.getLogger(__name__)


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

    ks_values = ks_2samp(fo_pnl, risk_pnl)[0]

    spear_values = spearmanr(fo_pnl, risk_pnl)[0]

    logger.info(
        f"{asctime} Retrieving pla statistics, "
        f"Spearman Correlation: {spear_values} and KS metric: {ks_values}."
    )

    return spear_values, ks_values


#if __name__ == '__main__':
#    pla_stats()
