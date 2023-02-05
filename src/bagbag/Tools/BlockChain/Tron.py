from __future__ import annotations

import tronpy
from tronpy import Tron as TronAPI
from tronpy.providers import HTTPProvider

import traceback

from ... import Http, Json, Re, Lg, Time 

assetDecimals = {}
contractDecimals = {}

class tronAssetInfo():
    def __init__(self) -> None:
        self.raw_data:dict = None 
        self.TokenID:int = None 
        self.Precision:int = None 
        self.Description:int = None
        self.DateCreated:int = None  
        self.Abbr:str = None 
        self.Email:str = None
        self.Website:str = None 
        self.Github:str = None 
        self.URL:str = None 
        self.Name:str = None
        self.OwnerAddress:str = None 
        self.WhitePaper:str = None 
        self.TotalSupply:int = None 
        self.SocialMedia:list = None 
    
    def __str__(self) -> str:
        m = f"tronAssetInfo("
        m += f"TokenID={self.TokenID} "
        m += f"Precision={self.Precision} "
        m += f"Description={self.Description} "
        m += f"DataCreated={self.DateCreated}) "
        m += f"Abbr={self.Abbr} "
        m += f"Email={self.Email} "
        m += f"Website={self.Website} "
        m += f"Github={self.Github} "
        m += f"URL={self.URL} "
        m += f"Name={self.Name} "
        m += f"OwnerAddress={self.OwnerAddress} "
        m += f"WhitePaper={self.WhitePaper} "
        m += f"TotalSupply={self.TotalSupply} "
        m += f"SocialMedia={self.SocialMedia}"
        m += ")"

        return m

class TronAsset():
    def __init__(self, name:str) -> None:
        self.name = name 
        
    
    def Name(self) -> str:
        return self.name 
    
    def Info(self) -> tronAssetInfo:
        content = Http.Get("https://apilist.tronscanapi.com/api/token?id=%d&showAll=1" % self.name, timeoutRetryTimes=999).Content
        contentj = Json.Loads(content)

        tronassetinfo = tronAssetInfo()

        tronassetinfo.raw_data = contentj

        rd = None 
        for rd in contentj['data']:
            if self.name == rd['tokenID']:
                break 
        if rd == None:
            raise Exception(f"找不到trc10的info:{self.name}\n服务器返回的数据为:\n{content}")

        tronassetinfo.TokenID = rd['tokenID'] # asset_name 
        tronassetinfo.Precision = rd['precision']
        tronassetinfo.Description = rd['description']
        tronassetinfo.DateCreated = rd['dateCreated']
        tronassetinfo.Abbr = rd['abbr']
        tronassetinfo.Email = rd['email']
        tronassetinfo.Website = rd['website']
        tronassetinfo.Github = rd['github']
        tronassetinfo.URL = rd['url']
        tronassetinfo.Name = rd['name']
        tronassetinfo.OwnerAddress = rd['ownerAddress']
        tronassetinfo.WhitePaper = rd['white_paper']
        tronassetinfo.TotalSupply = rd['totalSupply']
        tronassetinfo.SocialMedia = rd['social_media']

        return tronassetinfo

class tronContractInfo():
    def __init__(self) -> None:
        self.raw_data:dict = None 
        self.ContractAddress:str = None 
        self.ContractName:str = None 
        self.Symbol:str = None 
        self.Name:str = None 
        self.IssueAddress:str = None 
        self.IssueTime:int = None 
        self.Decimals:int = None 
        self.HomePage:str = None
        self.TokenDesc:str = None 
        self.Email:str = None 
        self.SocialMediaList:list = None 
        self.WhitePaper:str = None 
        self.GitHub:str = None 
        self.TotalSupplyWithDecimals:int = None 
    
    def __str__(self) -> str:
        m = "tronContractInfo("
        m += f"ContractAddress={self.ContractAddress} "
        m += f"ContractName={self.ContractName} "
        m += f"Symbol={self.Symbol} "
        m += f"Name={self.Name} "
        m += f"IssueAddress={self.IssueAddress} "
        m += f"IssueTime={self.IssueTime} "
        m += f"Decimals={self.Decimals} "
        m += f"HomePage={self.HomePage} "
        m += f"TokenDesc={self.TokenDesc} "
        m += f"Email={self.Email} "
        m += f"SocialMediaList={self.SocialMediaList} "
        m += f"WhitePaper={self.WhitePaper} "
        m += f"GitHub={self.GitHub} "
        m += f"TotalSupplyWithDecimals={self.TotalSupplyWithDecimals}"
        m += ")"

        return m

