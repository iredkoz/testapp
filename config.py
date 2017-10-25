class Config(object):
    DEBUG = False
    
class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    
class TestConfig(Config):
    TESTING = True
    
app_config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestConfig
}