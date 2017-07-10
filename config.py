class Config(object):
    DEBUG = True
    
    
class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    
class TestConfig(Config):
    TESTING = True
    
app_config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestConfig
}