class TronContract():
    def __init__(self, address:str) -> None:
        self.address = address 
    
    def Address(self) -> str:
        return self.address 
    
    def Info(self) -> tronContractInfo:
        content = Http.Get("https://apilist.tronscanapi.com/api/token_trc20?contract=%s&showAll=1" % self.address, timeoutRetryTimes=999).Content
        contentj = Json.Loads(content)

        troncontractinfo = tronContractInfo()
        troncontractinfo.raw_data = contentj

        rd = None 
        for rd in contentj['trc20_tokens']:
            if self.address == rd['contract_address']:
                break 
        if rd == None:
            raise Exception(f"找不到trc20的info:{self.address}\n服务器返回的数据为:\n{content}")

        troncontractinfo.ContractAddress = rd['contract_address']
        troncontractinfo.ContractName = rd['contract_name']
        troncontractinfo.Symbol = rd['symbol']
        troncontractinfo.Name = rd['name']
        troncontractinfo.IssueAddress = rd['issue_address']
        troncontractinfo.IssueTime = Time.Strptime(rd['issue_time'])
        troncontractinfo.Decimals = rd['decimals']
        troncontractinfo.HomePage = rd['home_page']
        troncontractinfo.TokenDesc = rd['token_desc']
        troncontractinfo.Email = rd['email']
        troncontractinfo.SocialMediaList = rd['social_media_list']
        troncontractinfo.WhitePaper = rd['white_paper']
        troncontractinfo.GitHub = rd['git_hub']
        troncontractinfo.TotalSupplyWithDecimals = rd['total_supply_with_decimals'] 

        return troncontractinfo
    
    def __str__(self) -> str:
        return f"TronContract(Address={self.address})"

