logger = logging.getLogger('engine.layers')

def mylog():
    try:
      print('1')
    except:
      logger.exception(
          's',
          extra={
              'sa_uid': uid,
              'tax_number': tax_number,
              'email': email,
              'login': login,
              'organization': organization
          }
        )
      
if __name__ == '__main__':
    mylog()
