from pydantic import BaseSettings


class EnvConfig:
    validate_assignment = True  # 属性更新時の検証を有効にする
    env_prefix = ""
    env_file = ".env"  # .envを読み込む


class RabbitmqConfig(BaseSettings):
    class Config(EnvConfig):
        pass

    RABBITMQ_HOST: str


class ElasticSearchConfig(BaseSettings):
    class Config(EnvConfig):
        pass

    ES_CLOUD_ID: str
    ES_USER: str
    ES_SECRET: str


class FirebaseConfig(BaseSettings):
    class Config(EnvConfig):
        pass

    GOOGLE_APPLICATION_CREDENTIALS = "secret_firebase.json"
    DEFAULT_BUCKET = "government-ee2de.appspot.com"

    def set_env(self):
        import os

        # 環境変数にクレデンシャルへのパスを設定しないと使えない
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = self.GOOGLE_APPLICATION_CREDENTIALS