class tronTranscation():
    def __init__(self, trx:dict, tron:Tron, block:tronBlock) -> None:
        # Lg.Trace()
        self.block:tronBlock = block
        self.tron:Tron = tron
        self.trx:dict = trx

        self.contract:dict = trx["raw_data"]["contract"][0]
        
        self.ContractRet:str = trx['ret'][0]['contractRet']
        self.Asset:TronAsset = None 
        self.Contract:TronContract = None 
        self.Decimals:int = None 

        self.TxID:str = trx["txID"]
        self.Type:str = self.contract["type"]
        # Lg.Trace()

        self.Expiration:int = None 
        if 'expiration' in trx["raw_data"]:
            self.Expiration = trx["raw_data"]["expiration"]
        
        self.Timestamp:int = None 
        if "timestamp" in trx["raw_data"]:
            self.Timestamp = trx["raw_data"]["timestamp"]

        if self.contract["type"] == "TransferContract":
            # Lg.Trace()
            self.Amount:int = None 
            if "amount" in self.contract["parameter"]["value"]:
                self.Amount = self.contract["parameter"]["value"]["amount"] / (10 ** 6)
            self.FromAddress:str = self.contract["parameter"]["value"]["owner_address"]
            self.ToAddress:str = self.contract["parameter"]["value"]["to_address"]

        elif self.contract["type"] == "TransferAssetContract":
            # Lg.Trace()
            self.Asset:TronAsset = TronAsset(self.contract["parameter"]["value"]["asset_name"])
            self.Amount:str = self.contract["parameter"]["value"]["amount"]
            self.FromAddress:str = self.contract["parameter"]["value"]["owner_address"]
            self.ToAddress:str = self.contract["parameter"]["value"]["to_address"]

            if not self.Asset.Name() in assetDecimals:
                # Lg.Trace()
                assetDecimals[self.Asset.Name()] = self.getAssetDecimals(self.Asset.Name())
            
            # Lg.Trace()
            # decimals = assetDecimals[self.AssetName]
            # if decimals != 0:
            #     # Lg.Trace()
            #     # txinfo["amount"] = txinfo["amount"] / (10 ** decimals)
            #     self.Decimals = 10 ** decimals
            self.Decimals:int = assetDecimals[self.Asset.Name()]

        elif self.contract["type"] == "TriggerSmartContract":
            # Lg.Trace()
            self.Contract:TronContract = TronContract(self.contract["parameter"]["value"]["contract_address"])

            if 'data' in self.contract["parameter"]["value"]:
                data = self.contract["parameter"]["value"]['data'] 

                if data[:8] in [
                    "a9059cbb", # transfer 
                    "23b872dd", # transferFrom
                ]:
                    if self.Contract.Address() not in contractDecimals:
                        try:
                            contractDecimals[self.Contract.Address()] = self.getContractDecimals(self.Contract.Address())
                        except Exception as e:
                            Lg.Warn(f"获取合约{self.Contract.Address()}精度失败:\n" + traceback.format_exc())
                            contractDecimals[self.Contract.Address()] = None 

                # transfer
                if data[:8] == "a9059cbb":
                    # Lg.Trace()
                    self.FromAddress:str = self.contract["parameter"]["value"]["owner_address"]
                    self.ToAddress:str = tronpy.keys.to_base58check_address('41' + (data[8:72])[-40:])
                    self.Amount:int = int(data[-64:], 16)

                    # if contractDecimals[self.ContractAddress] != None:
                    #     # Lg.Trace()
                    #     if contractDecimals[self.ContractAddress] <= 18:
                    #         self.Decimals = 10 ** contractDecimals[self.ContractAddress] 
                    #         # Lg.Trace()
                    self.Decimals:int = contractDecimals[self.Contract.Address()]

                # transferFrom
                elif data[:8] == "23b872dd":
                    self.FromAddress:str = tronpy.keys.to_base58check_address('41' + (data[8:72])[-40:])
                    self.ToAddress:str = tronpy.keys.to_base58check_address('41' + (data[72:136])[-40:])
                    self.Amount:int = int(data[-64:], 16) 

                    # if contractDecimals[self.ContractAddress] != None:
                    #     if contractDecimals[self.ContractAddress] <= 18:
                    #         self.Decimals = 10 ** contractDecimals[self.ContractAddress]
                    self.Decimals:int = contractDecimals[self.Contract.Address()]
    
    def __str__(self) -> str:
        m = "tronTranscation("
        m += f"TxID={self.TxID} "
        m += f"Type={self.Type} "
        m += f"ContractRet={self.ContractRet} "
        m += f"Asset={self.Asset} "
        m += f"Contract={self.Contract} "
        m += f"Decimals={self.Decimals} "
        m += f"Expiration={self.Expiration} "
        m += f"Timestamp={self.Timestamp} "
        m += f"Amount={self.Amount} "
        m += f"FromAddress={self.FromAddress} "
        m += f"ToAddress={self.ToAddress}"
        m += ")"

        return m

    def getAssetDecimals(self, assetName:str) -> int:
        data = Http.PostJson(self.tron.nodeServer + "/wallet/getassetissuebyid", {'value': assetName, 'visible': True}, timeoutRetryTimes=999999).Content.replace('\n', '')
        if '"precision"' in data:

            res = []
            for i in data:
                if i in r'''1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM{}" :,''':
                    res.append(i)
            
            data = ''.join(res)

            # data = String(data).Filter(r'''1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM{}" :,''')
            try:
                c = Json.Loads(data)
                precision = c["precision"]
            except:
                precision = int(Re.FindAll('"precision": *([0-9]+)', data)[0][1])

            
            return precision
        else:
            return 0

    def getContractDecimals(self, contract:str) -> int:
        errcount = 0
        while True:
            try:
                contractobj = self.tron.tron.get_contract(contract)
                if hasattr(contractobj.functions, 'decimals'):
                    return contractobj.functions.decimals()
                else:
                    return self.getContractDecimalsFromWeb(contract)
            except ValueError as e:
                if 'can not call a contract without ABI' in str(e):
                    while True:
                        try:
                            return self.getContractDecimalsFromWeb(contract)
                        except Exception as e:
                            errcount += 1
                            if errcount > 5:
                                raise e
                else:
                    raise e
            except Exception as e:
                errcount += 1
                if errcount > 5:
                    raise e
    
    def getContractDecimalsFromWeb(self, contract:str) -> int:
        # Lg.Trace("从web获取精度")
        content = Http.Get("https://apilist.tronscanapi.com/api/token_trc20?contract=%s&showAll=1" % contract, timeoutRetryTimes=999).Content
        contentj = Json.Loads(content)
        if contentj['total'] == 0:
            return None  
        
        rd = None 
        for rd in contentj['trc20_tokens']:
            if contract == rd['contract_address']:
                break 
        if rd == None:
            return None  
        
        return int(rd['decimals'])

