"""
Connect Azure Blob
"""
from azure.storage.blob import BlockBlobService

#Azureブロブ操作クラス
class Blob():
    """Azure Blob 操作クラス

    Azure Storage Blob service を操作するためのクラス。
    config.pyに設定した Azure Storage のアカウント名と接続キーがインスタンスに必要。

    Attributes:
        table_service: TableService クラスのインスタンス

    """
    def __init__(self, name, key):
        #コンストラクタの定義
        self.block_blob_service = BlockBlobService(account_name=name, account_key=key)

    #ユーザーIDをキーにストレージ検索
    def upload_image(self, blob_name, file_name, file_path):
        """戻り値なし"""
        self.block_blob_service.create_blob_from_path(blob_name, file_name, file_path)
