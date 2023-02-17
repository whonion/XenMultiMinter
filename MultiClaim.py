from web3 import Web3
from web3.middleware import geth_poa_middleware
from loguru import logger
from sys import stderr
from multiprocessing.dummy import Pool
ABI = ''
c_addr = ''
XEN_MAIN = '0x06450dEe7FD2Fb8E39061434BAbCFC05599a6Fb8'
XEN_BSC = '0x2AB0e9e4eE70FFf1fB9D67031E44F6410170d00e'
XEN_MATIC = '0x2AB0e9e4eE70FFf1fB9D67031E44F6410170d00e'
XEN_AVAX = '0xC0C5AA69Dbe4d6DDdfBc89c0957686ec60F24389'
XEN_EVMOS = '0x2AB0e9e4eE70FFf1fB9D67031E44F6410170d00e'
XEN_FTM='0xeF4B763385838FfFc708000f884026B8c0434275'
XEN_OKX='0x1cC4D981e897A3D2E7785093A648c0a75fAd0453'
XEN_ARB = 'nil'
XEN_OPT = 'nil'
rpc_main = 'https://rpc.ankr.com/eth'
rpc_bsc = 'https://rpc.ankr.com/bsc'
rpc_matic = 'https://rpc.ankr.com/polygon'
rpc_avax = 'https://rpc.ankr.com/avalanche'
rpc_arb = 'https://rpc.ankr.com/avalanche'
rpc_opt = 'https://mainnet.optimism.io'
rpc_evmos = 'https://eth.bd.evmos.org:8545'
rpc_ftm='https://rpc.ankr.com/fantom'
rpc_okx='https://exchainrpc.okex.org'

logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white>"
                          " | <level>{level: <8}</level>"
                          " | <cyan>{line}</cyan>"
                          " - <white>{message}</white>")


def send_tx(private_key: str):
    address = None

    try:
        address = Web3.toChecksumAddress(w3.eth.account.from_key(private_key).address)
        transaction = contract.functions.claimMintReward() \
            .buildTransaction({
                'gas': 354853,
                'value': w3.toWei(0.0005, 'ether'),
                'gasPrice': Web3.toWei(gwei, 'gwei'),
                'from': address,
                'nonce': w3.eth.getTransactionCount(address)
            })

        signed_txn = w3.eth.account.signTransaction(transaction,
                                                    private_key=private_key)
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))

        logger.info(f'{address} | {tx_hash}')

    except Exception as error:
        logger.error(f'{address} | {error}')


if __name__ == '__main__':
    print('-' * 108)
    print((' '*46)+'XEN MULTI CLAIMER'+(' '*46))
    print('-' * 108)
    with open('accounts.txt', encoding='utf-8-sig') as file:
        private_keys = [row.strip() for row in file]

    with open('ABI.txt', 'r', encoding='utf-8-sig') as file:
        ABI = file.read().strip().replace('\n', '').replace(' ', '')
    print('Input chain:\n')
    print('1.Mainnet\n2.BSC Chain\n3.Polygon mainnet\n4.AVAX C-hain\n5.Evmos\n6.Fantom\n7.OKX\n')
    rpc_ch = int(input('Input Chain for mint XEN: '))
    if rpc_ch == 1:
        rpc = rpc_main
        c_addr = XEN_MAIN
    elif rpc_ch == 2:
        rpc = rpc_bsc
        c_addr = XEN_BSC
    elif rpc_ch == 3:
        rpc = rpc_matic
        c_addr = XEN_MATIC
    elif rpc_ch == 4:
        rpc= rpc_avax
        c_addr = XEN_AVAX
    elif rpc_ch == 5:
        rpc= rpc_evmos
        c_addr = XEN_EVMOS
    elif rpc_ch == 6:
        rpc= rpc_ftm
        c_addr = XEN_FTM
    elif rpc_ch == 7:
        rpc= rpc_okx
        c_addr = XEN_OKX

    w3 = Web3(Web3.HTTPProvider(rpc))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract = w3.eth.contract(address=Web3.toChecksumAddress(c_addr),
                               abi=ABI)
    logger.info(f'Загружено {len(private_keys)} кошельков')
    gwei = int(input('Input GWEI: '))

    with Pool(processes=len(private_keys)) as executor:
        executor.map(send_tx, private_keys)

    input('Press Enter To Exit..')