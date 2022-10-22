

from proof_of_stake import ProofOfStake
from proof_of_work import ProofOfWork


def getConsensusStrategy(strategy):
    strategyInstance = None
    if strategy == 'pos':
        strategyInstance = ProofOfStake
    elif strategy == 'pow':
        strategyInstance = ProofOfWork

    return strategyInstance()