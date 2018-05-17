from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message

def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg

def reply_handler(msg):
    """Handles of server replies"""
    print "Server Response: %s, %s" % (msg.typeName, msg)

def create_contract(symbol, sec_type, exch, prim_exch, curr):

    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def create_order(order_type, quantity, action):

    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    return order

if __name__ == "__main__":

    # Connect to the Trader Workstation (TWS) running on the 7496 port; make clientId 100

    tws_conn = Connection.create(port=7496, clientId=100)
    tws_conn.connect()

    # Assign the error handling function defined above
    # to the TWS connection
    tws_conn.register(error_handler, 'Error')

    # Assign all of the server reply messages to the
    # reply_handler function defined above
    tws_conn.registerAll(reply_handler)

    # Create an order ID which is 'global' for this session. Change as orders increase
    order_id = 2

    # Create a contract in AAPL stock via SMART order routing
    AAPL_contract = create_contract('AAPL', 'STK', 'SMART', 'SMART', 'USD')

    # Sell 100 shares of Apple:
    AAPL_order = create_order('MKT', 100, 'SELL')

    # Use the connection to the send the order to IB
    tws_conn.placeOrder(order_id, AAPL_contract, AAPL_order)

    # Disconnect from TWS
    tws_conn.disconnect()
