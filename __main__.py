from web import RequestManager

rm = RequestManager('test', '', '')
if __name__ == '__main__':
    rm.run('0.0.0.0', 988)