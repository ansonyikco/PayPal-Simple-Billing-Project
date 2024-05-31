import requests
import json

available_list={}

def check_available():
    
   
    url = 'http://localhost:3001/api/seller/contracts'
    check_result = requests.get(url)
    check = json.loads(check_result.text)
    check = check['msg']
    for each in check:
        if int(each['totalSupply'])>0 and each['currentStage'] =='2':
            
           
            
      
            available_list[each['tokenSymbol']] = each['contractAddress']
    
    return available_list
            
    # print("Transaction Server (Port 3001) said:", tx.msg)
    
def transfer_to(contract_address,
                buyer_address, amount):
    try:
       
        url = 'http://localhost:3001/api/seller/transfer'
        transaction_request = {
            "contractAddress": contract_address,
            "toAddress": buyer_address,
            "amount": amount
        }
        tx_result = requests.post(url, json=transaction_request)
        tx = json.loads(tx_result.text)
        print (tx)
        # print("Transaction Server (Port 3001) said:", tx.msg)
        return tx['result']
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    print (check_available())
  