class BaseConfig(object):
    BASE_URL = '/'
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'essay2021'

    # SQLALCHEMY_DATABASE_URI = 'mysql://admin:123456@db:3306/noni'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/essay'
    # SQLALCHEMY_DATABASE_URI = 'mysql://admin:go3gether#@momo-db-test.crzyjr9tepyo.ap-northeast-2.rds.amazonaws.com:3306/noni'

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PROPAGATE_EXCEPTIONS = True


    #FCM_API_URL = 'https://fcm.googleapis.com/fcm/send'
    #FCM_AUTH_KEY = 'AAAAwttfJgs:APA91bFWMRK6gB3Sh28TupoIBf88lxVbTRtjNNiBnYY-D4JLYJe6k5ETjk7Zwdwi1up9DYQTan_xmJy77fFxxV0eUf6FyXx2yOMngfSefp_63-qIDQ3Z8varCRdYa3gnjg-CeM2huboJ'

