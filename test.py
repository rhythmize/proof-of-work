"""
test.py

Created on: 14-Jun-2020
    Author: rhythm
"""
from proof_of_work import ProofOfWork

authdata = [b'AzYRrAzFGtUesvkUOPxGGMvbOsbJCarGDNnIugELJzNTAPJEtMlgiHHFLBuYPJLk',
            b'pEgksoEuFtQkPGnppCUkcHVMMgbSyKStnjcHGmTxZXYKAEjiyseSdYznNbiLkSHK',
            b'zftqwDJPGCvgPIObWcjHkkquvcssXxulXYPEwDmxMRdeotqRADSOjqqEwKyxRYyv',
            b'vAVFIRzbPxHiyuQUIBislQyLEgvtZKaioZaGXngaWDWplUDmGHOHdzLZTjUVnLHB',
            b'jjJtOSmYHCIdBBxGeHWsccJbsVxHAsMlRRKwhEYpihsFZIAPqflOEkHCmdHPgPae']

if __name__ == '__main__':
    unwanted_chars = [0x0a, 0x0d, 0x09, 0x20]  # hex values for ['\n', '\r', '\t', ' ']
    difficulty = 8
    for a in authdata:
        print("Solving for ", a, difficulty)
        proof_of_work = ProofOfWork(a, difficulty, unwanted_chars=unwanted_chars)
        proof_of_work.solve()
