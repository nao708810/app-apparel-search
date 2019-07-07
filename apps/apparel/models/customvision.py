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
    def get_prediction(self, image_path):
        """走行データリストに Custom Vision 解析結果を格納して返却

        Custom Vision ポータルでトレーニング済みの Project を検索。
        BlobコンテナのURLを指定して画像を解析させ、画像解析結果を取得する。

        Args:
            entities (list): 走行データのリスト
            blob_url (str): BlobコンテナへのアクセスURL

        Returns:
            予測値5割を超える場合に解析結果を格納する。
            予測値が5割以下の場合は"予測結果なし"を格納する。
            引数の走行データを全件検索し終えると、
            画像解析結果を格納した走行データリストを返却する。

        """
        #トレーニング済みの指定プロジェクト検索
        project = self._get_train_project()
            
        #CustomVisionによるAI解析開始
        results = self.predictor.classify_image_url(project.id,\
                self.publish_iteration_name, image_path)
        #予測値が最大のオブジェクトを取得
        prediction = max(results.predictions, key=lambda x: x.probability)
        #予測値が5割を超える場合は予測結果として格納
        return prediction
