"""
Connect Azure Custom Vision
"""
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

class Customvision():
    """Custom Vision 操作クラス

    Azure Custom Vision service を操作するためのクラス。
    config.pyに設定した Custom Vision 接続キーがインスタンスに必要。

    Attributes:
        predictor: CustomVisionPredictionClient クラスのインスタンス
        trainer: CustomVisionTrainingClient クラスのインスタンス
        project_name (str): トレーニング済みの Custom Vision Project の名前
        publish_iteration_name (str): 公開されたイテレーションの名前

    """
    def __init__(self, training_key, prediction_key, endpoint, project_name,\
         publish_iteration_name):
        #コンストラクタの定義
        self.predictor = CustomVisionPredictionClient(prediction_key, endpoint=endpoint)
        self.trainer = CustomVisionTrainingClient(training_key, endpoint=endpoint)
        self.project_name = project_name
        self.publish_iteration_name = publish_iteration_name

    #トレーニング済みの指定プロジェクト検索
    def _get_train_project(self):
        """トレーニング済みの Project を検索して返却

        CustomVisionTrainingClientのインスタンスからポータル上で作成された
        project を取得する。
        取得した project の中から指定した project があるかを比較する。

        Returns:
            指定した project があった場合、 取得した project を返却。
            なかった場合は、None を返却する。

        """
        ret_project = None
        for project in self.trainer.get_projects():
            if project.name == self.project_name:
                ret_project = project
        return ret_project

    #CustomVisionによる解析結果を走行データに格納して返却
    def get_prediction(self, blob_url):
        """走行データリストに Custom Vision 解析結果を格納して返却

        Custom Vision ポータルでトレーニング済みの Project を検索。
        BlobコンテナのURLを指定して画像を解析させ、画像解析結果を取得する。

        Args:
            entities (list): 走行データのリスト
            blob_url (str): BlobコンテナへのアクセスURL

        Returns:
        """
        #トレーニング済みの指定プロジェクト検索
        project = self._get_train_project()

        #CustomVisionによるAI解析開始
        results = self.predictor.classify_image_url(project.id,\
                self.publish_iteration_name, blob_url)

        #数値高い順に並び替え
        predictions = sorted(results.predictions, key=lambda prob: prob.probability, reverse=True)

        return predictions
