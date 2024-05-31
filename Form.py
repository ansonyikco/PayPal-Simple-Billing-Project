import PayPal_function
import Record
from flask import Flask, request, render_template, redirect, url_for
import TokenTransaction
import datetime
app = Flask(__name__)

receiving_address = ""
receiving_amount = ""
available_list ={}
Contract_address = ''
def get_reference_id():
    now = datetime.datetime.now()
    date_string = now.strftime("%Y%m%d%H%M")
    date_int = int(date_string)
    return (date_int)
class Order:
    # class attribute 
    attr1 = "NFT"

    # Instance attribute 
    def __init__(self, given_name, surname, email,amount,token_type):
        self.given_name = given_name
        self.surname = surname
        self.email = email
        self.currency = 'USD'
        self.price = 10
        self.amount = float (amount)
        self.bill = self.price*self.amount
        self.token_type = token_type
        

    def create_order(self):
        self.access_token, self.id = PayPal_function.create_order_(self.currency, self.bill)

    def create_link(self):
        self.Link = PayPal_function.make_payment_link(self.given_name, self.surname, self.email, self.access_token,
                                                      self.id)

    def check_paid(self):
        self.status = PayPal_function.check_paid(self.access_token, self.id)


def Delivery():
    print('Delivery')
    print(Record.status_book)
    print(Record.Token_book)
    print(Record.id_book)
    #  Tim - TokenTransfer here [START]
    global receiving_address, receiving_amount,token_type,available_list,Contract_address
    print (receiving_address, receiving_amount,token_type,available_list,Contract_address)
    tx_result = TokenTransaction.transfer_to(Contract_address,receiving_address, receiving_amount)
    if tx_result:
        print("Token Transaction Success")
        return True
    else:
        print("Token Transaction Fail")
        return False
    #  Tim - TokenTransfer here [END]


@app.route('/')
def formPage():
    try:
        
        Token_list = TokenTransaction.check_available()
    except:
        Token_list= ["Token server not yet ready"]
    global available_list
    available_list = Token_list
    return render_template('form2.html',Token_list= list(available_list))


@app.route('/back', methods=['POST'])
def back():
    #Token_list = TokenTransaction.check_available()
    return render_template('form2.html',Token_list= list(available_list))
   


@app.route('/submit', methods=['POST'])
def submit():
    try:
        print('try')
        given_name = request.form['gname']
        print(given_name)
        surname = request.form['sname']
        email = request.form['email']  # 'sb-fa2bn29862044@personal.example.com'#request.form['email']
        user = given_name + ' ' + surname
        print(user)
        print("post : user => ", user)

        global receiving_address, receiving_amount,token_type,available_list,Contract_address
        receiving_address = request.form['receiving_address']
        receiving_amount = request.form['receiving_amount']
        token_type = request.form['Token']
        Contract_address=available_list[token_type]
        order1 = Order(given_name, surname, email,receiving_amount,token_type)  # PayPal_function.make_payment_link(given_name,surname,email)

        order1.create_order()
        print(order1.id)
        order1.create_link()

        Record.Token_book.append(order1.access_token)
        Record.id_book.append(order1.id)
        Record.Name_book.append(user)
        Record.Amount_book.append(receiving_amount)
        Record.status_book.append("ORDER CREATED")
        
        Record.Reference_Number_book.append(get_reference_id())
        
        Link = order1.Link
        print(Link)
        return redirect(Link, code='302')

    except:
        return render_template('Paid.html', status="Token server not yet ready.")


@app.route('/check_paid')
def check_paid():

    serial = len(Record.Token_book) - 1
    token = Record.Token_book[serial]
    print(token)
    PayerID = Record.id_book[serial]
    print(PayerID)
    check_result = PayPal_function.check_paid_(token, PayerID)
    status = check_result.get('status')
    Reference_Number = get_reference_id()
    if status == 'COMPLETED': # paid money
        Record.status_book[-1]='PAYMENT '+status
        Record.Reference_Number_book[-1]=(Reference_Number)
        
        if Delivery(): 
            Record.status_book[-1]='TOKEN DELIVERED'
            Message = ' Payment completed and token is given to you. Thx!  Reference Time : {}'.format(Reference_Number)
            return render_template('Paid.html', status=Message)
        else: 
            Message = 'Due to an error, our system currently fails to give you the token.'
            refund_id = check_result["purchase_units"][0]["payments"]['captures'][0]['id']
            refund_status = PayPal_function.refund(token, PayerID,refund_id)
            if refund_status == "COMPLETED":
                Message += ' But refund has been completed. Hope to see u again. \nReference Time : {}'.format(Reference_Number)
                Record.status_book[-1] = 'REFUND '+str(refund_status)
                Record.Reference_Number_book[-1] = Reference_Number
            else: 
                Message += ' But refund cannot be done right now. Reference Time : {}'.format(Reference_Number)
                Record.status_book[-1] = 'REFUND '+str(refund_status)
                Record.Reference_Number_book[-1] = Reference_Number
            return render_template('Paid.html', status=Message)


        

    return render_template('Paid.html', status=status)




if __name__ == '__main__':
    app.run(host='localhost', port=5000)