class tronBlock():
    def __init__(self, block:dict, tron:Tron) -> None:
        self.tron:Tron = tron
        # Lg.Trace()

        self.block:dict = block 
        self.BlockID:str = block['blockID']
        self.TxTrieRoot:str = block['block_header']['raw_data']['txTrieRoot']
        self.WitnessAddress:str = block['block_header']['raw_data']['witness_address']
        self.ParentHash:str = block['block_header']['raw_data']['parentHash']

        # Lg.Trace()

        self.Number:int = None 
        if 'number' in block['block_header']['raw_data']:
            self.Number = block['block_header']['raw_data']['number']

        self.Timestamp:int = None
        if 'timestamp' in block['block_header']['raw_data']:
            self.Timestamp = block['block_header']['raw_data']['timestamp']
        
        self.WitnessSignature:str = None 
        if 'witness_signature' in block['block_header']['raw_data']:
            self.WitnessSignature = block['block_header']['witness_signature']
        
        # Lg.Trace()
    
    def __str__(self) -> str:
        m = "tronBlock("
        m += f"BlockID={self.BlockID} "
        m += f"TxTrieRoot={self.TxTrieRoot} "
        m += f"WitnessAddress={self.WitnessAddress} "
        m += f"ParentHash={self.ParentHash} "
        m += f"Number={self.Number} "
        m += f"Timestamp={self.Timestamp} "
        m += f"WitnessSignature={self.WitnessSignature}"
        m += ")"

        return m

    def Transcations(self) -> list[tronTranscation]:
        """
        返回block里面的transcation的列表.
        不会解析所有的transcation, 只会解析一部分交易相关的. 
        具体会解析哪些, 还需要看看源码. 
        """
        # Lg.Trace(self.block)
        trxs = []
        if "transactions" not in self.block:
            return trxs 

        for trx in self.block["transactions"]:
            txid = trx["txID"]
            contract = trx["raw_data"]["contract"][0]

            if contract["type"] not in [
                "TransferContract", 
                "TransferAssetContract", 
                "TriggerSmartContract"
            ]:
                continue
            try:
                trxs.append(tronTranscation(trx, self.tron, self))
            except Exception as e:
                Lg.Warn(f"处理block'{self.BlockID}'的tx'{txid}'出错:\n" + traceback.format_exc())
                pass 

        return trxs 

class Tron():
    def __init__(self, nodeServer:str) -> None:
        self.nodeServer:str = nodeServer
        self.tron = TronAPI(HTTPProvider(nodeServer))
    
    def Block(self, blockNumber:int) -> tronBlock:
        block = self.tron.get_block(blockNumber)
        # Lg.Trace(block)
        return tronBlock(block, self)

if __name__ == "__main__":
    tttt = Tron("http://13.124.62.58:8090")
    bdf = tttt.Block(48311298)
    Lg.Trace(bdf)
    txs = bdf.Transcations()
    for tx in txs:
        if tx.TxID == '8e055811c777cd0cf5ec2b74f79a2cb4f1aaf143011e9afe468760d654f86465':
            Lg.Trace(tx)
            if tx.Asset != None:
                Lg.Trace(tx.Asset.Info())
            if tx.Contract != None:
                Lg.Trace(tx.Contract.Info())
            # ipdb.set_trace()